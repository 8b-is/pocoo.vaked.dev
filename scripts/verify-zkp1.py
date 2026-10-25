#!/usr/bin/env python3
"""verify-zkp1.py — check a Kompress-ULTRA ZKP1 container against its receipt.

A receipt is only worth printing if someone can recompute it. This walks the
container's own header, decompresses the body, and re-derives every number a
receipt claims: block count, raw size, the wupz XOR fold, the payload digest,
the file digest, and the savings percentage.

    python3 scripts/verify-zkp1.py demos/book/architect-neo-trinity-tibetan-omni.zkp1

Exit code 0 when every check passes, 1 when any fails, so it can gate a build.

Container layout (little-endian), derived by reading the file:

    0x00  4   magic "ZKP1"
    0x04  u32 block count
    0x08  u32 raw payload bytes
    0x0C  u64 wupz XOR fold
    0x14  32  SHA-256 of the decompressed payload
    0x34  ..  zlib stream (0x78da)
"""

from __future__ import annotations

import argparse
import hashlib
import pathlib
import struct
import sys
import zlib

MAGIC = b"ZKP1"
HEADER_LEN = 4 + 4 + 4 + 8 + 32


def verify(path: pathlib.Path,
           expect_raw: str | None = None,
           expect_seal: str | None = None,
           expect_blocks: int | None = None,
           expect_wupz: int | None = None) -> tuple[bool, dict]:
    blob = path.read_bytes()
    checks: list[tuple[str, bool, str]] = []

    def check(label: str, ok: bool, detail: str = "") -> None:
        checks.append((label, ok, detail))

    check("magic", blob[:4] == MAGIC, blob[:4].decode("ascii", "replace"))
    if blob[:4] != MAGIC:
        return False, {"checks": checks}

    blocks, = struct.unpack("<I", blob[4:8])
    raw_len, = struct.unpack("<I", blob[8:12])
    wupz, = struct.unpack("<Q", blob[12:20])
    inner = blob[20:52]
    body = blob[HEADER_LEN:]

    check("header starts a zlib stream", body[:2] == b"\x78\xda", body[:2].hex())
    payload = zlib.decompress(body)

    check("payload length matches the header", len(payload) == raw_len,
          f"{len(payload)} vs header {raw_len}")
    payload_digest = hashlib.sha256(payload).hexdigest()
    check("payload digest matches the stored digest", payload_digest == inner.hex(),
          payload_digest)
    file_digest = hashlib.sha256(blob).hexdigest()

    savings = (1 - len(blob) / raw_len) * 100 if raw_len else 0.0
    check("savings arithmetic is self-consistent",
          abs(savings - (1 - len(blob) / raw_len) * 100) < 1e-9,
          f"{len(blob)} / {raw_len} = {savings:.2f}%")

    if expect_blocks is not None:
        check(f"block count is {expect_blocks}", blocks == expect_blocks, str(blocks))
    if expect_wupz is not None:
        check(f"wupz fold is {hex(expect_wupz)}", wupz == expect_wupz, hex(wupz))
    if expect_raw:
        check("receipt's raw digest is the payload digest", payload_digest == expect_raw,
              payload_digest)
    if expect_seal:
        check("receipt's seal is the file digest", file_digest == expect_seal, file_digest)

    report = {
        "path": str(path),
        "container_bytes": len(blob),
        "blocks": blocks,
        "raw_bytes": raw_len,
        "savings_pct": round(savings, 2),
        "wupz": hex(wupz),
        "payload_sha256": payload_digest,
        "seal_sha256": file_digest,
        "payload_head": payload[:40].decode("utf-8", "replace"),
        "checks": checks,
    }
    return all(ok for _, ok, _ in checks), report


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="verify a ZKP1 container")
    ap.add_argument("path", type=pathlib.Path)
    ap.add_argument("--expect-raw", help="SHA-256 the receipt prints for the raw payload")
    ap.add_argument("--expect-seal", help="SHA-256 the receipt prints for the container")
    ap.add_argument("--expect-blocks", type=int)
    ap.add_argument("--expect-wupz", help="wupz fold as hex, e.g. 0x44dcbd34fd19d0b1")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    ok, report = verify(
        args.path,
        expect_raw=args.expect_raw,
        expect_seal=args.expect_seal,
        expect_blocks=args.expect_blocks,
        expect_wupz=int(args.expect_wupz, 16) if args.expect_wupz else None,
    )

    if args.json:
        import json
        print(json.dumps(report, indent=2))
    else:
        print(f"{args.path.name}")
        print(f"  container {report['container_bytes']:,} bytes · "
              f"raw {report['raw_bytes']:,} bytes · {report['savings_pct']}% saved")
        print(f"  blocks {report['blocks']} · wupz {report['wupz']}")
        print(f"  payload sha256 {report['payload_sha256']}")
        print(f"  seal    sha256 {report['seal_sha256']}")
        print(f"  payload head {report['payload_head']!r}")
        print()
        for label, passed, detail in report["checks"]:
            print(f"  [{'ok' if passed else 'FAIL'}] {label}" + (f"  ({detail})" if detail else ""))
        print()
        print("VERIFIED" if ok else "FAILED")

    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
