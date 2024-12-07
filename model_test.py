import pytest
import pandas as pd
import numpy as np
from mylib.lib import (
    data_split_to_feature_outcome,
    rank_teams_produce_top_68,
    post_season_mapping,
)


@pytest.fixture
def sample_dataframe():
    data = {
        "team": ["A", "B", "C", "D", "E"],
        "feature1": [1, 2, 3, 4, 5],
        "feature2": [5, 4, 3, 2, 1],
        "feature3": [10, 15, 20, 25, 30],
        "SEED": [1, 2, 3, np.nan, 5],
        "POSTSEASON": ["Champion", "Final Four", "Sweet Sixteen", None, "Round of 64"],
    }
    return pd.DataFrame(data)


def test_data_split_to_feature_outcome(sample_dataframe):
    outcome = "SEED"
    features = ["feature1", "feature2", "feature3"]
    X, y = data_split_to_feature_outcome(sample_dataframe, outcome, features)
    assert not X.isnull().values.any()
    assert len(X) == 4
    assert all(col in X.columns for col in features)
    assert len(y) == 4
    assert y.dtype == int


def test_rank_teams_produce_top_68():
    data = {"team": [f"Team {i}" for i in range(1, 100)], "score": np.random.rand(99)}
    df = pd.DataFrame(data)
    result = rank_teams_produce_top_68(df, "score")
    assert len(result) == 99
    assert not result["predicted_seed_with_update"].isnull().all()
    assert result["predicted_seed_with_update"].nunique() <= 16


def test_post_season_mapping():
    data = {"team": ["A", "B", "C"], "POSTSEASON_LABEL": [0, 1, 2]}
    df = pd.DataFrame(data)
    result = post_season_mapping(df, "POSTSEASON_LABEL")
    assert result.isin(["Winner", "Runner-Up", "Final Four"]).all()


if __name__ == "__main__":
    pytest.main([__file__])
