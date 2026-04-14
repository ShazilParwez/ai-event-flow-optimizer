import pytest
from models.predictor import predict_crowd_trend


def test_prediction_output():
    result = predict_crowd_trend([10, 20, 30])
    assert result is not None


def test_empty_input():
    with pytest.raises(Exception):
        predict_crowd_trend([])