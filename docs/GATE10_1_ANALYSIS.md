# Gate 10.1 - Read-only analytics extension

Status: FEATURE BRANCH CI VERIFIED for code commit 43e808fe; NOT MERGED. No final-test reevaluation.

## Added
- Add detailed 14-candidate experiment table showing silhouette standard deviation and ARI minimum across seeds; fields come from the existing train/validation selection_evidence.csv, not simulated.
- Add descriptive outlier concentration from verified development 352-profile, explicitly without removing observations.
- Explain each customer assignment with six input-versus-cluster-median ratios, both centroid distances and distance gap. These values are never a probability/confidence.
- Export customer and experiment CSV with safe spreadsheet string encoding; use browser Print/Save PDF instead of claiming automatic PDF file generation.
- Add three-stage interactive Lloyd toy example from course reading Bài 8. Toy points are synthetic and separate from Wholesale Customers.
- Tests: Fastify shape/bounds and three Playwright E2E cases, each across desktop/mobile Chromium.

## Do not change
Frozen D011 K2 model/selection/final evaluation, Gate9.2 final profile, held-out test.
Do not run ml:freeze or ml:finalize.

## Next
PCA 2D and hierarchical comparison require offline development-only row-level evidence; do not manufacture PCA points. Add a reproducible offline generator and reviewed artifact in the next gate.

CI verified: GitHub Actions run 38020099636 SUCCESS on commit 43e808fe. Serving 15/15, Fastify 14/14, Playwright 46/46 (desktop + mobile Chromium), build, audit and Python-Node parity PASS. First run exposed an old 3-table expectation and mobile CSV click interception; fixed before the green run.