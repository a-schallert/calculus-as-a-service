from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers import optimize, derivative, integration, critical, plot, partial, gradient, rate_of_change
import os

app = FastAPI()

# Static file route for plots
os.makedirs("plots", exist_ok=True)
app.mount("/plots", StaticFiles(directory="plots"), name="plots")

# Include routers
app.include_router(optimize.router)
app.include_router(derivative.router)
app.include_router(integration.router)
app.include_router(critical.router)
app.include_router(plot.router)
app.include_router(partial.router)
app.include_router(gradient.router)
app.include_router(rate_of_change.router)