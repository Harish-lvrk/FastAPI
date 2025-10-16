from fastapi import FastAPI,Request,Path, HTTPException, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import json 
import uvicorn

app = FastAPI()

def load_data():
    with open('patients.json','r') as f:
        data = json.load(f)
    return data


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



@app.get('/view')
def view():
    return load_data()


@app.get('/patient/{patient_id}')
def view_patient(patient_id: str = Path(...,description='Id of the patient in  the DB',example='P001')):
    data = load_data()

    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail="patient not found")

@app.get('/sort')
def sort_patients(sort_by: str = Query(...,description='sort on the basis of height , weight and bmi'),sort_order: str = Query('asc',description='sort in asc or desc order')):

    valid_fields = ['height','weight','bmi']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400,detail=f'Invalid field select from {valid_fields}')
    
    if sort_order not in ['asc','desc']:
        raise HTTPException(status_code=400,detail=f'Invalid sort order select between asc or desc')
    
    data = load_data()
    
    order = True if sort_order=='desc' else False

   
    sorted_data = sorted(data.values(),key = lambda x:x.get(sort_by,0),reverse=order) 
    """If 'age' does NOT exist, use 0 as the default value.
                    So 0 here prevents errors like KeyError if 'age' is missing, and ensures those entries are treated as having age 0."""
    return sorted_data




# Run the application with automatic reloading for development
if __name__ == "__main__":
    uvicorn.run(
        "main:app",  # The import string "module_name:app_instance_name"
        host="127.0.0.1",
        port=8000,
        reload=True  # Enables the auto-reload feature
    )
