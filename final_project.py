import json
import sys
from datetime import datetime


# Function to read text file
def read_file(database_file: str):
    try:
        # Retrieve text from text file
        with open(database_file, "r") as file:
            data = file.read()
        # If file is empty, returns an empty list, else return data from text file
        if data == "": 
            return []
        else: 
            item_dict = json.loads(data)
            return item_dict
    # If text file does not exist, notify user and create a new text file
    except FileNotFoundError: 
        print(f"ERROR: File {database_file} does not exist in this directory. Creating a new text file...")
        with open(database_file, "w") as file:
            file.write("[]")
            return []
    # If text formatting is corrupted, store file data in a separate text file and create a new file
    except json.JSONDecodeError:
        print(f"ERROR: File {database_file} has been tampered and cannot be read due to incorrect formatting.")
        with open("temp.txt", "w") as file:
            file.write(data)
            print(f"Contents from {database_file} have been stored in 'temp.txt', and a new text file will be created.")
        with open(database_file, "w") as file:
            file.write("[]")
            return []


# Function to write to text file
def write_file(database_file: str, input: dict, format: str):
    # If format is 'a', append input into the dictionary list
    if format == "a":
        dict_list = read_file(database_file)
        dict_list.append(input)
        input = dict_list

    # Open text file to write 
    with open(database_file, "w") as file:
        file.write(json.dumps(input, indent=2))


# Function for input validation
def check_input(user_input: str, check_type = "empty", item_attribute = "", file = ""):
    # Code block will loop until input is valid
    while True:
        try:
            # Remove trailing and leading spaces from input
            user_input = user_input.strip()

            # Check if input is empty
            if user_input == "":
                error_message = "This cannot be left empty"
                raise ValueError()
            
            match check_type:
                # Check if input is empty (already done above)
                case "empty":
                    output = user_input

                # Check if input already exists in given file
                case "duplicate":
                    dict_list = read_file(file)

                    for item_dict in dict_list: 
                        if user_input == item_dict[item_attribute]: # item_attribute refers to the category of the item
                            error_message = f"{item_attribute} already exists"
                            raise ValueError()
                    output = user_input

                # Check if input is a float
                case "float":
                    error_message = "Invalid integer or float"
                    output = float(format(float(user_input), ".2f"))

                # Check if input is a integer
                case "int":
                    error_message = "Invalid integer"
                    output = int(user_input)

        except ValueError:
            # If input produces an error, print error message and request for input again
            user_input = input(error_message + ", please try again: ")
        else: 
            # Return error-free output
            return output


# Add new product and its details to text file
def add_product():
    # Retrieve product list from text file
    product_list = read_file("products.txt")

    # Automatically generate ID based on number of existing products and display to user
    product_id = "P" + str(len(product_list)+1).rjust(3, "0")
    print(f"Assigned Product ID: {product_id}")

    # Prompt user to enter product name, and check if it already exists in the file
    product_name = check_input(input("Product Name: "), "duplicate", "Name", "products.txt")

    # Prompt user to enter description and check if input is empty
    description = check_input(input("Description: "), "empty")

    # Prompt user to enter price, and convert input into a float
    price = check_input(input("Price: "), "float")

    # Prompt user to enter stock, and ensure that given input is a positive integer
    stock = check_input(input("Stock: "), "int")
    while stock < 0:
        stock = check_input(input("Stock cannot be a negative value, please try again: "), "int")

    # Store user input in a dictionary
    new_product = {"Product ID": product_id, "Name": product_name, "Description": description, "Price": price, "Stock": stock}
    
    # Append dictionary to text file and display confirmation message
    write_file("products.txt", new_product, "a")
    print("New product added successfully!")


