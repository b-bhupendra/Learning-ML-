import streamlit as st
from datetime import datetime
import requests
import pandas as pd
API_URL = "http://localhost:8000"

def analytics_th():
    col1 = st.columns(1)[0] # without it they are stacked up to down
    with col1:
        current_year = datetime.now().year
        selected_year = st.number_input("Select Year", min_value=2000, max_value=2100, value=current_year)
    
        payload = {
            "year" : selected_year
        }

        response = requests.post(f"{API_URL}/analytics/2",json=payload)
        response = response.json()
        st.write(response)

        d = { "month" : [ list(m.keys())[0] for m in response],
                "total" : [ m['total'] for m in response]
            }
        df = pd.DataFrame(d).set_index("month")
        
        # df_sorted = df.set_index("Months")
        
        st.title("Expense Breakdown By Category")
        st.bar_chart(data=df)
        st.table(df)
        
         