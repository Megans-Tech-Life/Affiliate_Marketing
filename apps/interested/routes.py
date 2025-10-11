# Interested lead routes will be implemented here
# TODO: Add FastAPI routes for interested lead management

from fastapi import APIRouter

router = APIRouter(prefix="/interested", tags=["Interested"])

# TODO: Implement the following endpoints:
# - GET / (list all interested leads)
# - POST / (mark a lead as interested)
# - GET /{interested_id} (get specific interested lead)
# - PUT /{interested_id} (update interest level/notes)
# - DELETE /{interested_id} (remove interest status)