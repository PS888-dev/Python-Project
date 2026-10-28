from datetime import date  # ใช้ดึงวันที่ปัจจุบัน

Sales_file = "sales.txt"  # ชื่อไฟล์เก็บข้อมูลการขาย (ไฟล์สต็อกส่งมาจาก main.py)


# ---------------------------------------------------------------
# เมนู 1 : เพิ่มสินค้าเข้าสต็อก
# ---------------------------------------------------------------
def add_product(stock):
    today = date.today().isoformat()  # วันที่วันนี้ รูปแบบ YYYY-MM-DD
    # ถ้าผู้ใช้กด Enter เฉยๆ (ค่าว่าง) จะใช้วันที่วันนี้แทน
    day = input(f"Input date (YYYY-MM-DD, Enter = {today}) : ") or today
    name = input("Input product name : ")
    try:
        price = float(input("Input product price : "))  # ราคาเป็นทศนิยม
        qty = int(input("Input product quantity : "))   # จำนวนเป็นจำนวนเต็ม
    except ValueError:
        # ถ้าพิมพ์ตัวอักษรแทนตัวเลข จะแจ้งเตือนแล้วออกจากฟังก์ชัน
        print("Price and quantity must be numbers.\n")
        return

    # เปิดไฟล์โหมด "a" (append) เพื่อเขียนต่อท้าย ข้อมูลเก่าไม่หาย
    with open(stock, "a", encoding="UTF_8") as f:
        f.write("\n" + f"{day},{name},{price},{qty}")
    # :, คือใส่คอมมาคั่นหลักพัน  :.2f คือทศนิยม 2 ตำแหน่ง
    print(f"Saved: {name} x {qty:,} = {price * qty:,.2f} baht on {day}\n")


# ---------------------------------------------------------------
# เมนู 2 : แสดงรายงานสินค้าทั้งหมดในสต็อก
# ---------------------------------------------------------------
def show_product(stock):
    try:
        qty_sum = {}   # เก็บจำนวนรวม key = (วันที่, ชื่อ)
        price_of = {}  # เก็บราคา key = (วันที่, ชื่อ)
        with open(stock, "r", encoding="UTF_8") as f:
            for row in f:
                parts = row.strip().split(",")  # แยกบรรทัดด้วยคอมมา
                if len(parts) != 4:
                    continue  # ข้ามบรรทัดที่ข้อมูลไม่ครบ 4 ช่อง (เช่น บรรทัดว่าง)
                day, name, price, qty = parts
                key = (day, name)
                # สินค้าวันที่และชื่อเดียวกัน ให้บวกจำนวนรวมกัน
                qty_sum[key] = qty_sum.get(key, 0) + int(qty)
                price_of[key] = float(price)

        # พิมพ์หัวตาราง  :^ = จัดกึ่งกลาง  :< = ชิดซ้าย  :> = ชิดขวา
        line = "=" * 78
        print(f"{line}\n|{'Current Products':^76}|")
        print(f"{line}\n| {'Date':<10} | {'Name':<20} | {'Price per piece':>15} | {'Qty':>6} | {'Total price':>11} |\n{line}")
        # sorted เรียงตามวันที่ แล้วตามชื่อสินค้า
        for (day, name), qty in sorted(qty_sum.items()):
            price = price_of[(day, name)]
            print(f"| {day:<10} | {name:<20} | {price:>15,.2f} | {qty:>6,} | {price * qty:>11,.2f} |")
        print(line + "\n")
    except FileNotFoundError:
        # ยังไม่มีไฟล์สต็อก = ยังไม่เคยเพิ่มสินค้า
        print("No product data found. Please input product first.\n")


# ---------------------------------------------------------------
# เมนู 3 : บันทึกการขาย (ตรวจสต็อกคงเหลือก่อนขาย)
# ---------------------------------------------------------------
def Sales(stock):
    # 1) อ่านสต็อก: ชื่อ(ตัวเล็ก) -> [ชื่อจริง, ราคา, จำนวนคงเหลือ]
    items = {}
    try:
        with open(stock, "r", encoding="UTF_8") as f:
            for row in f:
                p = row.strip().split(",")
                if len(p) == 4:
                    # setdefault = ถ้ายังไม่มีสินค้านี้ให้สร้างใหม่ ถ้ามีแล้วใช้ของเดิม
                    item = items.setdefault(p[1].lower(), [p[1], 0, 0])
                    item[1] = float(p[2])  # ราคาล่าสุด
                    item[2] += int(p[3])   # บวกจำนวนที่เพิ่มเข้ามา
    except FileNotFoundError:
        pass  # ไม่มีไฟล์ก็ปล่อยผ่าน แล้วไปแจ้งเตือนด้านล่าง

    if not items:
        print("No product in stock. Please input product first.\n")
        return

    # 2) หักยอดที่ขายไปแล้วออกจากสต็อก (ได้จำนวนคงเหลือจริง)
    try:
        with open(Sales_file, "r", encoding="UTF_8") as f:
            for row in f:
                p = row.strip().split(",")
                if len(p) == 4 and p[1].lower() in items:
                    items[p[1].lower()][2] -= int(p[3])
    except FileNotFoundError:
        pass  # ยังไม่เคยขาย ก็ไม่ต้องหัก

    # 3) รับข้อมูลการขาย
    today = date.today().isoformat()
    day = input(f"Input sale date (YYYY-MM-DD, Enter = {today}) : ") or today

    cart = []  # ตะกร้า เก็บรายการที่ขายในรอบนี้ (ชื่อ, ราคา, จำนวน)
    while True:
        # lower() ทำให้พิมพ์ Pork หรือ pork ก็ถือว่าเป็นสินค้าเดียวกัน
        name = input("Input product name (Enter = finish) : ").strip().lower()
        if not name:
            break  # กด Enter เฉยๆ = จบการขาย
        if name not in items:
            print("Product not found.\n")
            continue

        real_name, price, left = items[name]
        print(f"  Price {price:,.2f} baht | In stock: {left:,}")
        if left <= 0:
            print("  Out of stock.\n")  # สินค้าหมด
            continue

        try:
            qty = int(input("Input quantity : "))
        except ValueError:
            print("Quantity must be a number.\n")
            continue
        if not 1 <= qty <= left:
            # ต้องขายอย่างน้อย 1 และไม่เกินจำนวนคงเหลือ
            print(f"Quantity must be between 1 and {left:,}.\n")
            continue

        items[name][2] -= qty  # หักสต็อกในหน่วยความจำทันที (กันขายเกินในรอบเดียวกัน)
        cart.append((real_name, price, qty))
        print(f"  Taken out: {qty:,} | Remaining: {items[name][2]:,}\n")

    if not cart:
        print("No items sold.\n")
        return

    # 4) บันทึกลงไฟล์ sales.txt ทุกรายการในตะกร้า
    with open(Sales_file, "a", encoding="UTF_8") as f:
        for name, price, qty in cart:
            f.write(f"{day},{name},{price},{qty}\n")

    total = sum(p * q for _, p, q in cart)  # ยอดรวม = ผลรวมของ ราคา x จำนวน
    print(f"Saved sale on {day}: {len(cart)} item(s), total {total:,.2f} baht\n")


