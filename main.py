from utils.file_handler import read_sales_data
from utils.data_processor import parse_transactions, customer_analysis
from utils.api_handler import (
    fetch_all_products,
    create_product_mapping,
    enrich_sales_data
)
from utils.report_generator import generate_sales_report

def main():
    raw = read_sales_data("data/sales_data.txt")
    transactions = parse_transactions(raw)

    api_products = fetch_all_products()
    product_map = create_product_mapping(api_products)
    enriched = enrich_sales_data(transactions, product_map)

    enriched = customer_analysis(enriched)

    generate_sales_report(transactions, enriched)
    print("Customer segmentation written")

if __name__ == "__main__":
    main()













