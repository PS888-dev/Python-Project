import datetime

def register_member():
    name = input("Enter member name : ")
    table = input("Enter table number : ")

    with open("member.txt", "a", encoding="utf-8") as f:
        f.write(f"MEMBER : {name} | TABLE : {table}\n")

    print(f"Member '{name}' registered at Table {table}")
    return name, table

def delete_member():
    while True:
        name_to_delete = input("Enter member name to delete (Enter to exit) : ")

        if name_to_delete.strip() == "":
            break

        try:
            with open("member.txt", "r", encoding="utf-8") as f:
                lines = f.readlines()

            found = False
            new_lines = []

            for line in lines:
                line = line.strip()

                if line.startswith("MEMBER : "):
                    try:
                        member_part = line.split("|")[0].strip()
                        member_name = member_part.replace("MEMBER : ", "").strip()

                        if member_name.lower() == name_to_delete.lower():
                            found = True
                            continue
                    except Exception:
                        pass

                new_lines.append(line + "\n")

            if not found:
                print(f"Member '{name_to_delete}' not found. Please try again.\n")
                continue

            with open("member.txt", "w", encoding="utf-8") as f:
                f.writelines(new_lines)

            print(f"Member '{name_to_delete}' has been removed successfully.\n")
            break

        except FileNotFoundError:
            print("Error: member.txt not found. Please register a member first.\n")
            break

def read_menu_from_file(filename):
    menus = {}
    category = None

    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue

            if line.startswith("===") and line.endswith("==="):
                category = line.replace("=", "").strip()
                menus[category] = []
                continue

            if line.startswith("-"):
                continue

            if category and "," in line:
                parts = line.split(",")
                if len(parts) == 3:
                    no = parts[0].strip()
                    name = parts[1].strip()
                    price = float(parts[2].strip())
                    menus[category].append({
                        "no": no,
                        "name": name,
                        "price": price
                    })
    return menus

def show_menu_by_category(category, menu_items):
    h = f"|{category:^46}|"
    head = f'| No.|{'Name':^30}|{'Price':^10}|'
    l = '=' * len(h)
    print('', l, h, l, head, l, sep='\n')

    i = 1
    for item in menu_items:
        print(f"|{i:>3} | {item['name']:<29}|{item['price']:^7}.- |")
        i += 1
    print(l)

def select_from_category(category, menu_items):
    orders = []
    show_menu_by_category(category, menu_items)

    selected = input("Select a menu (1,3,5 or enter to skip) : ").strip()

    if selected == "":
        return orders

    selected_numbers = []
    for num in selected.split(","):
        cleaned_num = num.strip()
        if cleaned_num:
            selected_numbers.append(cleaned_num)

    for num in selected_numbers:
        found = False
        for item in menu_items:
            if item["no"] == num:
                qty = input(f"Enter the number of '{item['name']}': ")
                if qty.isdigit():
                    qty = int(qty)
                    total = item["price"] * qty
                    orders.append({
                        "category": category,
                        "name": item["name"],
                        "price": item["price"],
                        "qty": qty,
                        "total": total
                    })
                else:
                    print("Please enter the quantity in numbers.")
                found = True
                break
        if not found:
            print(f"No menu number found. {num}")

    return orders

def calculate_total(orders, discount=0):
    total = sum(item["price"] * item["qty"] for item in orders)
    if discount > 0:
        total = total - (total * discount / 100)
    return total

