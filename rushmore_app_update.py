import json # simple database for storing orders
from datetime import datetime # for timestamping order
import os # managing the database file .json

pizza_data = {
    "1": {"name": "Classic", "price": 3.4},
    "2": {"name": "Chicken", "price": 4.5},
    "3": {"name": "Pepperoni", "price": 4.0},
    "4": {"name": "Deluxe", "price": 6.0},
    "5": {"name": "Vegetable", "price": 4.0},
    "6": {"name": "Chocolate", "price": 12.0},
    "7": {"name": "Cheese", "price": 5.0}
}

"""
data to save: order datetime, pizza-type, order-type, quantity,  total_price, discount_applied
"""
ORDERDB_FILE = 'pizza_orders.json' #  database file name

def save_order_to_json(pizza_type, order_type, quantity, price, discount):
    order = {
        'order_datetime': datetime.now().strftime('%Y-%m-%d-%H:%M:%S'),
        'pizza_type': pizza_type,
        'order_type': order_type,
        'quantity': quantity,
        'total_price': price,
        'discount_applied': discount
    }

    if os.path.exists(ORDERDB_FILE):
        with open(ORDERDB_FILE, 'r+', encoding='utf-8') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = []
            data.append(order)
            file.seek(0) # moves the cursor to the beginning of the file
            json.dump(data, file, indent=4)
    else:
        with open(ORDERDB_FILE, 'w', encoding='utf-8') as file:
            json.dump([order], file, indent=4)



def calculate_payment(price, quantity, discount_rate=0.0):
    total = price * quantity
    discount = total * discount_rate
    return total - discount


def handle_box_order(pizza_name, price):
    """
    Process box order quantity and payments
    """
    while True:
        qty_input = input("How many Box(es) do you want? (or type 'q' to cancel): ").strip()
        if qty_input.lower() == 'q':
            print('Box Order Cancelled')
            break
        elif qty_input.isdigit():
            quantity = int(qty_input)
            break
        else:
            print("Please enter a valid number.")
        
    # discount and payment
    discount_rate = 0.0
    if 5 <= quantity < 10:
        discount_rate = 0.10
    elif quantity >= 10:
        discount_rate = 0.20

    discount_applied = discount_rate > 0.0
    total = calculate_payment(price=price, quantity=quantity, discount_rate=discount_rate) # to calculate the total
    print(f"Your payment is ${total:.2f} for {quantity} of {pizza_name} Pizza box(es).")
    if discount_applied:
        print(f"A discount of {int(discount_rate * 100)}% was applied.")
    
    save_order_to_json(pizza_type=pizza_name, order_type='Box', quantity=quantity, price=total, discount=discount_applied)


def handle_slice_order(pizza_name, slice_price):
    """
    Process slice order quantity and payments
    """
    while True:
        qty_input = input("How many slices do you want? (or type 'q' to cancel): ").strip()
        if qty_input.lower() == 'q':
            print('Slice Order Cancelled')
            break
        elif qty_input.isdigit():
            quantity = int(qty_input)
            break
        else:
            print("Please enter a valid number.")
        
    discount_rate = 0.0
    if 5 <= quantity < 10:
        discount_rate = 0.10
    elif quantity >= 10:
        discount_rate = 0.20

    discount_applied = discount_rate > 0.0
    
    total = calculate_payment(price=slice_price, quantity=quantity) # to calculate the total
    print(f"Your payment is ${total:.2f} for {quantity} of {pizza_name} Pizza slice(s).")
    # save to the database
    save_order_to_json(pizza_type=pizza_name, order_type='Slice', quantity=quantity, price=total, discount=False)

def pizza_selection_order(pizza_type):
    """
    Handling Pizza Type Based on Boxes or Slices
    """
    if pizza_type in pizza_data:
        pizza = pizza_data[pizza_type]
        name = pizza["name"]
        price = pizza['price'] # per box
        slice_price = round(price / 8, 2)
        # pizza_details
        print(f"You selected {name}\nPrice - ${price} per box | ${slice_price} per slice")
        # select either box or slices
        while True:
            choice = input("Select 'B' for Box or 'S' for Slice (or 'q' to cancel): ").strip().upper()
            if choice == 'B':
                handle_box_order(pizza_name=name, price=price) # handle box order
                break
            elif choice == 'S':
                handle_slice_order(pizza_name=name, slice_price=slice_price) # handle slice order
                break
            elif choice == 'Q':
                print("Order Cancelled!")
                break
            else:
                print("Select either B, S or q")
    else:
        print("We do not have this the Pizza Flavour for now, maybe later")


# Main Pizze Order System!
def main_system():
    while True:
        print("Welcome to RushMore Pizzeria\nTake a look at our Menu: ")
        # display menu
        for key, value in pizza_data.items():
            print(f"{key}: {value['name']} - ${value['price']}")

        print("Pick your choice from (1-7) and we serve you right away!\nor type in 'q' to quit:")
        # Make a selection
        choice = input("What do you want to pick? ").strip().lower()
        if choice == 'q':
            print("Goodbye and Have a nice day!\n\tCome back another time...")
            break
        elif choice in pizza_data:
            pizza_selection_order(choice) # order handling
        else:
            print("Invalid Input, Please Try Again!")


if __name__ == "__main__":
    main_system()
