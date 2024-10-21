#Art Item Class
class ArtItem:
    def __init__(self, item_id, title, artist, year, price, quantity_in_stock, status="For Sale"):
        self.item_id = item_id
        self.title = title
        self.artist = artist
        self.year = year
        self.price = price
        self.quantity_in_stock = quantity_in_stock
        self.status = status

    def apply_discount(self, discount_percentage):
        self.price = self.price - (self.price * discount_percentage / 100)

    def is_available(self):
        return self.quantity_in_stock > 0

    def update_status(self, new_status):
        self.status = new_status

    def __str__(self):
        return f"{self.title} by {self.artist} ({self.year}) | Price: ${self.price:.2f} | Status: {self.status}"

#Inventory Class
class Inventory:
    def __init__(self):
        self.art_items = {}

    def add_item(self, art_item):
        if art_item.item_id not in self.art_items:
            self.art_items[art_item.item_id] = art_item
            print(f"Added {art_item.title} to the inventory.")
        else:
            print("Item ID already exists.")

    def remove_item(self, item_id):
        if item_id in self.art_items:
            removed_item = self.art_items.pop(item_id)
            print(f"Removed {removed_item.title} from the inventory.")
        else:
            print("Item ID not found.")

    def update_item(self, item_id, title=None, artist=None, year=None, price=None, quantity=None, status=None):
        if item_id in self.art_items:
            art_item = self.art_items[item_id]
            if title:
                art_item.title = title
            if artist:
                art_item.artist = artist
            if year:
                art_item.year = year
            if price:
                art_item.price = price
            if quantity:
                art_item.quantity_in_stock = quantity
            if status:
                art_item.status = status
            print(f"Updated {art_item.title}.")
        else:
            print("Item ID not found.")

    def view_items(self):
        for art_item in self.art_items.values():
            print(art_item)

    def search_by_artist(self, artist_name):
        result = [item for item in self.art_items.values() if item.artist.lower() == artist_name.lower()]
        return result

#Report Class
class Report:
    def generate_inventory_report(self, inventory):
        print("Inventory Report:")
        for item in inventory.art_items.values():
            print(f"{item.title} by {item.artist}, {item.year} | Quantity: {item.quantity_in_stock} | Price: ${item.price:.2f}")

    def generate_sales_report(self, inventory):
        print("Sales Report (Sold Items):")
        sold_items = [item for item in inventory.art_items.values() if item.status.lower() == "sold"]
        total_revenue = sum(item.price for item in sold_items)
        for item in sold_items:
            print(f"{item.title} by {item.artist}, sold for ${item.price:.2f}")
        print(f"Total Revenue: ${total_revenue:.2f}")

    def filter_by_availability(self, inventory):
        available_items = [item for item in inventory.art_items.values() if item.is_available()]
        print("Available Items:")
        for item in available_items:
            print(item)

    def generate_price_report(self, inventory, min_price, max_price):
        print(f"Items priced between ${min_price:.2f} and ${max_price:.2f}:")
        filtered_items = [item for item in inventory.art_items.values() if min_price <= item.price <= max_price]
        for item in filtered_items:
            print(item)

import json

class DataPersistence:
    def __init__(self, filename):
        self.filename = filename

    def save_to_file(self, inventory):
        data = {item_id: item.__dict__ for item_id, item in inventory.art_items.items()}
        with open(self.filename, 'w') as file:
            json.dump(data, file)
        print(f"Inventory saved to {self.filename}.")

    def load_from_file(self, inventory):
        try:
            with open(self.filename, 'r') as file:
                data = json.load(file)
                for item_data in data.values():
                    item = ArtItem(**item_data)
                    inventory.add_item(item)
            print(f"Inventory loaded from {self.filename}.")
        except FileNotFoundError:
            print("File not found.")

# Example 

inventory = Inventory()

art_item1 = ArtItem(1, "Starry Night", "Vincent Van Gogh", 1889, 1000000, 1)
art_item2 = ArtItem(2, "The Kiss", "Gustav Klimt", 1908, 2000000, 1)
art_item3 = ArtItem(3, "Mona Lisa", "Leonardo da Vinci", 1503, 850000000, 1)

inventory.add_item(art_item1)
inventory.add_item(art_item2)
inventory.add_item(art_item3)

report = Report()
report.generate_inventory_report(inventory)
report.filter_by_availability(inventory)

art_item1.apply_discount(10)
art_item1.update_status("Sold")

report.generate_sales_report(inventory)

data_persistence = DataPersistence('art_inventory.json')
data_persistence.save_to_file(inventory)

new_inventory = Inventory()
data_persistence.load_from_file(new_inventory)

new_inventory.view_items()
