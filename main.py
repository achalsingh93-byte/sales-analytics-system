from utils.file_handler import read_sales_file
from utils.data_processor import (
    parse_sales_lines,
    clean_sales_records,
    validate_sales_records
)

def main():
    print("Starting Sales Analytics System...")

    file_path = "data/sales_data.txt"

    lines = read_sales_file(file_path)
    parsed_records = parse_sales_lines(lines)
    cleaned_records = clean_sales_records(parsed_records)
    valid_records, invalid_count = validate_sales_records(cleaned_records)

    print(f"Total records parsed: {len(parsed_records)}")
    print(f"Invalid records removed: {invalid_count}")
    print(f"Valid records after cleaning: {len(valid_records)}")

if __name__ == "__main__":
    main()
