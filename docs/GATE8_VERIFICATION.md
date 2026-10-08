# Gate 8 — Final Code Audit & Windows clean install

**Status:** IN PROGRESS — Windows CI must finish before PASS. No report or slides.

## Scope

- Verify clean GitHub checkout on `windows-latest`, `npm ci`, audited Node dependencies, `npm run test:gate6` and Python↔Node frozen joblib parity.
- Playwright Chromium desktop and simulated mobile viewport on Windows. Verify missing/invalid values, out-of-training-range warning, API failure and dashboard.
- Execute the **actual** `run.bat` on Windows CI, poll `localhost:5173` + `127.0.0.1:3001/api/health`, send POST request to compiled model API.
- Audit source: fixed stale async form response after user cleared or edited inputs; add regression browser scenario.
- Keep Gate 5 D011 K=2 model immutable. Do not touch or open final test CSV. Do not perform ML training or re-evaluation.
- Audit file hygiene, stale docs and dependency security. Do not delete historical experiment/model evidence without provenance.

## Limitations

GitHub Actions `windows-latest` uses an actual Windows Server runner (not the user's Windows 10 device). Browser mobile project uses viewport/device emulation, not a physical phone. Neither can guarantee behavior of the user's installed OS, hardware, antivirus, firewall, browser extensions or locale. User should still do a final double-click and visual review locally.

## Evidence

Pending live CI logs. Gate 6 and 7 historical evidence at `docs/GATE6_SERVING.md` and `docs/GATE7_VERIFICATION.md`.
