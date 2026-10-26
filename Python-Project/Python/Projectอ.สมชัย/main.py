from MyModule import *

def main():
    menu_info = "stock.txt"

    while True:
        head = f"|{'WELCOME TO RESTAURANT':^40}|"
        line = '=' * len(head)
        ch = (f"| {'1. Input Product Management':<39}|\n| {'2. Show Product Report':<39}|\n"
      f"| {'3. Sales Management':<39}|\n| {'4. Daily Sales Report':<39}|\n"
      f"| {'5. Sales Report by Product':<39}|\n| {'6. Exit program':<39}|")
        print(line, head, line, ch, line, sep='\n')

        try:
            choice = int(input("Enter choice : "))
            if choice == 1:add_product(menu_info)
            elif choice == 2:show_product(menu_info)
            elif choice == 3:Sales(menu_info)
            elif choice == 4:Daily_Sales(menu_info)
            elif choice == 5:report_sales(menu_info)
            elif choice == 6:
                print("Exiting program.")
                break

            else:
                print("Please enter a valid choice (1-5).\n")

        except ValueError:
            print('Please enter choice only (1-5).\n')


if __name__ == "__main__":
    main()