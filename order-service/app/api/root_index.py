from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

# Create a FastAPI app
router = APIRouter()

# Health check route
@router.get("/")
async def root_index():
    data = {
        'message': 'project is running'
    }
    return JSONResponse(content=data, status_code=status.HTTP_200_OK)