def show_receipt(all_orders, member_info, discount=0):
    name, table = member_info
    now = datetime.datetime.now()
    date_str = now.strftime("%Y-%m-%d %H:%M:%S")

    print(f"\n===== ORDER SUMMARY | TABLE {table} | MEMBER: {name} ======\n")
    print('=' * 48, f"| {'Name':^35}| {'Price':^8}|", '=' * 48, sep='\n')
    
    for order in all_orders:
        print(f"| {order['name']:<28} * {order['qty']:>3} | {order['total']:>5}.- |")
    print('=' * 48)

    total_price = calculate_total(all_orders, discount)
    
    print(f"| Discount : {discount:>3}%{'':30}|")
    print(f"| Total : {total_price:>4} Baht{'':27}|")
    print('=' * 48)

    with open("sales.txt", "a", encoding="utf-8") as f:
        f.write(f"=== TABLE {table} | MEMBER: {name} | DATE: {date_str} ===\n")
        for order in all_orders:
            f.write(f"- {order['name']} x {order['qty']} = {order['total']} Baht\n")
        if discount > 0:
            f.write(f"Discount: {discount}%\n")
        f.write(f"Total Price: {total_price} Baht\n")

def report_sales_by_member():
    try:
        with open("sales.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()

        sales_data = {}
        current_member = None

        for line in lines:
            line = line.strip()

            if line.startswith("=== TABLE"):
                parts = line.split("|")
                for p in parts:
                    if "MEMBER:" in p:
                        current_member = p.split(":")[1].strip()
                        if current_member not in sales_data:
                            sales_data[current_member] = {
                                "food": 0.0,
                                "snack": 0.0,
                                "drink": 0.0,
                                "total": 0.0
                            }

            elif line.startswith("- "):
                item_part = line.split("=")
                name = item_part[0].split("x")[0].replace("-", "").strip()
                price = float(item_part[1].replace("Baht", "").strip())

                is_drink = False
                drink_words = [
                    "tea",
                    "water",
                    "coke",
                    "coffee",
                    "juice",
                    "milk",
                    "smoothie",
                    "drink",
                    "herbal"
                ]
                for word in drink_words:
                    if word.lower() in name.lower():
                        is_drink = True
                        break

                is_snack = False
                snack_words = [
                    "cookie",
                    "cake",
                    "fries",
                    "donut",
                    "snack",
                    "bread",
                    "toast",
                    "muffin",
                    "pie",
                    "waffle",
                    "brownie"
                ]
                for word in snack_words:
                    if word.lower() in name.lower():
                        is_snack = True
                        break

                if is_drink == True:
                    sales_data[current_member]["drink"] += price

                elif is_snack == True:
                    sales_data[current_member]["snack"] += price

                else:
                    sales_data[current_member]["food"] += price

            elif line.startswith("Total Price:"):
                total = float(line.replace("Total Price:", "").replace("Baht", "").strip())
                sales_data[current_member]["total"] += total

        print("\n=== Summary of sales according to members ===\n")
        for member, data in sales_data.items():
            print(f"Member : {member}")
            print(f"  - Total food sales : {data['food']} Baht")
            print(f"  - Total drink sales : {data['drink']} Baht")
            print(f"  - Total snack sales : {data['snack']} Baht")
            print(f"  - Total Price : {data['total']} Baht\n")

    except FileNotFoundError:
        print("The sales.txt file was not found.")

def daily_sales_report():
    while True:
        date_input = input("Enter the date to view sales (YYYYMMDD) or press Enter to exit : ").strip()

        if date_input == "":
            return
        
        if len(date_input) != 8 or not date_input.isdigit():
            print("Invalid date format. Please enter in YYYYMMDD format.")
            continue
        
        formatted_date = f"{date_input[:4]}-{date_input[4:6]}-{date_input[6:]}"
        
        total_sales = 0
        current_block_date = None

        try:
            with open("sales.txt", "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if "DATE:" in line:
                        date_part = line.split("DATE:")[1].strip().split()[0]
                        current_block_date = date_part
                    
                    if "Total Price:" in line and current_block_date == formatted_date:
                        price = float(line.replace("Total Price:", "").replace("Baht", "").strip())
                        total_sales += price
        except FileNotFoundError:
            print("No sales data found.")
            return
        else:
            print("\n=== DAILY SALES REPORT ===", f"Date: {formatted_date}", f"Total Sales: {total_sales} Baht", sep='\n')
            break