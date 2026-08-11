import pytest
from pydantic import ValidationError
from schema.user_input import UserInput

def test_valid_user_input():
    user = UserInput(
        age=30,
        weight=70.0,
        height=1.75,
        income_lpa=10.0,
        smoker=False,
        city="  mumbai  ",
        occupation="private_job"
    )
    assert user.city == "Mumbai"
    assert round(user.bmi, 2) == round(70.0 / (1.75 ** 2), 2)
    assert user.age_group == "adult"
    assert user.city_tier == 1
    assert user.lifestyle_risk == "low"

def test_invalid_age():
    with pytest.raises(ValidationError):
        UserInput(
            age=0,
            weight=70.0,
            height=1.75,
            income_lpa=10.0,
            smoker=False,
            city="Delhi",
            occupation="private_job"
        )

def test_invalid_height():
    with pytest.raises(ValidationError):
        UserInput(
            age=30,
            weight=70.0,
            height=0.2,  # Height below 0.5m
            income_lpa=10.0,
            smoker=False,
            city="Delhi",
            occupation="private_job"
        )

def test_invalid_weight_nan():
    with pytest.raises(ValidationError):
        UserInput(
            age=30,
            weight=float('nan'),
            height=1.70,
            income_lpa=10.0,
            smoker=False,
            city="Delhi",
            occupation="private_job"
        )

def test_empty_city():
    with pytest.raises(ValidationError):
        UserInput(
            age=30,
            weight=70.0,
            height=1.70,
            income_lpa=10.0,
            smoker=False,
            city="   ",
            occupation="private_job"
        )

def test_invalid_occupation():
    with pytest.raises(ValidationError):
        UserInput(
            age=30,
            weight=70.0,
            height=1.70,
            income_lpa=10.0,
            smoker=False,
            city="Delhi",
            occupation="astronaut"  # Not in allowed enum
        )
