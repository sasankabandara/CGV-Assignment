import re
import matplotlib.pyplot as plt
import seaborn as sns
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def read_sales_data(file_path):
    """
    Reads the sales data from the text file and returns a dictionary of product-sales.
    """
    sales_dict = {}
    with open(file_path, 'r') as f:
        for line in f:
            # Skip empty lines and header lines
            if line.strip() == "" or 'Extracted Text Summary' in line:
                continue
            # Use regular expression to extract product and sales
            match = re.match(r'(.+?):\s*([\d,]+)', line)
            if match:
                product = match.group(1).strip()
                sales = match.group(2).replace(',', '').strip()
                try:
                    sales = int(sales)
                    sales_dict[product] = sales
                except ValueError:
                    logging.warning(f"Could not convert sales value '{sales}' for product '{product}' to integer.")
            else:
                logging.warning(f"Line '{line.strip()}' does not match the expected format.")
    return sales_dict

def plot_sales_bar_chart(sales_data, save=False):
    """
    Plots a bar chart of sales data.
    """
    products = list(sales_data.keys())
    sales = list(sales_data.values())

    plt.figure(figsize=(10, 6))
    sns.barplot(x=products, y=sales, palette='Blues_d')
    plt.title('Sales Summary by Product')
    plt.xlabel('Product')
    plt.ylabel('Sales Amount')
    plt.xticks(rotation=45)
    plt.tight_layout()
    if save:
        plt.savefig('sales_bar_chart.png')
    plt.show()

def plot_sales_pie_chart(sales_data, save=False):
    """
    Plots a pie chart of sales data.
    """
    products = list(sales_data.keys())
    sales = list(sales_data.values())

    plt.figure(figsize=(8, 8))
    plt.pie(sales, labels=products, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
    plt.title('Sales Distribution by Product')
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    if save:
        plt.savefig('sales_pie_chart.png')
    plt.show()

def plot_sales_line_chart(sales_data, save=False):
    """
    (Optional) Plots a line chart of sales data.
    """
    products = list(sales_data.keys())
    sales = list(sales_data.values())

    plt.figure(figsize=(10, 6))
    sns.lineplot(x=products, y=sales, marker='o')
    plt.title('Sales Trend by Product')
    plt.xlabel('Product')
    plt.ylabel('Sales Amount')
    plt.xticks(rotation=45)
    plt.tight_layout()
    if save:
        plt.savefig('sales_line_chart.png')
    plt.show()

def main():
    # Path to the extracted text summary file
    file_path = 'extracted_text_summary.txt'

    # Read and parse the sales data
    sales_data = read_sales_data(file_path)

    if not sales_data:
        logging.error("No valid sales data found. Please check the input file format.")
        return

    logging.info("Extracted Sales Data:")
    for product, sales in sales_data.items():
        logging.info(f"{product}: {sales}")

    # Plotting
    plot_sales_bar_chart(sales_data, save=True)
    plot_sales_pie_chart(sales_data, save=True)
    # Uncomment the following line if you wish to plot a line chart
    # plot_sales_line_chart(sales_data, save=True)

if _name_ == "_main_":
    main()