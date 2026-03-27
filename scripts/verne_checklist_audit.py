#!/usr/bin/env python3
"""Backward-compatible entrypoint for Verne checklist audits.
Use scripts/checklist_manifest_audit.py for generic country/project audits.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from checklist_manifest_audit import main  # type: ignore

if __name__ == "__main__":
    raise SystemExit(main())