def update_product():
    # Initialize variables
    PRODUCT_ATTRIBUTES = ("Product ID", "Name", "Description", "Price", "Stock")
    attribute_num = len(PRODUCT_ATTRIBUTES)
    product_dict = {}

    # Retrieve product list from file and display existing product IDs
    product_list = read_file("products.txt")
    print("List of Product IDs and Names:")
    for product in product_list:
        print(f"{product["Product ID"]} - {product["Name"]}")

    print() # Spacing

    # Prompt user to enter product ID, and check if input is empty
    product_id = check_input(input("Please enter the ID of the product you wish to change: "), "empty")

    # If product with given product ID exists, store product information in product_dict 
    for product in product_list:
        if product_id == product["Product ID"]:
            product_dict = product
            break
    
    # If product does not exist, notify user and return to main menu
    if product_dict == {}:
        print("ERROR: Product ID was not found. ")
        return
    
    print() # Spacing
    
    # Print attributes of the selected product
    for key in product_dict:
        print(f"{key.ljust(13)}: {product_dict[key]}")
    
    print() # Spacing
    
    # Print options for editing product attributes
    for i in range(1, attribute_num):
        print(f"[{i}] {PRODUCT_ATTRIBUTES[i]}")
    print(f"[{attribute_num}] Return to Main Menu")

    # Ask user to select an option, check if input is an integer
    choice = check_input(input("\nWhich element do you wish to change? "), "int")
    
    # Loop until user chooses a valid option
    while choice < 1 or choice > attribute_num:   
        choice = check_input(input("Option does not exist. Please choose a valid option: "), "int")

    # If "Exit" was chosen
    if choice == attribute_num:
        return
    
    # If any other option was chosen
    else:
        # Store selected attribute name and prompt user to enter new data
        item_attribute = PRODUCT_ATTRIBUTES[choice] 
        new_data = input(f"Please enter new data for {item_attribute}: ")

        # Update attributes of the chosen element
        match item_attribute:
            case "Name":
                new_data = check_input(new_data, "duplicate", item_attribute, "products.txt")

            case "Description":
                new_data = check_input(new_data, "empty")

            case "Price":
                new_data = check_input(new_data, "float")

            case "Stock":
                new_data = check_input(new_data, "int")
                while new_data < 0:
                    new_data = check_input(input("Stock cannot be a negative value, please try again: "), "int")

        # After validating input, write new data into product_dict, and then update the text file
        product_dict[item_attribute] = new_data
        write_file("products.txt", product_list, "w")

        # Display confirmation message
        print("Product updated successfully!")


def add_supplier():
    # Retrieve supplier data from suppliers.txt
    supplier_list = read_file("suppliers.txt")

    # Automatically generate ID based on number of existing suppliers and display to user
    supplier_id = "S" + str(len(supplier_list)+1).rjust(3, "0")
    print(f"Assigned Supplier ID: {supplier_id}")

    # Prompt user to enter supplier name and validate input
    name = check_input(input("Please enter Supplier Name: "), "duplicate", "Name", "suppliers.txt")
    
    # Prompt user to enter supplier contact number
    contact = input("Please enter Contact Number: ")
    # Check if contact number format is valid
    while not contact.isdigit() or len(contact) < 10:
        contact = input("Contact number should contain only digits and have least 10 digits, please try again: ").strip()
    
    # Prompt user to enter supplier email address
    email = check_input(input("Please enter Email Address: "), "empty")
    # Check if email address format is valid
    while email.count("@") != 1 or not "@" in email[1:-5] or not "." in email[-4:-2]:
        email = check_input(input("Invalid Email Address format, please try again: "), "empty")

    # Create a new supplier entry and store given input
    new_entry = {"Supplier ID": supplier_id, "Name": name, "Contact Number": contact, "Email": email}

    # Write entry to text file and display confirmation message
    write_file("suppliers.txt", new_entry, "a")
    print("\nNew supplier information has been added! ")


# order placing function
def order_placement():

    #reads the products.txt text file and stores it 
    product_list = read_file("products.txt") # Replaced this, renamed x to product_list

    # prints out the available products
    for element in product_list:
        print(f" Product ID: {element['Product ID']}\n Name: {element['Name']}\n Description: {element['Description']}\n Price: {element['Price']}\n Stock: {element['Stock']}")
        print()
    
    # receives the product ID from the user
    PID = input("Type the product ID that you wish to order: ")
    item = next((element for element in product_list if str(element['Product ID']) == PID), None)

    # runs if the product ID received is valid
    if item:

        # prints the product that was specified by the user
        for key in item:
            print(f"{key}: {item[key]}")
        
        print() # Spacing

        # initialize choice variable to loop order type
        choice = 0
        while choice != "1" and choice != "2": 

            # askes the user what order type they want
            choice = input("[1] Sale\n[2] Resupply\nOrder Type: ")

            if choice == "1":
                order_type = "Sale"

                if item["Stock"] == 0: # notifies the user that item is out of stock and returns to main menu
                    print("Product is currently out of stock, please restock this product. ")
                    return
                
            elif choice == "2":
                order_type = "Resupply"
            else:
                print("Invalid option, please try again \n")

        # asks the user how much products they want to sell / resupply
        quantity = check_input(input("Order quantity: "), "int")

        # loops in case product is too little to sell then the specified amount or if quantity is negative
        while True:
            if quantity < 1:
                quantity = check_input(input("Quantity cannot be less than 1, please try again: "), "int")
            elif order_type == "Sale" and quantity > item["Stock"]:
                quantity = check_input(input("Order amount exceeds inventory level, please try again: "), "int")
            else:
                break

        # confirmation for order placement. loops if input is not acceptable
        confirmation = input((f"The total cost of {quantity} {item['Name']} is {quantity * float(item['Price'])} \n Confirm?(Y/N) -> "))
        while confirmation.upper() != "Y" and confirmation.upper() != "N":
            confirmation = input("Please select 'Y' or 'N': ")

        if confirmation.upper() == "Y":

            # reads the data in the orders.txt text file
            data = read_file("orders.txt") 

            # generates a new order id based on the last order id
            ord_ID = "OR" + str(len(data)+1).rjust(3, "0")

            # creates a new dictionary for new order
            new_order = {"Order ID": ord_ID, "Product ID": item['Product ID'], "Quantity": quantity, "Order Date": datetime.now().strftime ("%d/%m/%Y"), "Order Type": order_type}

            # writes the order into the orders.txt text file
            write_file("orders.txt", new_order, "a") 
            print(f"{order_type} Order Placed")

            # changes the value of stock in the product list
            for element in product_list:
                if element == item:
                    if order_type == "Sale":
                        element['Stock'] -= quantity
                    else:
                        element['Stock'] += quantity
                    break

            # writes the changes into the products.txt text file
            write_file("products.txt", product_list, "w") 
        
        # activates if order is cancelled
        else:
            print(f"{order_type} Order Cancelled")

    # tells the user there is no product with the inputted product ID
    else:
        print("There is no such product. ")


