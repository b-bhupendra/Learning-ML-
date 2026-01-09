from fastapi import FastAPI
import db_helper
from typing import List
from pydantic import BaseModel

class Expense(BaseModel):
    amount : float
    category : str
    notes : str

class DateRange(BaseModel):
    amount :float
    category : str
    notes : str

