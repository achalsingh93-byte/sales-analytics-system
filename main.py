from utils.data_processor import (
    read_sales_data,
    parse_transactions,
    validate_and_filter,
    region_wise_sales,
    top_selling_products,
    customer_analysis
)
from utils.api_handler import fetch_all_products
from utils.report_generator import (
    create_report_file,
    write_region_summary,
    write_top_products,
    write_customer_segments,
    write_peak_sales_day
)


def main():
    print("=" * 50)
    print("SALES ANALYTICS SYSTEM – END TO END PIPELINE")
    print("=" * 50)

    # [1/10] Read raw sales data
    print("[1/10] Reading sales data file...")
    raw_lines = read_sales_data("data/sales_data.txt")

    # [2/10] Parse transactions
    print("[2/10] Parsing transactions...")
    transactions = parse_transactions(raw_lines)

    # [3/10] User-driven filters
    min_amount = input("Enter minimum transaction amount (or press Enter to skip): ")
    min_amount = float(min_amount) if min_amount else None

    region = input("Enter region filter (East/West/North/South or press Enter to skip): ")
    region = region if region else None

    # [4/10] Validate & filter
    print("[3/10] Validating and filtering transactions...")
    valid_txns, invalid_count, summary = validate_and_filter(
        transactions,
        region=region,
        min_amount=min_amount
    )

    print("Filter Summary:", summary)

    # [5/10] Fetch product data from API
    print("[4/10] Fetching product data from API...")
    products = fetch_all_products()

    # [6/10] Enrich transactions
    print("[5/10] Enriching transactions with product data...")
    product_map = {p["id"]: p for p in products}

    enriched = []
    for txn in valid_txns:
        product = product_map.get(txn["ProductID"], {})
        txn.update({
            "ProductTitle": product.get("title"),
            "Category": product.get("category"),
            "Brand": product.get("brand"),
            "API_Price": product.get("price"),
            "Rating": product.get("rating")
        })
        enriched.append(txn)

    print(f"Enriched transactions: {len(enriched)}")

    # [7/10] Generate analytics
    region_summary = region_wise_sales(enriched)
    top_products = top_selling_products(enriched)
    customers = customer_analysis(enriched)
    peak_day = max(
        enriched,
        key=lambda x: x["Quantity"] * x["UnitPrice"],
        default=None
    )

    # [8/10] Generate report
    print("[6/10] Generating sales report...")
    report_path = "output/sales_report.txt"
    create_report_file(report_path, len(transactions))

    write_region_summary(report_path, region_summary)
    write_top_products(report_path, top_products)
    write_customer_segments(report_path, customers)
    write_peak_sales_day(report_path, peak_day)

    print("[10/10] Process complete!")
    print("Report saved at:", report_path)


if __name__ == "__main__":
    main()











