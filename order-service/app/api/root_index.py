from fastapi import APIRouter, status, Request
from fastapi.responses import JSONResponse
from app.common.template import render_template, render_mail_template
from app.utils.mailer.mail import send_mail

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
        context = {
            "user": "John Doe kamal",
            "activation_link": "http://example.com/activate"
        }

        # Render the email template
        rendered_email = render_mail_template("welcome_email.html", context)
        print(rendered_email)
        
        try:
            print(0)
        except print(0):
            pass
        
        
        data = {
            'message': 'project is running'
        }
        return JSONResponse(content=data, status_code=status.HTTP_200_OK)
    
@router.get("/mail")
async def mail(request: Request):
        context = {
            "user": "John Doe kamal",
            "activation_link": "http://example.com/activate"
        }

        rendered_email = render_mail_template("welcome_email.html", context)
        
        try:
            a = await send_mail('this is fastapi micro service',['mostafa@kintaro.io'] ,'welcome_email.html', context) 
            print(a)
        except Exception as e:
            print(str(e))
            
        
        data = {
            'data1': rendered_email
        }
        return JSONResponse(content=data, status_code=status.HTTP_200_OK)