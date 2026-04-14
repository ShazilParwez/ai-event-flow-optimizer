import pandas as pd
from models.crowd_model import classify_crowd


def create_test_df(density):
    return pd.DataFrame({
        "area_name": ["A"],
        "density": [density]
    })


def test_low_density():
    df = create_test_df(10)
    result = classify_crowd(df)
    assert "Low" in result


def test_medium_density():
    df = create_test_df(80)
    result = classify_crowd(df)
    assert "Medium" in result


def test_high_density():
    df = create_test_df(150)
    result = classify_crowd(df)
    assert "High" in result