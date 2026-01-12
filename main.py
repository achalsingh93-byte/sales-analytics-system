def main():
    try:
        print("=" * 40)
        print("SALES ANALYTICS SYSTEM")
        print("=" * 40)

        print("[1/10] Initializing system...")

        print("[2/10] Reading sales data file...")
        from utils.file_handler import read_sales_data
        raw_lines = read_sales_data("data/sales_data.txt")
        print(f"      Lines read (including header): {len(raw_lines)}")

        print("[3/10] Parsing transactions...")
        from utils.data_processor import parse_transactions
        transactions = parse_transactions(raw_lines)
        print(f"      Parsed transactions: {len(transactions)}")
        print("[4/10] Applying validation & filters...")

        from utils.data_processor import validate_and_filter

        # User inputs (optional)
        region_input = input("Enter region to filter (or press Enter to skip): ").strip()
        region = region_input if region_input else None

        min_amount_input = input("Enter minimum transaction amount (or press Enter to skip): ").strip()
        min_amount = float(min_amount_input) if min_amount_input else None

        filtered_transactions, invalid_count, summary = validate_and_filter(
            transactions,
            region=region,
            min_amount=min_amount
        )

        print("      Filter Summary:")
        print(f"         Total Input: {summary.get('total_input')}")
        print(f"         Invalid Records: {invalid_count}")
        print(f"         Final Valid Transactions: {summary.get('final_count')}")
        print("[5/10] Fetching product data from API...")
        from utils.api_handler import (
            fetch_all_products,
            create_product_mapping,
            enrich_sales_data
        )

        api_products = fetch_all_products()
        product_map = create_product_mapping(api_products)
        print(f"      API products fetched: {len(api_products)}")

        print("[6/10] Enriching transactions with product data...")
        enriched_transactions = enrich_sales_data(filtered_transactions, product_map)
        print(f"      Enriched transactions: {len(enriched_transactions)}")
        print("[7/10] Saving enriched data to file...")
        from utils.file_handler import save_enriched_data

        save_enriched_data(enriched_transactions, "data/enriched_sales_data.csv")
        print("      Enriched data file saved")
        print("[8/10] Generating final report...")

        print("\n========= FINAL EXECUTION SUMMARY =========")
        print(f"Total Input Records      : {summary['total_input']}")
        print(f"Invalid Records          : {summary['invalid']}")
        print(f"Final Valid Transactions : {len(filtered_transactions)}")
        print(f"Enriched Transactions    : {len(enriched_transactions)}")

        print("[10/10] Process Complete!")
        print("=" * 40)

    except Exception as e:
        print("❌ An unexpected error occurred.")
        print(str(e))


if __name__ == "__main__":
    main()
    print("\n[10/10] Sales Analytics Pipeline Completed Successfully!")
    print("===========================================")













