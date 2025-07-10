from fastapi import APIRouter, HTTPException
from sympy import symbols, sympify, diff, lambdify
from models.schemas import RateOfChangeRequest

router = APIRouter()

@router.post("/rate-of-change")
def rate_of_change(req: RateOfChangeRequest):
    try:
        x = symbols(req.variable)
        expr = sympify(req.function)

        first_derivative = diff(expr, x)
        second_derivative = diff(first_derivative, x)

        f_prime = lambdify(x, first_derivative, 'numpy')
        f_double_prime = lambdify(x, second_derivative, 'numpy')

        rate = f_prime(req.at_point)
        acceleration = f_double_prime(req.at_point)

        explanation = f"At {req.variable} = {req.at_point}, the rate of change is {round(rate, 4)} and the acceleration is {round(acceleration, 4)}."
        if req.context:
            explanation += f" This may represent the rate of change of {req.context}."

        return {
            "rate_of_change": round(float(rate), 4),
            "acceleration": round(float(acceleration), 4),
            "at_point": req.at_point,
            "expression": {
                "first_derivative": str(first_derivative),
                "second_derivative": str(second_derivative)
            },
            "explanation": explanation
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))