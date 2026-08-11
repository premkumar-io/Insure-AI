from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional

class PredictionResponse(BaseModel):
    predicted_category: str = Field(
        ...,
        description="The predicted insurance premium category",
        json_schema_extra={"example": "High"}
    )
    confidence: float = Field(
        ...,
        description="Model's confidence score for the predicted class (range: 0 to 1)",
        json_schema_extra={"example": 0.8432}
    )
    class_probabilities: Dict[str, float] = Field(
        ...,
        description="Probability distribution across all possible classes",
        json_schema_extra={"example": {"Low": 0.01, "Medium": 0.15, "High": 0.84}}
    )

class ErrorDetail(BaseModel):
    code: str = Field(..., description="Machine-readable error code")
    message: str = Field(..., description="Human-readable error description")
    details: Optional[List[Dict[str, Any]]] = Field(None, description="Detailed validation breakdown")

class ErrorResponse(BaseModel):
    success: bool = Field(False, description="Operation success flag")
    error: ErrorDetail = Field(..., description="Error details object")