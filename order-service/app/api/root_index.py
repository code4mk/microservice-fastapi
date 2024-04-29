from fastapi import APIRouter, status, Request
from fastapi.responses import JSONResponse
from app.common.template import render_template

# Create a FastAPI app
router = APIRouter()

# Health check route
@router.get("/")
async def root_index(request: Request):
    is_html = request.query_params.get('is_html')
    
    if is_html == 'yes':
        context = {"message": 'project is running'}
        return render_template("user.html", request, context)
    else:
        data = {
            'message': 'project is running'
        }
        return JSONResponse(content=data, status_code=status.HTTP_200_OK)