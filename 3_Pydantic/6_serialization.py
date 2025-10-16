from pydantic import BaseModel

class Address(BaseModel):

    city: str
    state: str
    pin: str

class Patient(BaseModel):

    name: str
    gender: str = 'Male'
    age: int
    address: Address

address_dict = {'city': 'gurgaon', 'state': 'haryana', 'pin': '122001'}

address1 = Address(**address_dict)

patient_dict = {'name': 'nitish', 'age': 35, 'address': address1}

patient1 = Patient(**patient_dict)

temp = patient1.model_dump(exclude_unset=True) # include = ['name'] only name we get and exclue also works
# exclude_unset True do if we are not specifyin the during the creation default values are assigned thos default assignedd properties
# are not returned
temp2 = patient1.model_dump_json()

print(temp)
print(type(temp))

print(temp2)
