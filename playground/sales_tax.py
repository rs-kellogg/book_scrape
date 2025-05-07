# Define a function to calculate tax
def calculate_tax(price, tax_rate):
    return price * tax_rate

# Define a simple class for a shopping item
class ShoppingItem:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def total_with_tax(self, tax_rate):
        return self.price + calculate_tax(self.price, tax_rate)

# Create some items
item1 = ShoppingItem("Notebook", 3.50)
item2 = ShoppingItem("Pen", 1.20)


# Set tax rate
tax_rate = 0.07  # 7% tax

# Print total prices
print(f"{item1.name}: ${item1.total_with_tax(tax_rate):.2f}")
print(f"{item2.name}: ${item2.total_with_tax(tax_rate):.2f}")
