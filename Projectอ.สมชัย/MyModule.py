from datetime import date

Sales_file = "sales.txt"


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
    try:
        qty_sum = {}
        price_of = {}
        with open(stock, "r", encoding="UTF_8") as f:
            for row in f:
                parts = row.strip().split(",")
                if len(parts) != 4:
                    continue
                day, name, price, qty = parts
                key = (day, name)
                qty_sum[key] = qty_sum.get(key, 0) + int(qty)
                price_of[key] = float(price)

        line = "=" * 78
        print(f"{line}\n|{'Current Products':^76}|")
        print(f"{line}\n| {'Date':<10} | {'Name':<20} | {'Price per piece':>15} | {'Qty':>6} | {'Total price':>11} |\n{line}")
        for (day, name), qty in sorted(qty_sum.items()):
            price = price_of[(day, name)]
            print(f"| {day:<10} | {name:<20} | {price:>15.2f} | {qty:>6} | {price * qty:>11.2f} |")
        print(line + "\n")
    except FileNotFoundError:
        print("No product data found. Please input product first.\n")


def Sales(stock):
    # 1) อ่านสต็อก: ชื่อ(ตัวเล็ก) -> [ชื่อจริง, ราคา, จำนวนคงเหลือ]
    items = {}
    try:
        with open(stock, "r", encoding="UTF_8") as f:
            for row in f:
                p = row.strip().split(",")
                if len(p) == 4:
                    item = items.setdefault(p[1].lower(), [p[1], 0, 0])
                    item[1] = float(p[2])
                    item[2] += int(p[3])
    except FileNotFoundError:
        pass

    if not items:
        print("No product in stock. Please input product first.\n")
        return

    # 2) หักยอดที่ขายไปแล้วออกจากสต็อก
    try:
        with open(Sales_file, "r", encoding="UTF_8") as f:
            for row in f:
                p = row.strip().split(",")
                if len(p) == 4 and p[1].lower() in items:
                    items[p[1].lower()][2] -= int(p[3])
    except FileNotFoundError:
        pass

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

    try:
        with open(Sales_file, "r", encoding="UTF_8") as f:
            data = [row.strip().split(",") for row in f]
    except FileNotFoundError:
        print("No sales data found. Please record a sale first.\n")
        return

    # เลือกเฉพาะบรรทัดที่ครบ 4 ช่อง และเป็นวันที่ที่ต้องการ
    rows = [(p[1], float(p[2]), int(p[3])) for p in data if len(p) == 4 and p[0] == day]
    if not rows:
        print(f"No sales on {day}.\n")
        return

    header = f"| {'Product':<20} | {'Price':>10} | {'Qty':>5} | {'Total':>11} |"
    line = "=" * len(header)
    print(f"{line}\n|{('Daily Sales Report : ' + day):^{len(header) - 2}}|")
    print(f"{line}\n{header}\n{line}")

    for name, price, qty in rows:
        print(f"| {name:<20} | {price:>10.2f} | {qty:>5} | {price * qty:>11.2f} |")

    total_qty = sum(q for _, _, q in rows)
    total_money = sum(p * q for _, p, q in rows)
    print(line)
    print(f"| {'Total':<20} | {'':>10} | {total_qty:>5} | {total_money:>11.2f} |")
    print(line + "\n")


def report_sales(stock):
    sales_by_product = {}
    try:
        with open(Sales_file, "r", encoding="UTF_8") as f:
            for row in f:
                parts = row.strip().split(",")
                if len(parts) != 4:
                    continue
                _, name, price, qty = parts
                try:
                    price = float(price)
                    qty = int(qty)
                except ValueError:
                    continue

                key = name.lower()
                product = sales_by_product.setdefault(key, [name, 0, 0.0])
                product[1] += qty
                product[2] += price * qty
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
    for name, qty, amount in sorted(sales_by_product.values(), key=lambda item: item[0].lower()):
        print(f"| {name:<20} | {qty:>8} | {amount:>12.2f} |")
        total_qty += qty
        total_sales += amount

    print(line)
    print(f"| {'Total':<20} | {total_qty:>8} | {total_sales:>12.2f} |")
    print(line + "\n")