# backend/app/routes/__init__.py
from fastapi import APIRouter
# Assuming you have a file named 'analysis.py' inside 'routes/'
from app.routes.analyze import router 

# If you don't have analysis.py yet, just create an empty router for now:
# router = APIRouter()