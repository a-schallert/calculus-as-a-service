from fastapi import APIRouter, HTTPException
from sympy import symbols, sympify, diff, solve
from models.schemas import CriticalPointsRequest

router = APIRouter()

@router.post("/critical-points")
def critical_points(req: CriticalPointsRequest):
    try:
        x = symbols(req.variable)
        expr = sympify(req.function)

        first_derivative = diff(expr, x)
        second_derivative = diff(first_derivative, x)

        critical_pts = solve(first_derivative, x)

        results = []
        for pt in critical_pts:
            concavity = second_derivative.subs(x, pt).evalf()
            classification = "minimum" if concavity > 0 else "maximum" if concavity < 0 else "saddle point"
            results.append({
                "point": float(pt.evalf()),
                "classification": classification,
                "f'": str(first_derivative),
                "f''": str(second_derivative)
            })

        return {
            "critical_points": results,
            "explanation": "Points where the first derivative is zero, classified using the second derivative test."
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
