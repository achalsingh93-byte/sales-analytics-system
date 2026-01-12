from datetime import datetime

def generate_sales_report(
    transactions,
    enriched_transactions,
    output_file="output/sales_report.txt"
):
    """
    Generates a comprehensive formatted sales report
    """
    with open(output_file, "w", encoding="utf-8") as f:
        # Header
        f.write("SALES ANALYTICS REPORT\n")
        f.write("=" * 30 + "\n")
        f.write(f"Generated On: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Total Transactions Processed: {len(transactions)}\n")
        f.write("\n")
        # Section 1: Region-wise Sales Summary
        f.write("REGION-WISE SALES SUMMARY\n")
        f.write("-" * 30 + "\n")

        region_summary = {}

        for txn in transactions:
            region = txn.get("Region")
            amount = txn.get("Quantity", 0) * txn.get("UnitPrice", 0)

            if region not in region_summary:
                region_summary[region] = {
                    "revenue": 0.0,
                    "transactions": 0
                }

            region_summary[region]["revenue"] += amount
            region_summary[region]["transactions"] += 1

        for region, data in region_summary.items():
            f.write(
                f"Region: {region} | "
                f"Revenue: {data['revenue']:.2f} | "
                f"Transactions: {data['transactions']}\n"
            )

        f.write("\n")
        # Section 2: Top Selling Products
        f.write("TOP SELLING PRODUCTS\n")
        f.write("-" * 30 + "\n")

        product_sales = {}

        for txn in transactions:
            product = txn.get("ProductName")
            amount = txn.get("Quantity", 0) * txn.get("UnitPrice", 0)

            if product not in product_sales:
                product_sales[product] = 0.0

            product_sales[product] += amount

        top_products = sorted(
            product_sales.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]

        for idx, (product, revenue) in enumerate(top_products, start=1):
            f.write(f"{idx}. {product} | Revenue: {revenue:.2f}\n")

        f.write("\n")
        # Section 3: Customer Segmentation Summary
        f.write("CUSTOMER SEGMENTATION SUMMARY\n")
        f.write("-" * 30 + "\n")

        segment_count = {}

        for txn in enriched_transactions:
            segment = txn.get("Segment")
            if segment:
                segment_count[segment] = segment_count.get(segment, 0) + 1

        for segment, count in segment_count.items():
            f.write(f"{segment}: {count} customers\n")

        f.write("\n")
        # Section 4: Peak Sales Day
        f.write("PEAK SALES DAY\n")
        f.write("-" * 30 + "\n")

        daily_sales = {}

        for txn in transactions:
            date = txn.get("Date")
            amount = txn.get("Quantity", 0) * txn.get("UnitPrice", 0)
            daily_sales[date] = daily_sales.get(date, 0) + amount

        peak_date = max(daily_sales, key=daily_sales.get)
        peak_revenue = daily_sales[peak_date]

        f.write(f"Peak Sales Date: {peak_date}\n")
        f.write(f"Revenue: {peak_revenue:.2f}\n\n")
        # Footer
        f.write("=" * 30 + "\n")
        f.write("END OF REPORT\n")

