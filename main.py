from utils.file_handler import read_sales_data, save_enriched_data
from utils.data_processor import parse_transactions
from utils.api_handler import (
    fetch_all_products,
    create_product_mapping,
    enrich_sales_data
)

def main():
    raw_lines = read_sales_data("data/sales_data.txt")
    transactions = parse_transactions(raw_lines)

    api_products = fetch_all_products()
    product_map = create_product_mapping(api_products)

    enriched = enrich_sales_data(transactions, product_map)
    save_enriched_data(enriched, "data/enriched_sales_data.csv")

    print("Enriched data saved successfully.")

if __name__ == "__main__":
    main()












