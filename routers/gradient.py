from fastapi import APIRouter, HTTPException
from sympy import symbols, sympify, diff
from models.schemas import GradientRequest

router = APIRouter()

@router.post("/gradient")
def gradient(req: GradientRequest):
    try:
        symbols_dict = {v: symbols(v) for v in req.variables}
        expr = sympify(req.function, locals=symbols_dict)
        vars_syms = [symbols_dict[v] for v in req.variables]
        grad_vector = [diff(expr, v) for v in vars_syms]

        if req.at_point:
            subs_dict = {symbols_dict[k]: v for k, v in req.at_point.items()}
            evaluated = [float(g.evalf(subs=subs_dict)) for g in grad_vector]
            return {
                "gradient": [str(g) for g in grad_vector],
                "value": [round(v, 4) for v in evaluated],
                "at_point": req.at_point
            }
        else:
            return {
                "gradient": [str(g) for g in grad_vector],
                "explanation": "Gradient vector of the function"
            }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))