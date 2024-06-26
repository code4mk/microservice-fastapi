from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import OperationalError
from app.utils.database import engine
from sqlalchemy import select

# Create a FastAPI app
router = APIRouter()

# Health check route
@router.get("/")
async def health_check():
    try:
        # Build a select statement to check database connectivity
        stmt = select(1)
        # Execute the query
        with engine.connect() as connection:
            result = connection.execute(stmt)
            result.fetchone()  # Ensure there is at least one row returned
        data =  {"status": "ok"}
        return JSONResponse(content=data, status_code=status.HTTP_200_OK)
    except OperationalError:
        # If there's an error connecting to the database, raise HTTP 503 Service Unavailable
        raise HTTPException(status_code=503, detail="Database connection failed")