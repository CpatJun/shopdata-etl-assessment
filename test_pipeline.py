import pandas as pd
from pipeline import transform_customers, transform_orders

def test_transform_customers():
    raw_data = pd.DataFrame({
        'customer_id': [1, 2, 3],
        'full_name': ['Alice', 'Bob', 'Alice'],
        'email': [None, '', 'alice@example.com'],
        'phone': ['+1 (555) 019-2831', '123-456-7890', '5550192831'],
        'signup_date': ['2023-01-01', '2023-01-02', '2023-01-05']
    })
    
    result = transform_customers.fn(raw_data)
    
    # 1. Email NULL/ว่าง ต้องแปลงเป็น unknown@domain.com
    assert result.loc[result['full_name'] == 'Bob', 'email'].values[0] == 'unknown@domain.com'
    
    # 2. Phone ต้องเหลือเฉพาะตัวเลข
    assert result['phone'].str.isdigit().all()
    
    # 3. Deduplicate ต้องเหลือ Alice แค่รายการล่าสุด
    assert len(result) == 2
    assert result.loc[result['full_name'] == 'Alice', 'signup_date'].values[0] == '2023-01-05'

def test_transform_orders():
    raw_orders = pd.DataFrame({
        'order_id': [101, 102, 103],
        'order_date': ['2023-01-01', '2023-01-01', '2023-01-02'],
        'total_amount': [100.0, -50.0, 200.0],
        'currency': ['EUR', 'USD', 'USD']
    })
    
    raw_rates = pd.DataFrame({
        'rate_date': ['2023-01-01'],
        'currency': ['EUR'],
        'exchange_rate_to_usd': [1.1]
    })
    
    result = transform_orders.fn(raw_orders, raw_rates)
    
    # 1. กรอง order ที่ติดลบออก (ต้องเหลือ 2 รายการ)
    assert len(result) == 2
    assert (result['total_amount'] > 0).all()
    
    # 2. คำนวณ USD ถูกต้อง (100 EUR * 1.1 = 110 USD)
    eur_order = result[result['order_id'] == 101]
    assert eur_order['usd_amount'].values[0] == 110.0