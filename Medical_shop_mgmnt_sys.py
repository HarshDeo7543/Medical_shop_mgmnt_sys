import pickle
import os
from datetime import datetime
import logging

# Setup logging configuration
logging.basicConfig(filename="shop.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# 1. Inventory Management: Stock Replenishment Alerts and Expiry Date Management

def write_file():
    f = open("MEDICAL_SHOP_SYSTEM.dat", "ab")
    c = "y"
    while c == "y":
        l = {}
        mdno = int(input("Enter the medicine number: "))
        mname = input("Enter the medicine name: ")
        price = float(input("Enter the price: "))
        qty = int(input("Enter the quantity: "))
        expiry_date = input("Enter the expiry date (dd-mm-yyyy): ")
        l["mdno"] = mdno
        l["medicine name"] = mname
        l["price"] = price
        l["quantity"] = qty
        l["expiry_date"] = expiry_date
        pickle.dump(l, f)
        logging.info(f"Added Medicine - Number: {mdno}, Name: {mname}, Price: {price}, Quantity: {qty}, Expiry: {expiry_date}")
        c = input("Wish to enter more records? Press y/n: ")
    f.close()

def stock_alert(threshold=10):
    """Alert if any medicine quantity falls below a certain threshold."""
    try:
        with open("MEDICAL_SHOP_SYSTEM.dat", "rb") as f:
            while True:
                try:
                    rec = pickle.load(f)
                    if rec["quantity"] <= threshold:
                        print(f"Alert: {rec['medicine name']} is low on stock (Quantity: {rec['quantity']})")
                        logging.warning(f"Stock Alert: {rec['medicine name']} is low on stock (Quantity: {rec['quantity']})")
                except EOFError:
                    break
    except FileNotFoundError:
        print("File not found. Please create the file first.")

def check_expired_medicine():
    """Check if any medicine has expired."""
    try:
        with open("MEDICAL_SHOP_SYSTEM.dat", "rb") as f:
            today = datetime.today()
            while True:
                try:
                    rec = pickle.load(f)
                    expiry_date = datetime.strptime(rec['expiry_date'], "%d-%m-%Y")
                    if expiry_date < today:
                        print(f"Expired: {rec['medicine name']} (Expired on {rec['expiry_date']})")
                        logging.warning(f"Expired Medicine: {rec['medicine name']} (Expired on {rec['expiry_date']})")
                except EOFError:
                    break
    except FileNotFoundError:
        print("File not found. Please create the file first.")


# 2. Advanced Search Features

def search_by_price_range(min_price, max_price):
    """Search for medicines in a specific price range."""
    try:
        with open("MEDICAL_SHOP_SYSTEM.dat", "rb") as f:
            while True:
                try:
                    rec = pickle.load(f)
                    if min_price <= rec['price'] <= max_price:
                        print(rec)
                        logging.info(f"Searched Medicine - Name: {rec['medicine name']}, Price: {rec['price']}")
                except EOFError:
                    break
    except FileNotFoundError:
        print("File not found. Please create the file first.")

def search_by_expiry_date_range(start_date, end_date):
    """Search for medicines expiring within a specific date range."""
    try:
        with open("MEDICAL_SHOP_SYSTEM.dat", "rb") as f:
            start_date = datetime.strptime(start_date, "%d-%m-%Y")
            end_date = datetime.strptime(end_date, "%d-%m-%Y")
            while True:
                try:
                    rec = pickle.load(f)
                    expiry_date = datetime.strptime(rec['expiry_date'], "%d-%m-%Y")
                    if start_date <= expiry_date <= end_date:
                        print(rec)
                        logging.info(f"Medicine Expiry Search - Name: {rec['medicine name']}, Expiry Date: {rec['expiry_date']}")
                except EOFError:
                    break
    except FileNotFoundError:
        print("File not found. Please create the file first.")


# 3. Customer Management System

def add_customer():
    """Add a new customer."""
    customer = {}
    customer['name'] = input("Enter customer name: ")
    customer['contact'] = input("Enter customer contact: ")
    customer['address'] = input("Enter customer address: ")
    customer['purchase_history'] = []
    with open("CUSTOMERS.dat", "ab") as f:
        pickle.dump(customer, f)
    logging.info(f"Added Customer - Name: {customer['name']}, Contact: {customer['contact']}")
    print("Customer added successfully.")

def view_customers():
    """Display all customers."""
    try:
        with open("CUSTOMERS.dat", "rb") as f:
            while True:
                try:
                    customer = pickle.load(f)
                    print(customer)
                except EOFError:
                    break
    except FileNotFoundError:
        print("No customers found.")

def update_customer_purchase(customer_name, purchase_details):
    """Update a customer's purchase history."""
    try:
        customers = []
        with open("CUSTOMERS.dat", "rb") as f:
            while True:
                try:
                    customer = pickle.load(f)
                    if customer['name'] == customer_name:
                        customer['purchase_history'].append(purchase_details)
                    customers.append(customer)
                except EOFError:
                    break

        with open("CUSTOMERS.dat", "wb") as f:
            for customer in customers:
                pickle.dump(customer, f)
        logging.info(f"Updated Purchase History - Customer: {customer_name}, Details: {purchase_details}")
    except FileNotFoundError:
        print("Customer file not found.")


# 4. Sales and Reports Generation

def sale_file():
    """Handle the sale of a medicine."""
    n = input("Enter medicine name: ")
    f = open("MEDICAL_SHOP_SYSTEM.dat", "rb+")
    flag = False
    try:
        while True:
            l1 = pickle.load(f)
            if l1["medicine name"] == n:
                num = int(input("Enter quantity to be sold: "))
                if l1["quantity"] >= num:
                    l1["quantity"] -= num
                    f.seek(f.tell() - len(pickle.dumps(l1)))
                    pickle.dump(l1, f)
                    flag = True
                    name = input("Enter your name: ")
                    bill = l1["price"] * num
                    print(f"Customer Name: {name}")
                    print(f"Medicine: {n}, Quantity: {num}, Total: {bill}")
                    update_customer_purchase(name, {"medicine": n, "quantity": num, "total_amount": bill})
                    logging.info(f"Sale Recorded - Customer: {name}, Medicine: {n}, Quantity: {num}, Total: {bill}")
                    print("Sale recorded successfully.")
                    break
                else:
                    print("Not enough stock.")
                    break
    except EOFError:
        pass
    if not flag:
        print("Medicine not available.")
    f.close()


def generate_sales_report():
    """Generate sales report."""
    try:
        with open("CUSTOMERS.dat", "rb") as f:
            total_sales = 0
            while True:
                try:
                    customer = pickle.load(f)
                    for purchase in customer['purchase_history']:
                        total_sales += purchase['total_amount']
                        print(purchase)
                except EOFError:
                    break
        print(f"Total Sales: {total_sales}")
        logging.info(f"Generated Sales Report - Total Sales: {total_sales}")
    except FileNotFoundError:
        print("No sales data found.")


# Main menu
while True:
    print("\n--- Medical Shop Management System ---")
    print("1. Create file (Add medicine records)")
    print("2. Display all records")
    print("3. Search records by price range")
    print("4. Search records by expiry date range")
    print("5. Sale")
    print("6. Add Customer")
    print("7. View Customers")
    print("8. Generate Sales Report")
    print("9. Check Stock Alerts")
    print("10. Check Expired Medicines")
    print("11. Exit")

    choice = int(input("Enter your choice: "))

    if choice == 1:
        write_file()
    elif choice == 2:
        read_file()
    elif choice == 3:
        min_price = float(input("Enter minimum price: "))
        max_price = float(input("Enter maximum price: "))
        search_by_price_range(min_price, max_price)
    elif choice == 4:
        start_date = input("Enter start date (dd-mm-yyyy): ")
        end_date = input("Enter end date (dd-mm-yyyy): ")
        search_by_expiry_date_range(start_date, end_date)
    elif choice == 5:
        sale_file()
    elif choice == 6:
        add_customer()
    elif choice == 7:
        view_customers()
    elif choice == 8:
        generate_sales_report()
    elif choice == 9:
        stock_alert()
    elif choice == 10:
        check_expired_medicine()
    elif choice == 11:
        print("Exiting...")
        break
    else:
        print("Invalid choice. Please try again.")