# ---------------------------------------------------------------
# เมนู 4 : รายงานยอดขายรายวัน
# ---------------------------------------------------------------
def Daily_Sales(stock):
    today = date.today().isoformat()
    day = input(f"Input date (YYYY-MM-DD, Enter = {today}) : ") or today

    try:
        with open(Sales_file, "r", encoding="UTF_8") as f:
            data = [row.strip().split(",") for row in f]  # อ่านทุกบรรทัดแล้วแยกช่อง
    except FileNotFoundError:
        print("No sales data found. Please record a sale first.\n")
        return

    # เลือกเฉพาะบรรทัดที่ครบ 4 ช่อง และเป็นวันที่ที่ต้องการ
    rows = [(p[1], float(p[2]), int(p[3])) for p in data if len(p) == 4 and p[0] == day]
    if not rows:
        print(f"No sales on {day}.\n")
        return

    # พิมพ์หัวตาราง (ความกว้างเส้นปรับตามความยาวของ header อัตโนมัติ)
    header = f"| {'Product':<20} | {'Price':>10} | {'Qty':>5} | {'Total':>11} |"
    line = "=" * len(header)
    print(f"{line}\n|{('Daily Sales Report : ' + day):^{len(header) - 2}}|")
    print(f"{line}\n{header}\n{line}")

    for name, price, qty in rows:
        print(f"| {name:<20} | {price:>10,.2f} | {qty:>5,} | {price * qty:>11,.2f} |")

    # แถวสรุปท้ายตาราง: จำนวนรวมและยอดเงินรวมของวันนั้น
    total_qty = sum(q for _, _, q in rows)
    total_money = sum(p * q for _, p, q in rows)
    print(line)
    print(f"| {'Total':<20} | {'':>10} | {total_qty:>5,} | {total_money:>11,.2f} |")
    print(line + "\n")


# ---------------------------------------------------------------
# เมนู 5 : รายงานยอดขายแยกตามสินค้า (รวมทุกวัน)
# ---------------------------------------------------------------
def report_sales(stock):
    sales_by_product = {}  # ชื่อ(ตัวเล็ก) -> [ชื่อจริง, จำนวนที่ขายรวม, ยอดเงินรวม]
    try:
        with open(Sales_file, "r", encoding="UTF_8") as f:
            for row in f:
                parts = row.strip().split(",")
                if len(parts) != 4:
                    continue
                _, name, price, qty = parts  # _ คือไม่ใช้ช่องวันที่
                try:
                    price = float(price)
                    qty = int(qty)
                except ValueError:
                    continue  # ข้ามบรรทัดที่ตัวเลขผิดรูปแบบ

                key = name.lower()
                product = sales_by_product.setdefault(key, [name, 0, 0.0])
                product[1] += qty            # สะสมจำนวนที่ขาย
                product[2] += price * qty    # สะสมยอดเงิน
    except FileNotFoundError:
        print("No sales data found. Please record a sale first.\n")
        return

    if not sales_by_product:
        print("No sales data found. Please record a sale first.\n")
        return

    header = f"| {'Product':<20} | {'Qty sold':>8} | {'Total sales':>12} |"
    line = "=" * len(header)
    print(f"{line}\n|{'Sales Report by Product':^{len(header) - 2}}|")
    print(f"{line}\n{header}\n{line}")

    total_qty = 0
    total_sales = 0.0
    # เรียงตามชื่อสินค้าจาก A ไป Z (lower() เพื่อไม่ให้ตัวพิมพ์ใหญ่เล็กมีผล)
    for name, qty, amount in sorted(sales_by_product.values(), key=lambda item: item[0].lower()):
        print(f"| {name:<20} | {qty:>8,} | {amount:>12,.2f} |")
        total_qty += qty
        total_sales += amount

    # แถวสรุปท้ายตาราง: ยอดรวมสุทธิทุกสินค้า
    print(line)
    print(f"| {'Total':<20} | {total_qty:>8,} | {total_sales:>12,.2f} |")
    print(line + "\n")