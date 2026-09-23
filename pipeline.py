import sqlite3
import pandas as pd
from prefect import task, flow

@task
def extract(db_path="shopdata.db"):
    conn = sqlite3.connect(db_path)
    cust = pd.read_sql_query("SELECT * FROM vw_raw_customers", conn)
    ordr = pd.read_sql_query("SELECT * FROM vw_raw_orders", conn)
    rate = pd.read_sql_query("SELECT * FROM vw_exchange_rates", conn)
    conn.close()
    return cust, ordr, rate

@task
def transform_customers(df):
    df = df.copy()
    df['email'] = df['email'].fillna('unknown@domain.com').replace('', 'unknown@domain.com')
    df['phone'] = df['phone'].fillna('').astype(str).str.replace(r'\D', '', regex=True)
    return df.sort_values('signup_date').drop_duplicates('full_name', keep='last')

@task
def transform_orders(orders, rates):
    df = orders[orders['total_amount'] > 0].copy()
    rates = rates.copy()
    
    # 1. แปลงวันที่ให้ตรงกัน
    df['order_date_str'] = pd.to_datetime(df['order_date']).dt.strftime('%Y-%m-%d')
    date_col = 'rate_date' if 'rate_date' in rates.columns else 'date'
    rates['rate_date_str'] = pd.to_datetime(rates[date_col]).dt.strftime('%Y-%m-%d')
    
    # 2. Merge ข้อมูล
    merged = pd.merge(
        df, rates,
        left_on=['order_date_str', 'currency'],
        right_on=['rate_date_str', 'currency'],
        how='left'
    )
    
    # 3. ระบุคอลัมน์เรทแลกเปลี่ยน
    possible_rate_cols = ['exchange_rate_to_usd', 'exchange_rate', 'rate']
    rate_col = next((c for c in possible_rate_cols if c in merged.columns), None)
    
    if rate_col:
        merged['rate_clean'] = pd.to_numeric(merged[rate_col], errors='coerce').fillna(1.0)
    else:
        merged['rate_clean'] = 1.0
        
    # ปัดทศนิยม 2 ตำแหน่ง ป้องกันปัญหา Floating Point Precision
    merged['usd_amount'] = (merged['total_amount'] * merged['rate_clean']).round(2)
    
    # 4. เลือกคืนเฉพาะคอลัมน์ดั้งเดิม + usd_amount
    clean_cols = [c for c in orders.columns] + ['usd_amount']
    return merged[clean_cols]

@task
def load(cust, ordr, db_path="analytics.db"):
    conn = sqlite3.connect(db_path)
    cust.to_sql('dim_customers', conn, if_exists='replace', index=False)
    ordr.to_sql('fct_orders', conn, if_exists='replace', index=False)
    conn.close()

@flow(name="ShopData ETL")
def etl_flow():
    cust, ordr, rate = extract()
    clean_cust = transform_customers(cust)
    clean_ordr = transform_orders(ordr, rate)
    load(clean_cust, clean_ordr)

if __name__ == '__main__':
    etl_flow()