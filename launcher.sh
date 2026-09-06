#!/bin/bash
# AUTO-UPDATER
cd /home/suraj/.gemini/antigravity/scratch/heavy_suite/zero-wasm-windows
git pull origin main --quiet
python3 zero_wasm_gui.py
