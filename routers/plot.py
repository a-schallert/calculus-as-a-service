from fastapi import APIRouter, HTTPException
from sympy import symbols, sympify, lambdify
from models.schemas import PlotRequest
import numpy as np
import matplotlib.pyplot as plt
import uuid
import os

router = APIRouter()

@router.post("/plot")
def plot_function(req: PlotRequest):
    try:
        x = symbols(req.variable)
        expr = sympify(req.function)
        f_lambdified = lambdify(x, expr, 'numpy')

        x_vals = np.linspace(req.range[0], req.range[1], 400)
        y_vals = f_lambdified(x_vals)

        plt.figure()
        plt.plot(x_vals, y_vals, label=f"f({req.variable})")
        plt.xlabel(req.variable)
        plt.ylabel("f(x)")
        plt.title("Function Plot")
        plt.grid(True)
        plt.legend()

        filename = f"plot_{uuid.uuid4().hex}.png"
        filepath = os.path.join("plots", filename)
        os.makedirs("plots", exist_ok=True)
        plt.savefig(filepath)
        plt.close()

        return {
            "filename": filename,
            "url": f"/plots/{filename}",
            "explanation": "Plot image saved and accessible via URL."
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))