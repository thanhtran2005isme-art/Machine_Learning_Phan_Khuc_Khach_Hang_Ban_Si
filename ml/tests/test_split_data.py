import numpy as np

from ml.src.split_data import assert_disjoint_and_complete, split_indices


def test_split_is_reproducible() -> None:
    first = split_indices(440, seed=42)
    second = split_indices(440, seed=42)
    for left, right in zip(first, second, strict=True):
        assert np.array_equal(left, right)


def test_default_split_counts_and_no_overlap() -> None:
    train_idx, validation_idx, test_idx = split_indices(440, seed=42)
    assert len(train_idx) == 264
    assert len(validation_idx) == 88
    assert len(test_idx) == 88
    assert_disjoint_and_complete(train_idx, validation_idx, test_idx, 440)


def test_different_seed_changes_assignment() -> None:
    first_train, _, _ = split_indices(440, seed=42)
    second_train, _, _ = split_indices(440, seed=43)
    assert not np.array_equal(first_train, second_train)
