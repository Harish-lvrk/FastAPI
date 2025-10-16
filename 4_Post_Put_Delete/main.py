from fastapi import FastAPI,Request,Path, HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import json 
import uvicorn
from pydantic import BaseModel,Field,computed_field
from typing import Annotated,Literal,Optional
app = FastAPI()

class Patient(BaseModel):
    id : Annotated[str,Field(...,description="Id of the patient",examples=['P001'])]
    name : Annotated[str,Field(...,description="Name of the patient")]
    city : Annotated[str,Field(...,description="City where the patient is living")]
    age : Annotated[int,Field(...,gt=0,lt=120,description="Enter the age of the patient")]
    gender : Annotated[Literal['male','female','others'],Field(...,description="gender of the patient")]
    height : Annotated[float,Field(...,gt=0,description='Height of the patient')]
    weight : Annotated[float,Field(...,gt=0,description="Weight of the patient")] 
    

    @computed_field
    @property
    def bmi(self)->float:
        bmi = round(self.weight/(self.height**2))
        return bmi
    
    @computed_field
    @property
    def verdict(self)->str:
        if self.bmi < 18.5:
            return "Underweight"
        elif self.bmi <30:
            return "Normal"
        else:
            return "Obese"
class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0)]
    gender: Annotated[Optional[Literal['male', 'female']], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]
    



def load_data():
    with open('4_Post_Put_Delete/patients.json','r') as f:
        data = json.load(f)
    return data

def save_data(data):
    with open('4_Post_Put_Delete/patients.json','w') as f:
        json.dump(data,f)





@app.get('/')
def hello():
    return {'message':'hellow world'}


# Initialize Jinja2Templates, pointing to your templates directory
templates = Jinja2Templates(directory="4_Post/templates")

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

@app.post('/create')
def create_patient(patient: Patient):

    # load exissting data
    data = load_data()

    # check if the patient is already exist

    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient is already exist")

    # if new patient add to the dataset

    data[patient.id] = patient.model_dump(exclude=['id'])

    save_data(data)

    return JSONResponse(status_code=201,content={'message':"Patient Created successfully"})

@app.put('/edit/{patient_id}')
def update_patient(patient_id:str,patient_update: PatientUpdate):

    existing_patient_info = view_patient(patient_id=patient_id)

    update_patient_info = patient_update.model_dump(exclude_unset=True)

    for key,Value in update_patient_info.items():
        existing_patient_info[key] = Value

    # existing_patient_info -> pydanticobject -> updateedbmi + verdict

    existing_patient_info['id'] = patient_id
    patient_pydantic_obj = Patient(**existing_patient_info)

    # -> pydantic object -> dict

    existing_patient_info = patient_pydantic_obj.model_dump(exclude='id')

    #load  the data
    data = load_data()
    #save the disct to the data
    data[patient_id] = existing_patient_info
    save_data(data)

    return JSONResponse(status_code=200, content={'message': 'patient updated'})



@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):
    
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404,detail="Patient not found")
    
    del data[patient_id]

    save_data(data=data)

    return JSONResponse(status_code=200, content={"message": "patient deleted"})













# Run the application with automatic reloading for development
if __name__ == "__main__":
    uvicorn.run(
        "main:app",  # The import string "module_name:app_instance_name"
        host="127.0.0.1",
        port=8000,
        reload=True  # Enables the auto-reload feature
    )
