from datetime import date

Sales_file = "sales.txt"


def read_rows(file):
    """อ่านไฟล์ คืนลิสต์ (วันที่, ชื่อ, ราคา, จำนวน) ถ้าไม่มีไฟล์คืน None"""
    rows = []
    try:
        with open(file, "r", encoding="UTF_8") as f:
            for row in f:
                p = row.strip().split(",")
                if len(p) == 4:
                    rows.append((p[0], p[1], float(p[2]), int(p[3])))
    except FileNotFoundError:
        return None
    return rows


def add_product(stock):
    today = date.today().isoformat()
    day = input(f"Input date (YYYY-MM-DD, Enter = {today}) : ") or today
    name = input("Input product name : ")
    try:
        price = float(input("Input product price : "))
        qty = int(input("Input product quantity : "))
    except ValueError:
        print("Price and quantity must be numbers.\n")
        return

    with open(stock, "a", encoding="UTF_8") as f:
        f.write("\n" + f"{day},{name},{price},{qty}")
    print(f"Saved: {name} x {qty} = {price * qty:.2f} baht on {day}\n")


def show_product(stock):
    data = read_rows(stock)
    if data is None:
        print("No product data found. Please input product first.\n")
        return

    total = {}  # (วันที่, ชื่อ) -> [ราคา, จำนวนรวม]
    for day, name, price, qty in data:
        t = total.setdefault((day, name), [price, 0])
        t[0] = price
        t[1] += qty

    line = "=" * 78
    print(f"{line}\n|{'Current Products':^76}|")
    print(f"{line}\n| {'Date':<10} | {'Name':<20} | {'Price per piece':>15} | {'Qty':>6} | {'Total price':>11} |\n{line}")
    for (day, name), (price, qty) in sorted(total.items()):
        print(f"| {day:<10} | {name:<20} | {price:>15.2f} | {qty:>6} | {price * qty:>11.2f} |")
    print(line + "\n")


def Sales(stock):
    # 1) อ่านสต็อก: ชื่อ(ตัวเล็ก) -> [ชื่อจริง, ราคา, จำนวนคงเหลือ]
    data = read_rows(stock)
    if not data:
        print("No product in stock. Please input product first.\n")
        return
    items = {}
    for _, name, price, qty in data:
        item = items.setdefault(name.lower(), [name, price, 0])
        item[1] = price
        item[2] += qty

    # 2) หักยอดที่ขายไปแล้ว
    for _, name, _, qty in read_rows(Sales_file) or []:
        if name.lower() in items:
            items[name.lower()][2] -= qty

    # 3) รับข้อมูลการขาย
    today = date.today().isoformat()
    day = input(f"Input sale date (YYYY-MM-DD, Enter = {today}) : ") or today

    cart = []
    while True:
        name = input("Input product name (Enter = finish) : ").strip().lower()
        if not name:
            break
        if name not in items:
            print("Product not found.\n")
            continue

        real_name, price, left = items[name]
        print(f"  Price {price:.2f} baht | In stock: {left}")
        if left <= 0:
            print("  Out of stock.\n")
            continue

        try:
            qty = int(input("Input quantity : "))
        except ValueError:
            print("Quantity must be a number.\n")
            continue
        if not 1 <= qty <= left:
            print(f"Quantity must be between 1 and {left}.\n")
            continue

        items[name][2] -= qty
        cart.append((real_name, price, qty))
        print(f"  Taken out: {qty} | Remaining: {items[name][2]}\n")

    if not cart:
        print("No items sold.\n")
        return

    # 4) บันทึกลงไฟล์
    with open(Sales_file, "a", encoding="UTF_8") as f:
        for name, price, qty in cart:
            f.write(f"{day},{name},{price},{qty}\n")

    total = sum(p * q for _, p, q in cart)
    print(f"Saved sale on {day}: {len(cart)} item(s), total {total:.2f} baht\n")


def Daily_Sales(stock):
    today = date.today().isoformat()
    day = input(f"Input date (YYYY-MM-DD, Enter = {today}) : ") or today

    data = read_rows(Sales_file)
    if data is None:
        print("No sales data found. Please record a sale first.\n")
        return
    rows = [(n, p, q) for d, n, p, q in data if d == day]
    if not rows:
        print(f"No sales on {day}.\n")
        return

    header = f"| {'Product':<20} | {'Price':>10} | {'Qty':>5} | {'Total':>11} |"
    line = "=" * len(header)
    print(f"{line}\n|{('Daily Sales Report : ' + day):^{len(header) - 2}}|")
    print(f"{line}\n{header}\n{line}")
    for name, price, qty in rows:
        print(f"| {name:<20} | {price:>10.2f} | {qty:>5} | {price * qty:>11.2f} |")
    print(line)
    print(f"| {'Total':<20} | {'':>10} | {sum(q for _, _, q in rows):>5} | {sum(p * q for _, p, q in rows):>11.2f} |")
    print(line + "\n")


def report_sales(stock):
    data = read_rows(Sales_file)
    if not data:
        print("No sales data found. Please record a sale first.\n")
        return

    totals = {}  # ชื่อ(ตัวเล็ก) -> [ชื่อ, จำนวนที่ขาย, ยอดเงิน]
    for _, name, price, qty in data:
        t = totals.setdefault(name.lower(), [name, 0, 0.0])
        t[1] += qty
        t[2] += price * qty

    header = f"| {'Product':<20} | {'Qty sold':>8} | {'Total sales':>12} |"
    line = "=" * len(header)
    print(f"{line}\n|{'Sales Report by Product':^{len(header) - 2}}|")
    print(f"{line}\n{header}\n{line}")
    for key in sorted(totals):
        name, qty, amount = totals[key]
        print(f"| {name:<20} | {qty:>8} | {amount:>12.2f} |")
    print(line)
    print(f"| {'Total':<20} | {sum(t[1] for t in totals.values()):>8} | {sum(t[2] for t in totals.values()):>12.2f} |")
    print(line + "\n")