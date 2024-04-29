from fastapi import Request
from fastapi.templating import Jinja2Templates
from app.utils.base import app_path

templates = Jinja2Templates(directory=app_path('templates'))

def render_template(template_name: str, request: Request, context: dict = {}):
    """
    Render a Jinja2 template with the given context.

    Args:
        template_name (str): The name of the template file.
        request (Request): The FastAPI request object.
        context (dict, optional): The context data to pass to the template. Defaults to {}.

    Returns:
        TemplateResponse: The rendered template response.
    """
    return templates.TemplateResponse(template_name, {"request": request, **context})
