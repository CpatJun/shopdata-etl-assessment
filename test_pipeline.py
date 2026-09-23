import sqlite3
import pandas as pd

def test_pipeline_output():
    conn = sqlite3.connect('analytics.db')
    customers = pd.read_sql_query("SELECT * FROM dim_customers", conn)
    conn.close()

    assert customers['email'].isnull().sum() == 0, "ยังมีค่า NULL ใน email"
    assert (customers['email'] == '').sum() == 0, "ยังมีสตริงว่างใน email"
    
    non_empty_phones = customers['phone'][customers['phone'] != '']
    assert non_empty_phones.str.isdigit().all(), "เบอร์โทรศัพท์ยังมีอักขระที่ไม่ใช่ตัวเลข"

    print("All Tests Passed Successfully!")

if __name__ == '__main__':
    test_pipeline_output()