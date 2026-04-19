import pandas as pd
import pytest
import random
from models.crowd_model import classify_crowd


# Helper
def create_test_df(density, area="A"):
    return pd.DataFrame({
        "area_name": [area],
        "density": [density]
    })


# PARAMETRIZED TEST (CORE LOGIC)
@pytest.mark.parametrize("density,expected", [
    (10, "Low"),
    (80, "Medium"),
    (150, "High"),
])
def test_density_levels(density, expected):
    df = create_test_df(density)
    result = classify_crowd(df)
    assert result["A"] == expected


# EDGE CASES

def test_empty_dataframe():
    df = pd.DataFrame()
    with pytest.raises(ValueError):
        classify_crowd(df)


def test_missing_columns():
    df = pd.DataFrame({"wrong": [1, 2]})
    with pytest.raises(ValueError):
        classify_crowd(df)


def test_invalid_input_type():
    with pytest.raises(Exception):
        classify_crowd("invalid_input")


# MULTI-AREA REALISTIC TEST

def test_multiple_areas():
    df = pd.DataFrame({
        "area_name": ["A", "B", "C"],
        "density": [20, 90, 140]
    })
    result = classify_crowd(df)

    assert isinstance(result, dict)
    assert len(result) == 3
    assert result["A"] == "Low"
    assert result["B"] == "Medium"
    assert result["C"] == "High"


# RANDOMIZED ROBUSTNESS TEST

def test_random_density_values():
    for _ in range(10):
        val = random.randint(0, 200)
        df = create_test_df(val)
        result = classify_crowd(df)

        assert isinstance(result["A"], str)
        assert result["A"] in ["Low", "Medium", "High"]


# LARGE DATA TEST

def test_large_dataset():
    df = pd.DataFrame({
        "area_name": ["A"] * 1000,
        "density": [50] * 1000
    })
    result = classify_crowd(df)

    assert isinstance(result, dict)
    assert "A" in result


# EXTREME VALUE TEST

def test_extreme_values():
    df = create_test_df(10000)
    result = classify_crowd(df)

    assert result["A"] == "High"


# NaN HANDLING

def test_nan_values():
    df = pd.DataFrame({
        "area_name": ["A"],
        "density": [None]
    })

    with pytest.raises(Exception):
        classify_crowd(df)


# CONSISTENCY TEST (DETERMINISTIC)

def test_consistency():
    df = create_test_df(80)

    result1 = classify_crowd(df)
    result2 = classify_crowd(df)

    assert result1 == result2


# BOUNDARY TESTS

def test_boundary_low_medium():
    df = create_test_df(60)
    result = classify_crowd(df)
    assert result["A"] in ["Low", "Medium"]


def test_boundary_medium_high():
    df = create_test_df(120)
    result = classify_crowd(df)
    assert result["A"] in ["Medium", "High"]