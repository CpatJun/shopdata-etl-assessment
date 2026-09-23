import sqlite3
import re
import pandas as pd

def run_pipeline():
    conn_src = sqlite3.connect('shopdata.db')
    customers = pd.read_sql_query("SELECT * FROM vw_raw_customers",conn_src)
    orders = pd.read_sql_query("SELECT * FROM vw_raw_orders", conn_src)
    conn_src.close()

    customers['email'] = customers['email'].fillna('unknown@domain.com').replace('', 'unknown@domain.com')
    customers['phone'] = customers['phone'].fillna('').astype(str).str.replace(r'\D', '', regex=True)
    customers = customers.sort_values('signup_date').drop_duplicates('full_name', keep='last')
    
    conn_dest = sqlite3.connect('analytics.db')
    customers.to_sql('dim_customers', conn_dest, if_exists='replace', index=False)
    orders.to_sql('fact_orders', conn_dest, if_exists='replace', index=False)
    conn_dest.close()
    print("Done!")

if __name__ == '__main__':
    run_pipeline()