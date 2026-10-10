"""Gate 10.2: offline, development-only PCA projection and Ward comparison.

PCA and Hierarchical are exploratory fits over 352 development rows only.
The production D011 scaler and K-Means centroids are READ ONLY.
Never load a final test split or retrain the production model.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
from sklearn.cluster import AgglomerativeClustering
from sklearn.decomposition import PCA
from sklearn.metrics import adjusted_rand_score, silhouette_score

from ml.src.data_paths import PROJECT_ROOT
from ml.src.final_profile import FEATURES, frozen_predict, load_development

DEFAULT_OUTPUT = PROJECT_ROOT / "reports/data/development_extension"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def create_extension(*, root: Path = PROJECT_ROOT, train: Path | None = None,
                     validation: Path | None = None, output: Path | None = None) -> dict:
    """Validate all inputs BEFORE writing any extension artifact."""
    root = Path(root)
    train = Path(train) if train is not None else root / "data/processed/train.csv"
    validation = Path(validation) if validation is not None else root / "data/processed/validation.csv"
    output = Path(output) if output is not None else root / "reports/data/development_extension"
    frame, model, provenance = load_development(root, train, validation)
    frozen, _ = frozen_predict(frame, model)
    assert len(frame) == 352 and np.bincount(frozen, minlength=2).tolist() == [162, 190]

    raw = frame[FEATURES].to_numpy(dtype=float, copy=True)
    mean = np.asarray(model["scaler_mean"], dtype=float)
    scale = np.asarray(model["scaler_scale"], dtype=float)
    X = (np.log1p(raw) - mean) / scale
    assert X.shape == (352, 6) and np.isfinite(X).all()

    # Unsupervised VISUALIZATION only: PCA is fitted to development 352 in
    # frozen feature space, with no test access and no effect on serving.
    pca = PCA(n_components=2, svd_solver="full")
    embedding = pca.fit_transform(X)
    variance = pca.explained_variance_ratio_
    if not np.isfinite(embedding).all() or not (0 < sum(variance) <= 1 + 1e-9):
        raise ValueError("Nonfinite PCA result")

    # Ward requires Euclidean geometry; same 6D X as frozen K-Means, NOT 2D
    # PCA coordinates, raw spending, Channel, or Region.
    ward = AgglomerativeClustering(n_clusters=2, linkage="ward", metric="euclidean")
    hierarchical = ward.fit_predict(X).astype(int)
    frozen_counts = np.bincount(frozen, minlength=2).astype(int).tolist()
    hier_counts = np.bincount(hierarchical, minlength=2).astype(int).tolist()
    contingency = [[int(np.count_nonzero((frozen == i) & (hierarchical == j)))
                    for j in (0, 1)] for i in (0, 1)]
    if min(hier_counts) == 0 or sum(map(sum, contingency)) != 352:
        raise ValueError("Invalid Ward groups")

    silhouette_frozen = float(silhouette_score(X, frozen))
    silhouette_ward = float(silhouette_score(X, hierarchical))
    ari = float(adjusted_rand_score(frozen, hierarchical))
    if not np.isclose(silhouette_frozen, 0.28915821493432775, atol=1e-8, rtol=0):
        raise ValueError("Frozen D011 development silhouette changed")

    rows = [
        {
            "index": int(i), "split": "train" if i < 264 else "validation",
            "pc1": float(embedding[i, 0]), "pc2": float(embedding[i, 1]),
            "kmeans": int(frozen[i]), "hierarchical": int(hierarchical[i]),
        }
        for i in range(352)
    ]
    analysis = {
        "schema_version": 1, "decision": "D011", "source_scope": "train_plus_validation",
        "feature_space": "frozen log1p + StandardScaler (6 dimensions)",
        "pca": {
            "explained_variance_ratio": [float(v) for v in variance],
            "components": [[float(c) for c in row] for row in pca.components_],
            "method": "PCA(n_components=2, svd_solver=full) fitted on 352 development",
            "usage": "Visualization only; production centroid assignment stays in 6D",
        },
        "comparison": {
            "method": "AgglomerativeClustering", "linkage": "ward", "metric": "euclidean",
            "n_clusters": 2, "fit_space": "frozen 6D log1p+StandardScaler",
            "frozen_counts": frozen_counts, "hierarchical_counts": hier_counts,
            "contingency": contingency, "ari": ari,
            "silhouette_kmeans": silhouette_frozen, "silhouette_hierarchical": silhouette_ward,
            "interpretation": "Exploratory Ward comparison; labels are arbitrary; no final test, selection or serving change.",
        },
        "points": rows,
    }
    raw_json = (json.dumps(analysis, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode("utf-8")
    metadata = {
        "schema_version": 1, "status": "COMPLETE", "decision": "D011",
        "scope": "train_plus_validation", "development_count": 352,
        "source_rows": {"train": 264, "validation": 88},
        "feature_columns": FEATURES, "profiling_only_columns": ["Channel", "Region"],
        "frozen_model_fit_performed": False, "frozen_scaler_fit_performed": False,
        "pca_fit_performed": True, "hierarchical_fit_performed": True,
        "test_used": False, "test_evaluated": False, "serving_model_changed": False,
        "provenance": provenance,
        "files": {"analysis.json": {
            "path": "reports/data/development_extension/analysis.json",
            "sha256": digest(raw_json),
        }},
    }
    raw_meta = (json.dumps(metadata, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode("utf-8")
    output.mkdir(parents=True, exist_ok=True)
    (output / "analysis.json").write_bytes(raw_json)
    (output / "metadata.json").write_bytes(raw_meta)
    return metadata


def main() -> None:
    parser = argparse.ArgumentParser(description="Offline PCA/Ward, development 352 only")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    info = create_extension(output=args.output)
    print("[Gate10.2] PCA/Ward 352 development, test_used=false, no model refit")
    print("[Gate10.2] analysis sha256:", info["files"]["analysis.json"]["sha256"])


if __name__ == "__main__":
    main()
