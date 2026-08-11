import pytest
from model.predict import predict_output

def test_prediction_low_risk_profile():
    sample_input = {
        'bmi': 22.2,
        'age_group': 'young',
        'lifestyle_risk': 'low',
        'city_tier': 1,
        'income_lpa': 15.0,
        'occupation': 'private_job'
    }
    result = predict_output(sample_input)
    assert "predicted_category" in result
    assert result["predicted_category"] in ["Low", "Medium", "High"]
    assert 0.0 <= result["confidence"] <= 1.0
    assert sum(result["class_probabilities"].values()) == pytest.approx(1.0, abs=0.01)

def test_prediction_high_risk_profile():
    sample_input = {
        'bmi': 33.5,
        'age_group': 'senior',
        'lifestyle_risk': 'high',
        'city_tier': 3,
        'income_lpa': 5.0,
        'occupation': 'retired'
    }
    result = predict_output(sample_input)
    assert "predicted_category" in result
    assert result["predicted_category"] in ["Low", "Medium", "High"]
    assert 0.0 <= result["confidence"] <= 1.0
