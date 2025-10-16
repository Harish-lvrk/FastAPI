from pydantic import BaseModel, EmailStr, AnyUrl, Field # use to do the type validation and data validation 
from typing import List, Dict, Optional, Annotated # it is used to check the type within the type also

class Patient(BaseModel):

    name: Annotated[str, Field(max_length=50, title='Name of the patient', description='Give the name of the patient in less than 50 chars', examples=['vamsi', 'Hareesh'])]
    email: EmailStr
    linkedin_url: AnyUrl
    age: int = Field(gt=0, lt=120) # here we doing the data validation and type checking also
    weight: Annotated[float, Field(gt=0, strict=True)]
    married: Annotated[bool, Field(default=None, description='Is the patient married or not')]
    allergies: Annotated[Optional[List[str]], Field(default=None, max_length=5)] 
    contact_details: Dict[str, str]


def update_patient_data(patient: Patient):

    print(patient.name)
    print(patient.age)
    print(patient.allergies)
    print(patient.married)
    print('updated')

patient_info = {'name':'Hareesh', 'email':'abc@gmail.com', 'linkedin_url':'http://linkedin.com/1322', 'age': '21', 'weight': 57,'contact_details':{'phone':'2353462'}}

patient1 = Patient(**patient_info)

update_patient_data(patient1)

print(patient1)
