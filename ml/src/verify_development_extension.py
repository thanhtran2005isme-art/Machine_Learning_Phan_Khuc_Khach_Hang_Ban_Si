"""Verify committed Gate 10.2 artifact against a fresh development-only fit.

Frozen SHA is strict for committed evidence. Cross-run SVD floating-point
differences are compared numerically, including optional PCA axis sign flips.
Never open test.csv or fit the production scaler/KMeans.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from tempfile import TemporaryDirectory

import numpy as np
from sklearn.metrics import adjusted_rand_score

from ml.src.data_paths import PROJECT_ROOT, TEST_CSV
from ml.src.development_extension import create_extension, DEFAULT_OUTPUT


def verify(*, root: Path = PROJECT_ROOT, source: Path = DEFAULT_OUTPUT) -> dict:
    root = Path(root)
    source = Path(source)
    if (root / "data/processed/test.csv").exists() or TEST_CSV.exists():
        raise ValueError("Held-out final test CSV must not be present during Gate 10.2")
    metadata = json.loads((source / "metadata.json").read_text(encoding="utf-8"))
    raw = (source / "analysis.json").read_bytes()
    expected = metadata["files"]["analysis.json"]["sha256"]
    canonical = raw.replace(b"\r\n", b"\n")
    if hashlib.sha256(raw).hexdigest() != expected and hashlib.sha256(canonical).hexdigest() != expected:
        raise ValueError("Committed analysis SHA256 mismatch")
    committed = json.loads(raw)
    if not (
        metadata["status"] == "COMPLETE" and metadata["test_used"] is False
        and metadata["serving_model_changed"] is False and len(committed["points"]) == 352
    ):
        raise ValueError("Committed analysis status or number of rows invalid")

    with TemporaryDirectory(prefix="gate10-2-replay-") as temporary:
        output = Path(temporary)
        replay_metadata = create_extension(root=root, output=output)
        replay = json.loads((output / "analysis.json").read_text(encoding="utf-8"))
    if replay_metadata["provenance"] != metadata["provenance"]:
        raise ValueError("Frozen data provenance changed")
    if len(replay["points"]) != len(committed["points"]) or len(committed["points"]) != 352:
        raise ValueError("Development row count changed")

    old = committed["points"]
    new = replay["points"]
    if [(p["index"],p["split"],p["kmeans"]) for p in old] != [
         (p["index"],p["split"],p["kmeans"]) for p in new]:
        raise ValueError("Frozen row index, split or assignment changed")
    if adjusted_rand_score([p["hierarchical"] for p in old],
                           [p["hierarchical"] for p in new]) < 1 - 1e-12:
        raise ValueError("Ward partition changed")

    a = np.asarray(committed["pca"]["components"], dtype=float)
    b = np.asarray(replay["pca"]["components"], dtype=float)
    if a.shape != (2,6) or b.shape != (2,6):
        raise ValueError("Unexpected PCA loadings")
    sign = np.where(np.sum(a*b, axis=1) >= 0, 1., -1.)
    np.testing.assert_allclose(a, b*sign[:,None], rtol=0, atol=1e-8)
    av = np.asarray(committed["pca"]["explained_variance_ratio"], dtype=float)
    bv = np.asarray(replay["pca"]["explained_variance_ratio"], dtype=float)
    np.testing.assert_allclose(av,bv,rtol=0,atol=1e-10)
    old_points = np.asarray([[p["pc1"],p["pc2"]] for p in old], dtype=float)
    new_points = np.asarray([[p["pc1"],p["pc2"]] for p in new], dtype=float)
    np.testing.assert_allclose(old_points,new_points*sign,rtol=0,atol=1e-8)

    for key in ("silhouette_kmeans","silhouette_hierarchical","ari"):
        if not np.isclose(committed["comparison"][key], replay["comparison"][key], rtol=0, atol=1e-10):
            raise ValueError("Comparison metric changed: "+key)
    if sorted(committed["comparison"]["hierarchical_counts"]) != sorted(replay["comparison"]["hierarchical_counts"]):
        raise ValueError("Ward counts changed")
    if not np.isclose(committed["comparison"]["silhouette_kmeans"],0.28915821493432775,rtol=0,atol=1e-8):
        raise ValueError("D011 silhouette disagrees with frozen evaluation")
    print("[Gate10.2] PASS: exact original SHA; semantic replay <=1e-8 PCA; identical frozen/Ward partitions; no final test")
    return metadata


if __name__=="__main__":
    verify()