def view_inventory():
    # Read the products data from a file
    products = read_file("products.txt")

    # Check if the inventory is empty
    if products == {}:
        print("No products available in the inventory.")
        return

    # Display all available product IDs and their names
    print("\nProduct IDs available:")
    for product in products:
        print(f"{product['Product ID']}: {product['Name']}")

    # Prompt the user to input a specific product ID to view details
    product_id = input("\nEnter product ID: ")

    # Initialize a variable to hold the details of the requested product
    product_details = None
    # Search for the product in the inventory by matching the product ID
    for product in products:
        if product["Product ID"] == product_id:
            product_details = product
            break  # Exit the loop once the product is found
            break

    # If no matching product is found, display an error message and exit
    if not product_details:
        print(f"Product ID {product_id} not found.")
        return

    # Display the details of the selected product
    print("\nProduct Details:")
    print(f"Product ID: {product_details['Product ID']}")
    print(f"Name: {product_details['Name']}")
    print(f"Description: {product_details['Description']}")
    print(f"Price: ${float(product_details['Price']):.2f}")
    print(f"Stock: {product_details['Stock']}")


def generate_report():
    product_list = read_file("products.txt")
    order_list = read_file("orders.txt")

    # Low stock items: If an item has a stock of 10 or less, display here
    print("Low Stock Items\n---------------")
    # Loops through each product dictionary
    for product in product_list:
        # If product stock is 10 or less, print product ID, name and stock level
        if product["Stock"] <= 10:
            print("Product ID  :", product["Product ID"])
            print("Product Name:", product["Name"])
            print("Stock level :", product["Stock"], "\n")
    
    # Product sales: List product ID, name, sale quantity, total revenue for sale orders
    print("\nProduct Sales\n-------------")
    for product in product_list:
        # Initialize sales variable
        sales = 0
        for order in order_list:
            # If Product ID is in order and order type is sale, add order quantity to sales
            if order["Product ID"] == product["Product ID"] and order["Order Type"] == "Sale":
                sales += order["Quantity"]
        # If product has sales, display details to user
        if sales != 0:
            print("Product ID    :", product["Product ID"])
            print("Product Name  :", product["Name"])
            print("Order Quantity:", sales)
            print("Total Revenue : $", format(sales*product["Price"], ".2f"), "\n")

    # Supplier orders: List supplier order details 
    print("\nSupplier Orders\n---------------")
    for order in order_list:
        # If order type is "Resupply", display details to user
        if order["Order Type"] == "Resupply":
            print("Order ID  :", order["Order ID"])
            print("Product ID:", order["Product ID"])
            print("Quantity  :", order["Quantity"])
            print("Order Date:", order["Order Date"], "\n")


def main_menu():
    while True:
        #input block for selecting function
        print("\n INVENTORY MANAGEMENT SYSTEM \n-----------------------------")
        print(" 1 --> Add new product \n 2 --> Update product attributes \n 3 --> Add new supplier \n 4 --> Place an order \n 5 --> View inventory \n 6 --> Generate reports \n 7 --> Exit \n")
        choice = input("Please select a function by entering its number: ")
        print() # Spacing

        try:
            match choice:
                case "1":
                    print(" ADD NEW PRODUCT \n-----------------")
                    add_product()
                case "2":
                    print(" UPDATE PRODUCT ATTRIBUTES \n---------------------------")
                    update_product()
                case "3":
                    print(" ADD NEW SUPPLIER \n------------------")
                    add_supplier()
                case "4":
                    print(" PLACE AN ORDER \n----------------")
                    order_placement()
                case "5":
                    print(" VIEW INVENTORY \n----------------")
                    view_inventory()
                case "6":
                    print(" GENERATE REPORTS \n------------------")
                    generate_report()
                case "7":
                    sys.exit(0)
                case _:
                    print("\nInvalid option. Please try again. ")
                    continue

            input("\nPress ENTER to return to main menu...")
        except SystemExit:
            print("Program terminated. ")
            break


main_menu()