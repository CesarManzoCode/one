#!/usr/bin/env python3
"""Minimal RV64 bare-metal ELF probes for Sail/Spike (ONE vault v0.3.0, SPEC-003 pre-code checks).

Not ONE tooling: a one-off generator kept only so the recorded probe results are reproducible.

Each probe runs in M-mode at 0x80000000 with a trap handler and exits through HTIF `tohost`:
  exit code 0             expected value observed in the checked register
  exit code 2             wrong value
  exit code >= 16         trap: code = (16 + mcause) | (mtval & 0xfff) << 8 | byte[DATA+0xffd] << 20
                          (*_tval probes: code = (16 + mcause) | (mtval & 0x3fffff) << 8)
Layout: .text 0x80000000, .tohost 0x80001000, .data 0x80002000 (0x1000 bytes, byte i = (0x11+i) & 0xff).
Probes *_region_end* expect main memory to end at 0x80003000.
"""
import os, struct, sys

BASE, TOHOST, DATA = 0x80000000, 0x80001000, 0x80002000
MTVEC, MCAUSE, MTVAL = 0x305, 0x342, 0x343
T0, T1, T2, S1, A0, A1, A2 = 5, 6, 7, 9, 10, 11, 12

def I(op, rd, f3, rs1, imm): return ((imm & 0xfff) << 20) | (rs1 << 15) | (f3 << 12) | (rd << 7) | op
def S(f3, rs1, rs2, imm):
    imm &= 0xfff
    return ((imm >> 5) << 25) | (rs2 << 20) | (rs1 << 15) | (f3 << 12) | ((imm & 0x1f) << 7) | 0x23
def B(f3, rs1, rs2, off):
    off &= 0x1fff
    return (((off >> 12) & 1) << 31) | (((off >> 5) & 0x3f) << 25) | (rs2 << 20) | (rs1 << 15) | (f3 << 12) \
        | (((off >> 1) & 0xf) << 8) | (((off >> 11) & 1) << 7) | 0x63
def J(rd, off):
    off &= 0x1fffff
    return (((off >> 20) & 1) << 31) | (((off >> 1) & 0x3ff) << 21) | (((off >> 11) & 1) << 20) \
        | (((off >> 12) & 0xff) << 12) | (rd << 7) | 0x6f

addi = lambda rd, rs, imm: I(0x13, rd, 0, rs, imm)
slli = lambda rd, rs, sh: I(0x13, rd, 1, rs, sh)
srli = lambda rd, rs, sh: I(0x13, rd, 5, rs, sh)
add = lambda rd, a, b: (b << 20) | (a << 15) | (rd << 7) | 0x33
ld = lambda rd, rs, imm: I(0x03, rd, 3, rs, imm)
lw = lambda rd, rs, imm: I(0x03, rd, 2, rs, imm)
lbu = lambda rd, rs, imm: I(0x03, rd, 4, rs, imm)
sd = lambda base, src, imm: S(3, base, src, imm)
csrrw = lambda rd, csr, rs: I(0x73, rd, 1, rs, csr)
csrrs = lambda rd, csr, rs: I(0x73, rd, 2, rs, csr)

def li64(rd, value):
    """Load a 64-bit constant nibble by nibble (fixed length: 33 words)."""
    out = [addi(rd, 0, 0)]
    for shift in range(60, -1, -4):
        out += [slli(rd, rd, 4), addi(rd, rd, (value >> shift) & 0xf)]
    return out

def build(body, reg, expected, wide=False):
    code = li64(T0, 0) + [csrrw(0, MTVEC, T0)] + body + li64(T1, expected)
    code += [B(0, reg, T1, 12), addi(S1, 0, 2), J(0, 8), addi(S1, 0, 0)]
    exit_at = len(code)
    code += li64(T2, TOHOST) + [slli(S1, S1, 1), addi(S1, S1, 1), sd(T2, S1, 0), J(0, 0)]
    handler = len(code)
    code += [csrrs(S1, MCAUSE, 0), addi(S1, S1, 16),
             csrrs(T1, MTVAL, 0)]
    if wide:  # code = (16 + mcause) | (mtval & 0x3fffff) << 8
        code += [slli(T1, T1, 42), srli(T1, T1, 34), add(S1, S1, T1)]
    else:
        code += [slli(T1, T1, 52), srli(T1, T1, 44), add(S1, S1, T1)]
        code += li64(T2, DATA + 0xffd) + [lbu(T1, T2, 0), slli(T1, T1, 20), add(S1, S1, T1)]
    code.append(J(0, (exit_at - len(code)) * 4))
    code[:33] = li64(T0, BASE + handler * 4)
    return b"".join(struct.pack("<I", w) for w in code)

