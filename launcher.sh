#!/bin/bash
cd /home/suraj/.gemini/antigravity/scratch/heavy_suite/zero-wasm-windows
git pull origin main --quiet
/home/suraj/.gemini/antigravity/scratch/v8_env/bin/python3 zero_wasm_gui.py
