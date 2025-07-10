from pydantic import BaseModel
from typing import Optional, List, Dict

class OptimizationRequest(BaseModel):
    function: str
    variable: str
    domain: List[float]

class DerivativeRequest(BaseModel):
    function: str
    variable: str
    order: int = 1
    at_point: Optional[float] = None

class RateOfChangeRequest(BaseModel):
    function: str
    variable: str
    at_point: float
    context: Optional[str] = None

class IntegrationRequest(BaseModel):
    function: str
    variable: str
    lower_bound: Optional[float] = None
    upper_bound: Optional[float] = None

class CriticalPointsRequest(BaseModel):
    function: str
    variable: str

class PlotRequest(BaseModel):
    function: str
    variable: str
    range: List[float]

class PartialDerivativeRequest(BaseModel):
    function: str
    variables: List[str]
    respect_to: str
    at_point: Optional[Dict[str, float]] = None

class GradientRequest(BaseModel):
    function: str
    variables: List[str]
    at_point: Optional[Dict[str, float]] = None
