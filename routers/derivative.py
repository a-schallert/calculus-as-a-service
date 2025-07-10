from fastapi import APIRouter, HTTPException
from sympy import symbols, sympify, diff, lambdify
from models.schemas import DerivativeRequest

router = APIRouter()

@router.post("/derivative")
def derivative(req: DerivativeRequest):
    try:
        x = symbols(req.variable)
        expr = sympify(req.function)
        deriv = diff(expr, x, req.order)

        if req.at_point is not None:
            f_lambdified = lambdify(x, deriv, 'numpy')
            value = f_lambdified(req.at_point)
            return {
                "derivative_order": req.order,
                "value": round(float(value), 4),
                "at_point": req.at_point,
                "expression": str(deriv),
                "explanation": f"The {req.order}-order derivative at {req.variable} = {req.at_point} is approximately {round(float(value), 4)}"
            }
        else:
            return {
                "derivative_order": req.order,
                "expression": str(deriv),
                "explanation": f"Symbolic derivative of order {req.order}"
            }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
