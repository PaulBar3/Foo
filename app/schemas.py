from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional



class ExpenseAddSchema(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    amount: float = Field(gt=0)
    comment: str 
    

    

class ExpenseSchema(ExpenseAddSchema):
    id: int 
    created_at: datetime = datetime.now()

    

class ExpenseUpdateSchema(ExpenseSchema):
    pass