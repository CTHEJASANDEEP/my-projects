from datetime import datetime

# 🧾 Static Data
items = {
    "rice": {"price": 20, "unit": "kg"},
    "sugar": {"price": 30, "unit": "kg"},
    "redbull": {"price": 140, "unit": "pcs"},
    "monsterultra": {"price": 140, "unit": "pcs"},
    "minutemaid": {"price": 25, "unit": "pcs"},
    "salt": {"price": 20, "unit": "kg"},
    "paneer": {"price": 125, "unit": "200g"},
    "maggi": {"price": 60, "unit": "pcs"},
    "yippee": {"price": 60, "unit": "pcs"},
    "pinksalt": {"price": 90, "unit": "kg"},
    "ferrarorocher": {"price": 150, "unit": "pcs"}
}

shoppinglist = "\n".join(
    [f"{item.title():<15} Rs {data['price']}/{data['unit']}" for item, data in items.items()]
)

# ✅ Helper Function
def get_valid_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a valid number.")

# 🚀 Input Initialization
name = input("ENTER YOUR NAME: ").strip()
pricelist = []
totalprice = 0

option = get_valid_int("FOR LIST OF ITEMS PRESS 1: ")
if option == 1:
    print("\nAvailable Items:\n" + shoppinglist + "\n")
    
    while True:
        inp1 = get_valid_int("IF YOU WANT TO BUY PRESS 1 OR 2 FOR EXIT: ")
        if inp1 == 2:
            break
        elif inp1 == 1:
            item = input("ENTER YOUR ITEM: ").strip().lower()
            if item in items:
                quantity = get_valid_int(f"ENTER QUANTITY ({items[item]['unit']}): ")
                unit_price = items[item]["price"]
                price = unit_price * quantity
                pricelist.append({
                    "item": item.title(),
                    "quantity": quantity,
                    "unit": items[item]["unit"],
                    "unit_price": unit_price,
                    "total_price": price
                })
                totalprice += price
                print(f"Price for {quantity} {items[item]['unit']} of {item.title()}: Rs {price}")
            else:
                print("SORRY, THE ITEM YOU ENTERED IS UNAVAILABLE.")
        else:
            print("Invalid input. Please press 1 to buy or 2 to exit.")

    inp = input("\nCAN I BILL THE ITEMS? YES OR NO: ").strip().lower()
    if inp != "yes":
        print("Billing cancelled.")
        exit()

else:
    print("You entered an invalid option. Exiting.")
    exit()

# 💰 Billing
gst = round((totalprice * 2) / 100, 2)
finalamount = totalprice + gst

if finalamount > 0:
    print("\n" + "=" * 25 + " SANDEEP SUPERMARKET " + "=" * 25)
    print(" " * 28 + "DHARMAVARAM")
    print(f"Name: {name:<20} Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 75)
    print("SNO".ljust(6), "ITEM".ljust(15), "QUANTITY".ljust(10), "UNIT".ljust(8), "PRICE")
    for idx, item in enumerate(pricelist, 1):
        print(
            str(idx).ljust(6),
            item["item"].ljust(15),
            str(item["quantity"]).ljust(10),
            item["unit"].ljust(8),
            f"Rs {item['total_price']}"
        )
    print("-" * 75)
    print("Total Amount:".rjust(60), f"Rs {totalprice}")
    print("GST (2%):".rjust(60), f"Rs {gst}")
    print("-" * 80)
    print("Final Amount:".rjust(60), f"Rs {finalamount}")
    print("-" * 75)
    print("THANKS FOR VISITING! :)".rjust(65))
    print("-" * 75)
else:
    print("No items purchased. Thank you for visiting!")
