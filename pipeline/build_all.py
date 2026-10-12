"""Bakes processed JSON for the app from the challenge data + verified findings.

Run from the repo root: .venv/bin/python pipeline/build_all.py
Writes into app/public/data/.
"""
import mc1_build
import mc2_build

if __name__ == "__main__":
    mc1_build.main()
    mc2_build.main()
