from fastapi import APIRouter, HTTPException
from sympy import symbols, sympify, diff
from models.schemas import PartialDerivativeRequest

router = APIRouter()

@router.post("/partial-derivative")
def partial_derivative(req: PartialDerivativeRequest):
    try:
        symbols_dict = {v: symbols(v) for v in req.variables}
        expr = sympify(req.function, locals=symbols_dict)
        diff_expr = diff(expr, symbols_dict[req.respect_to])

        if req.at_point:
            subs_dict = {symbols_dict[k]: v for k, v in req.at_point.items()}
            numeric_result = diff_expr.evalf(subs=subs_dict)
            return {
                "partial_derivative": str(diff_expr),
                "value": round(float(numeric_result), 4),
                "at_point": req.at_point
            }
        else:
            return {
                "partial_derivative": str(diff_expr),
                "explanation": f"Partial derivative with respect to {req.respect_to}"
            }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))