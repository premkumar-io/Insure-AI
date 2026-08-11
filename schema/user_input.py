from pydantic import BaseModel, Field, computed_field, field_validator
from typing import Literal, Annotated
import math
from config.city_tier import tier_1_cities, tier_2_cities

# Pydantic model to validate incoming user input payload
class UserInput(BaseModel):

    age: Annotated[int, Field(..., gt=0, lt=120, description='Age of the user in years')]
    weight: Annotated[float, Field(..., gt=0.0, le=500.0, description='Weight of the user in kg')]
    height: Annotated[float, Field(..., ge=0.5, le=2.5, description='Height of the user in meters')]
    income_lpa: Annotated[float, Field(..., gt=0.0, le=10000.0, description='Annual income in Lakhs Per Annum (₹)')]
    smoker: Annotated[bool, Field(..., description='Is user an active smoker')]
    city: Annotated[str, Field(..., min_length=1, description='Residential city')]
    occupation: Annotated[Literal[
        'retired', 'freelancer', 'student', 'government_job',
        'business_owner', 'unemployed', 'private_job'
    ], Field(..., description='Occupation of the user')]
    
    @field_validator('weight', 'height', 'income_lpa')
    @classmethod
    def validate_finite_floats(cls, v: float) -> float:
        if math.isnan(v) or math.isinf(v):
            raise ValueError("Value must be a valid finite number")
        return v

    @field_validator('city')
    @classmethod
    def normalize_city(cls, v: str) -> str:
        v = v.strip().title()
        if not v:
            raise ValueError("City name cannot be empty")
        return v
    
    @computed_field
    @property
    def bmi(self) -> float:
        return self.weight / (self.height ** 2)
    
    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        if self.smoker and self.bmi > 30:
            return "high"
        elif self.smoker or self.bmi > 27:
            return "medium"
        else:
            return "low"
        
    @computed_field
    @property
    def age_group(self) -> str:
        if self.age < 25:
            return "young"
        elif self.age < 45:
            return "adult"
        elif self.age < 60:
            return "middle_aged"
        return "senior"
    
    @computed_field
    @property
    def city_tier(self) -> int:
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:
            return 3

        