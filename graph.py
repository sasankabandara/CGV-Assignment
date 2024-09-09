import matplotlib.pyplot as plt

# Example sales data (could be read from a file or database)
sales_data = {
    'Product A': 150,
    'Product B': 200,
    'Product C': 80,
    'Product D': 120,
}

# Extract product names and sales values
products = list(sales_data.keys())
sales = list(sales_data.values())

# Create a bar chart
plt.bar(products, sales, color='blue')

# Add title and labels
plt.title("Sales Summary")
plt.xlabel("Products")
plt.ylabel("Number of Units Sold")

# Show the graph
plt.show()
