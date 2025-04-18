from fastapi import FastAPI
from routes.dotalyzer_route import router as dotalyzer_router

def create_app():
  app = FastAPI()

  # Routers
  app.include_router(dotalyzer_router)

  return app
