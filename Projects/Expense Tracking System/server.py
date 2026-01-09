from fastapi import FastAPI, HTTPException
from datetime import date
import logging

from typing import List
from pydantic import BaseModel


from backend import db_helper

"""log config"""
 

class Expense(BaseModel):
    amount : float
    category : str
    notes : str

class DateRange(BaseModel):
    start_date : date
    end_date : date

class Year(BaseModel):
    year: int

app = FastAPI()

@app.get("/" )
def hello():
    return "hello"

@app.get("/expenses/{expense_date}", response_model=List[Expense])
def get_expenses(expense_date : date):
    expenses = db_helper.fetch_expenses_for_date(expense_date)
    return expenses


@app.post("/expenses/{expense_date}")
def add_or_update_expense(expense_date : date , expenses:List[Expense] ):
    db_helper.delete_expenses_for_date(expense_date)
    for expense in expenses:
        db_helper.insert_expense(expense_date , expense.amount, expense.category,expense.notes)
    return {"message" : "Expenses Updated Successfully"}

@app.post("/analytics")
def get_analytics(date_range : DateRange ):
    data = db_helper.fetch_expense_summary(date_range.start_date,date_range.end_date)
    
    if data is None:
        raise HTTPException(status_code=500, detail="Failed to retrieve expense summary from database")
    total = 0
    
    total = sum([float(row['total']) for row in data]) # type: ignore

    breakdown = {}

    for row in data:
        percentage = (row['total']/ total) * 100 if total != 0 else 0 # type: ignore
        breakdown[row["category"]] = { # type: ignore
            "total" : row['total'],# type: ignore
            "percentage" :percentage
        }
   
    return breakdown


@app.post("/analytics/2")
def get_analytics_two(yr : Year ):
    
    year = int(yr.year)
    
    data = db_helper.get_monthly_expense(year)

    if data is None:
        raise HTTPException(status_code=500, detail="Failed to retrieve {Year}'s Monthly summary from database")
    
    n_data = {}

    for row in data:  # type: ignore
        n_data[row['mon']] = row['total'] # type: ignore
    
    # year = 2024
    # Generates the 1st of every month
    months = [ [ date(year, m, 1).strftime('%B'), m] for m in range(1, 13)]
    # strs = []
    n_data_final = []
    for month, m in months:

        if m in n_data:
            n_data_final.append({month: month, 'total' : n_data[m]})
        else:
            n_data_final.append({month: month , 'total' : 0 })
        
    return n_data_final

