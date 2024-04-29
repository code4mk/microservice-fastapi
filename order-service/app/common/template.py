from fastapi import Request
from fastapi.templating import Jinja2Templates
from app.utils.base import app_path
from app.utils.mailer.mail_templating import EmailTemplates


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
    templates = Jinja2Templates(directory=app_path('templates'))
    return templates.TemplateResponse(template_name, {"request": request, **context})

def render_mail_template(template_name: str, context: dict = {}):
  templates = EmailTemplates(directory=app_path('templates/mails'))
  return templates.render_template(template_name, context)