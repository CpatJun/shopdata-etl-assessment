-- ชุดที่ 1: เช็กข้อมูลลูกค้าซ้ำ
SELECT full_name, count(*) as count
FROM vw_raw_customers
GROUP BY full_name
HAVING count > 1;

-- ชุดที่ 2: เช็กเบอร์และอีเมลแปลกปลอม/ค่าว่าง
SELECT *
FROM vw_raw_customers
WHERE email ISNULL OR phone LIKE '%-%' OR phone LIKE '%(%';

-- ชุดที่ 3: เช็กยอดสั่งซื้อติดลบ หรือ 0
SELECT *
FROM vw_raw_orders
WHERE total_amount <= 0 OR currency ISNULL;