def elf(text, data, path):
    names = b"\0.text\0.tohost\0.data\0.symtab\0.strtab\0.shstrtab\0"
    n = lambda s: names.index(s)
    strtab = b"\0tohost\0fromhost\0"
    sym = lambda name, val: struct.pack("<IBBHQQ", name, 0x10, 0, 2, val, 8)
    symtab = bytes(24) + sym(1, TOHOST) + sym(8, TOHOST + 8)
    o_text = 64 + 3 * 56; o_toh = o_text + len(text); o_data = o_toh + 16
    o_sym = o_data + len(data); o_str = o_sym + len(symtab); o_shs = o_str + len(strtab); o_sh = o_shs + len(names)
    out = b"\x7fELF" + bytes([2, 1, 1, 0]) + bytes(8)
    out += struct.pack("<HHIQQQIHHHHHH", 2, 243, 1, BASE, 64, o_sh, 0, 64, 56, 3, 64, 7, 6)
    for o, a, size, flags in ((o_text, BASE, len(text), 5), (o_toh, TOHOST, 16, 6), (o_data, DATA, len(data), 6)):
        out += struct.pack("<IIQQQQQQ", 1, flags, o, a, a, size, size, 4)
    out += text + bytes(16) + data + symtab + strtab + names
    sh = lambda nm, t, fl, a, o, sz, link=0, info=0, al=1, ent=0: struct.pack("<IIQQQQIIQQ", nm, t, fl, a, o, sz, link, info, al, ent)
    out += bytes(64) + sh(n(b".text"), 1, 6, BASE, o_text, len(text), al=4) + sh(n(b".tohost"), 1, 3, TOHOST, o_toh, 16, al=8) \
        + sh(n(b".data"), 1, 3, DATA, o_data, len(data)) + sh(n(b".symtab"), 2, 0, 0, o_sym, len(symtab), 5, 1, 8, 24) \
        + sh(n(b".strtab"), 3, 0, 0, o_str, len(strtab)) + sh(n(b".shstrtab"), 3, 0, 0, o_shs, len(names))
    with open(path, "wb") as f:
        f.write(out)

def iw(funct7, shamt5, f3): return (funct7 << 25) | (shamt5 << 20) | (A0 << 15) | (f3 << 12) | (A1 << 7) | 0x1b

def main(outdir):
    os.makedirs(outdir, exist_ok=True)
    data = bytes((0x11 + i) & 0xff for i in range(0x1000))
    le = lambda addr, size: int.from_bytes(data[addr - DATA: addr - DATA + size], "little")
    sext32 = lambda v: (v ^ 0x80000000) - 0x80000000 & (2**64 - 1)
    v = 0x0123456789abcdef
    x = li64(A0, 0xf0000001)
    encodings = {
        "slliw_imm5_1": iw(0b0000001, 1, 1), "srliw_imm5_1": iw(0b0000001, 1, 5), "sraiw_imm5_1": iw(0b0100001, 1, 5),
        "slliw_ctrl": iw(0, 1, 1), "srliw_ctrl": iw(0, 1, 5), "sraiw_ctrl": iw(0b0100000, 1, 5),
    }
    probes = {
        "al_ld_control": build(li64(A0, DATA + 0x100) + [ld(A1, A0, 0)], A1, le(DATA + 0x100, 8)),
        "mis_ld_intrapage": build(li64(A0, DATA + 0x101) + [ld(A1, A0, 0)], A1, le(DATA + 0x101, 8)),
        "mis_lw_intrapage": build(li64(A0, DATA + 0x103) + [lw(A1, A0, 0)], A1, sext32(le(DATA + 0x103, 4))),
        "mis_sd_intrapage": build(li64(A0, DATA + 0x201) + li64(A2, v) + [sd(A0, A2, 0), ld(A1, A0, 0)], A1, v),
        "mis_ld_crosspage": build(li64(A0, DATA + 0xffd) + [ld(A1, A0, 0)], A1, le(DATA + 0xffd, 3) | (0x11 << 24) | (0x12 << 32) | (0x13 << 40) | (0x14 << 48) | (0x15 << 56)),
        "mis_ld_region_end": build(li64(A0, DATA + 0xffd) + [ld(A1, A0, 0)], A1, 0),
        "mis_sd_region_end": build(li64(A0, DATA + 0xffd) + li64(A2, v) + [sd(A0, A2, 0)], A1, 0),
        "mis_ld_region_end_tval": build(li64(A0, DATA + 0xffd) + [ld(A1, A0, 0)], A1, 0, wide=True),
        "mis_sd_region_end_tval": build(li64(A0, DATA + 0xffd) + li64(A2, v) + [sd(A0, A2, 0)], A1, 0, wide=True),
        "slliw_ctrl": build(x + [encodings["slliw_ctrl"]], A1, 0xffffffffe0000002),
        "srliw_ctrl": build(x + [encodings["srliw_ctrl"]], A1, 0x78000000),
        "sraiw_ctrl": build(x + [encodings["sraiw_ctrl"]], A1, 0xfffffffff8000000),
        "slliw_imm5_1": build(x + [encodings["slliw_imm5_1"]], A1, 0),
        "srliw_imm5_1": build(x + [encodings["srliw_imm5_1"]], A1, 0),
        "sraiw_imm5_1": build(x + [encodings["sraiw_imm5_1"]], A1, 0),
    }
    for name, text in probes.items():
        # crosspage probe needs the next page mapped: extend data with a second pattern page
        payload = data + bytes((0x11 + i) & 0xff for i in range(0x1000)) if name == "mis_ld_crosspage" else data
        elf(text, payload, os.path.join(outdir, name + ".elf"))
    with open(os.path.join(outdir, "encodings.txt"), "w") as f:
        f.writelines(f"{k} 0x{w:08x}\n" for k, w in encodings.items())

if __name__ == "__main__":
    main(sys.argv[1])
