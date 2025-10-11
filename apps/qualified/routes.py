# Qualified lead routes will be implemented here
# TODO: Add FastAPI routes for qualified lead management

from fastapi import APIRouter

router = APIRouter(prefix="/qualified", tags=["Qualified"])

# TODO: Implement the following endpoints:
# - GET / (list all qualified leads)
# - POST / (create/qualify a lead)
# - GET /{qualified_id} (get specific qualified lead)
# - PUT /{qualified_id} (update qualification)
# - DELETE /{qualified_id} (remove qualification)