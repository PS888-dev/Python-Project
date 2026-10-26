from test import *

def main():
    member_info = None

    while True:
        head = f"|{'WELCOME TO RESTAURANT':^40}|"
        line = '=' * len(head)
        ch = f": {'1. Register Member':<39}:\n: {'2. Delete Member':<39}:\n: {'3. Menu':<39}:\n: {'4. Summary of member totals':<39}:\n: {'5. Daily sales summary':<39}:\n: {'6. Exit program':<39}:"
        print(line, head, line, ch, line, sep='\n')

        try:
            choice = int(input('Enter choice : '))

            if choice == 1:
                member_info = register_member()

            elif choice == 2:
                delete_member()

            elif choice == 3:
                if not member_info:
                    print("\nPlease sign in before ordering!\n")
                    continue

                filename = "menu.txt"
                menus = read_menu_from_file(filename)
                all_orders = []

                for category, menu_items in menus.items():
                    orders = select_from_category(category, menu_items)
                    all_orders.extend(orders)
                    
                discount = 0
                ans = input("\nApply member discount? (y/n) : ")
                if ans.lower() == "y":
                    try:
                        discount = int(input("Enter discount percentage : "))
                    except ValueError:
                        discount = 0
                        print("Invalid input. No discount applied.")

                show_receipt(all_orders, member_info, discount)

            elif choice == 4:
                report_sales_by_member()

            elif choice == 5:
                daily_sales_report()

            elif choice == 6:
                print("Exiting program.")
                break

            else:
                print("Please enter a valid choice (1-6).\n")

        except ValueError:
            print('Please enter numbers only (1-6).\n')

        back = input("\nDo you want to go back to the main menu? (Y/N) : ").strip().lower()
        if back != 'y':
            break

if __name__ == "__main__":
    main()