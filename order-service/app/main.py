from fastapi import FastAPI
from app.api.v1 import order
from app.api import health, root_index
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

# Load .env file
load_dotenv()

def create_application():
    application = FastAPI()
    
    # Include routers
    application.include_router(root_index.router)
    application.include_router(health.router, prefix='/health')
    application.include_router(order.router, prefix="/api/v1")
    
    
    # Allow all origins (not recommended for production)
    # Replace the "*" with the actual frontend URL in production
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Replace ["*"] with your frontend URL in production
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=["*"],
    )
    
    return application

app = create_application()