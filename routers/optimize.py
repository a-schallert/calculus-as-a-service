from fastapi import APIRouter, HTTPException
from sympy import symbols, sympify, diff, solveset, S, lambdify
import numpy as np
from models.schemas import OptimizationRequest

router = APIRouter()

@router.post("/optimize")
def optimize(req: OptimizationRequest):
    try:
        x = symbols(req.variable)
        expr = sympify(req.function)
        derivative = diff(expr, x)
        critical_points = solveset(derivative, x)

        domain_min, domain_max = req.domain
        real_points = [pt.evalf() for pt in critical_points if pt.is_real and domain_min <= pt.evalf() <= domain_max]
        real_points += [domain_min, domain_max]

        f_lambdified = lambdify(x, expr, 'numpy')
        values = [(pt, f_lambdified(float(pt))) for pt in real_points]

        max_point, max_value = max(values, key=lambda item: item[1])

        return {
            "max_value": round(float(max_value), 4),
            "at_x": round(float(max_point), 4),
            "explanation": f"Maximum value of {round(float(max_value), 4)} occurs at {req.variable} = {round(float(max_point), 4)}"
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
