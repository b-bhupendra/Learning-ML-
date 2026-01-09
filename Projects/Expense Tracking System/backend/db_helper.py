import mysql.connector
from contextlib import contextmanager
import os
import sys

from backend.logging_setup import setup_logger

logger = setup_logger('db_helper',"server.log")



@contextmanager
def get_db_cursor(commit=False):
    connection = mysql.connector.connect(
        host="localhost",
        user="admin",
        password="",
        database="expense_manager"
    )

    cursor = connection.cursor(dictionary=True)
    yield cursor
    if commit:
        connection.commit()
    print("Closing cursor")
    cursor.close()
    connection.close()


def fetch_all_records():
    query = "SELECT * from expenses"

    with get_db_cursor() as cursor:
        cursor.execute(query)
        expenses = cursor.fetchall()
        for expense in expenses:
            print(expense)
   

def fetch_expenses_for_date(expense_date):
    logger.info(f"fetch_expenses_for_data called with {expense_date}")
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM expenses WHERE expense_date = %s", (expense_date,))
        expenses = cursor.fetchall()
        # for expense in expenses:
        #     print(expense)
        return expenses

def insert_expense(expense_date, amount, category, notes):
    logger.info(f"Insert_expense with {expense_date} {amount} {category} {notes}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            "INSERT INTO expenses (expense_date, amount, category, notes) VALUES (%s, %s, %s, %s)",
            (expense_date, amount, category, notes)
        ) 


def delete_expenses_for_date(expense_date):
    logger.info(f"fetch_expenses_for_data called with {expense_date}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("DELETE FROM expenses WHERE expense_date = %s", (expense_date,))

def fetch_expense_summary(start_date, end_date):
    logger.info(f"fetch_expense_summary called with start: {start_date} , end: {end_date}")
    with get_db_cursor() as cursor:
        cursor.execute(
            """
              SELECT category, SUM(amount) as total
              FROM expenses WHERE expense_date 
              BETWEEN %s AND %s
              GROUP BY category;
            """ , (start_date , end_date)
        )
        data = cursor.fetchall()
        
        return data

def get_monthly_expense(year):
    year = int(year)
    logger.info(f" Monthly Expense of year : {year}")
    with get_db_cursor() as cursor:
        cursor.execute(
            """
            SELECT extract(YEAR from expense_date) as yr, extract(MONTH from expense_date) as mon, sum(amount) total
            FROM expenses 
            WHERE extract(YEAR from expense_date) = %s
            GROUP BY extract(YEAR from expense_date), extract(MONTH from expense_date);
            """ , (year ,)
        )
        data = cursor.fetchall()
        
        return data

if __name__ == "__main__":
    # fetch_all_records()
    # fetch_expenses_for_date("2024-08-01")
    # insert_expense("2024-08-20", 300, "Food", "Panipuri")
    # delete_expenses_for_date("2024-08-20")
    # fetch_expenses_for_date("2024-08-20")
    # fetch_all_records()
    project_root = os.path.join(os.path.dirname(__file__) , '..')

    print(f"Project Root Path : {project_root}")
    sys.path.insert(0, project_root)
    summary = fetch_expense_summary("2024-08-01","2024-08-05")
  
    for record in summary:
        print(record)
        