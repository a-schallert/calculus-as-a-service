from fastapi import APIRouter, HTTPException
from sympy import symbols, sympify, integrate
from models.schemas import IntegrationRequest

router = APIRouter()

@router.post("/integrate")
def integrate_function(req: IntegrationRequest):
    try:
        x = symbols(req.variable)
        expr = sympify(req.function)

        if req.lower_bound is not None and req.upper_bound is not None:
            result = integrate(expr, (x, req.lower_bound, req.upper_bound))
            explanation = f"Definite integral of the function from {req.lower_bound} to {req.upper_bound}"
        else:
            result = integrate(expr, x)
            explanation = f"Indefinite integral of the function"

        return {
            "result": float(result) if result.is_real else str(result),
            "expression": str(result),
            "explanation": explanation
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))