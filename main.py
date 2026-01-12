from utils.file_handler import read_sales_data
from utils.data_processor import (
    parse_transactions,
    low_performing_products
)

def main():
    raw_lines = read_sales_data("data/sales_data.txt")
    transactions = parse_transactions(raw_lines)

    low_products = low_performing_products(transactions, threshold=10)

    print("Low Performing Products:")
    for p in low_products:
        print(p)

if __name__ == "__main__":
    main()









