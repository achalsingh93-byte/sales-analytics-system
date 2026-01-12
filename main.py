from utils.file_handler import read_sales_data
from utils.data_processor import parse_transactions, validate_and_filter

def main():
    print("Running Sales Analytics System (Q2)...")

    file_path = "data/sales_data.txt"

    raw_lines = read_sales_data(file_path)
    transactions = parse_transactions(raw_lines)

    valid_txns, invalid_count, summary = validate_and_filter(transactions)

    print("\nFinal Summary:")
    print(summary)

if __name__ == "__main__":
    main()




