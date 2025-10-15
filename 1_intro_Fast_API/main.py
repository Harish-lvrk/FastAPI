from fastapi import FastAPI,Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

# End point
@app.get('/')
def hello():
    return {'message':'hellow world'}


# Initialize Jinja2Templates, pointing to your templates directory
templates = Jinja2Templates(directory="templates")

@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    # Define context data to pass to the template
    context = {"request": request, "name": "Hareesh"}
    # Render the template and return it as an HTMLResponse
    return templates.TemplateResponse("index.html", context)
