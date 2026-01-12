# utils/data_processor.py

def parse_sales_lines(lines):
    """
    Parses raw sales lines into structured records.
    Skips header and malformed rows.
    """
    parsed_records = []

    header = lines[0]  # first line is header
    expected_fields = len(header.split("|"))

    for line in lines[1:]:  # skip header
        fields = line.split("|")

        # Skip rows with incorrect number of fields
        if len(fields) != expected_fields:
            continue

        parsed_records.append(fields)

    return parsed_records
def clean_sales_records(records):
    """
    Cleans parsed sales records:
    - Removes commas from ProductName
    - Converts Quantity and UnitPrice to integers
    """
    cleaned_records = []

    for record in records:
        transaction_id, date, product_id, product_name, quantity, unit_price, customer_id, region = record

        # Clean product name (remove commas)
        product_name = product_name.replace(",", "").strip()

        # Clean numeric fields
        try:
            quantity = int(quantity)
            unit_price = int(unit_price.replace(",", ""))
        except ValueError:
            # Skip records where numeric conversion fails
            continue

        cleaned_records.append([
            transaction_id,
            date,
            product_id,
            product_name,
            quantity,
            unit_price,
            customer_id,
            region
        ])

    return cleaned_records
def validate_sales_records(records):
    """
    Applies validation rules to cleaned records.
    Returns valid records and invalid count.
    """
    valid_records = []
    invalid_count = 0

    for record in records:
        transaction_id, date, product_id, product_name, quantity, unit_price, customer_id, region = record

        # Validation rules
        if not transaction_id.startswith("T"):
            invalid_count += 1
            continue

        if quantity <= 0 or unit_price <= 0:
            invalid_count += 1
            continue

        if not customer_id or not region:
            invalid_count += 1
            continue

        valid_records.append(record)

    return valid_records, invalid_count
def parse_transactions(raw_lines):
    """
    Parses raw sales lines into a clean list of dictionaries.
    """
    transactions = []

    for line in raw_lines:
        fields = line.split("|")

        # Skip malformed rows
        if len(fields) != 8:
            continue

        (
            transaction_id,
            date,
            product_id,
            product_name,
            quantity,
            unit_price,
            customer_id,
            region
        ) = fields

        # Clean product name
        product_name = product_name.replace(",", "").strip()

        # Clean numeric fields
        try:
            quantity = int(quantity)
            unit_price = float(unit_price.replace(",", ""))
        except ValueError:
            continue

        transaction = {
            "TransactionID": transaction_id,
            "Date": date,
            "ProductID": product_id,
            "ProductName": product_name,
            "Quantity": quantity,
            "UnitPrice": unit_price,
            "CustomerID": customer_id,
            "Region": region
        }

        transactions.append(transaction)

    return transactions
def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    """
    Validates transactions and applies optional filters.
    Returns (valid_transactions, invalid_count, summary)
    """
    valid_transactions = []
    invalid_count = 0

    regions_available = set()
    amounts = []

    # ---------- VALIDATION ----------
    for txn in transactions:
        try:
            if not txn["TransactionID"].startswith("T"):
                invalid_count += 1
                continue

            if not txn["ProductID"].startswith("P"):
                invalid_count += 1
                continue

            if not txn["CustomerID"].startswith("C"):
                invalid_count += 1
                continue

            if not txn["Region"]:
                invalid_count += 1
                continue

            if txn["Quantity"] <= 0 or txn["UnitPrice"] <= 0:
                invalid_count += 1
                continue

            regions_available.add(txn["Region"])
            amounts.append(txn["Quantity"] * txn["UnitPrice"])
            valid_transactions.append(txn)

        except KeyError:
            invalid_count += 1
            continue

    # ---------- DISPLAY INFO ----------
    print("Available Regions:", sorted(regions_available))
    if amounts:
        print(f"Transaction Amount Range: {min(amounts)} - {max(amounts)}")

    # ---------- FILTERING ----------
    filtered_transactions = valid_transactions
    filtered_by_region = 0
    filtered_by_amount = 0

    if region:
        before = len(filtered_transactions)
        filtered_transactions = [
            t for t in filtered_transactions if t["Region"] == region
        ]
        filtered_by_region = before - len(filtered_transactions)

    if min_amount is not None:
        before = len(filtered_transactions)
        filtered_transactions = [
            t for t in filtered_transactions
            if (t["Quantity"] * t["UnitPrice"]) >= min_amount
        ]
        filtered_by_amount += before - len(filtered_transactions)

    if max_amount is not None:
        before = len(filtered_transactions)
        filtered_transactions = [
            t for t in filtered_transactions
            if (t["Quantity"] * t["UnitPrice"]) <= max_amount
        ]
        filtered_by_amount += before - len(filtered_transactions)

    summary = {
        "total_input": len(transactions),
        "invalid": invalid_count,
        "filtered_by_region": filtered_by_region,
        "filtered_by_amount": filtered_by_amount,
        "final_count": len(filtered_transactions)
    }

    return filtered_transactions, invalid_count, summary
def calculate_total_revenue(transactions):
    """
    Calculates total revenue from all transactions
    Returns: float
    """
    total_revenue = 0.0

    for txn in transactions:
        total_revenue += txn["Quantity"] * txn["UnitPrice"]

    return total_revenue
def region_wise_sales(transactions):
    """
    Calculates region-wise sales summary.
    Returns a list of dictionaries sorted by revenue descending.
    """
    region_summary = {}
    total_revenue = 0.0

    for txn in transactions:
        total_revenue += txn["Quantity"] * txn["UnitPrice"]

    for txn in transactions:
        region = txn["Region"]

        # Skip empty region
        if not region:
            continue

        revenue = txn["Quantity"] * txn["UnitPrice"]

        if region not in region_summary:
            region_summary[region] = {
                "Region": region,
                "Revenue": 0.0,
                "Transactions": 0
            }

        region_summary[region]["Revenue"] += revenue
        region_summary[region]["Transactions"] += 1

    result = []
    for data in region_summary.values():
        percentage = (
            (data["Revenue"] / total_revenue) * 100
            if total_revenue > 0 else 0
        )
        data["Percentage"] = round(percentage, 2)
        result.append(data)

    result.sort(key=lambda x: x["Revenue"], reverse=True)
    return result
def top_selling_products(transactions, top_n=5):
    """
    Returns top N selling products by quantity.
    """
    product_summary = {}

    for txn in transactions:
        product = txn["ProductName"]
        quantity = txn["Quantity"]
        revenue = txn["Quantity"] * txn["UnitPrice"]

        if product not in product_summary:
            product_summary[product] = {
                "ProductName": product,
                "TotalQuantity": 0,
                "Revenue": 0.0
            }

        product_summary[product]["TotalQuantity"] += quantity
        product_summary[product]["Revenue"] += revenue

    result = list(product_summary.values())
    result.sort(key=lambda x: x["TotalQuantity"], reverse=True)

    return result[:top_n]
def customer_analysis(transactions):
    """
    Performs customer-wise analysis and segmentation.
    Returns a list of customer summaries.
    """
    customer_summary = {}

    for txn in transactions:
        customer = txn["CustomerID"]
        spend = txn["Quantity"] * txn["UnitPrice"]

        if customer not in customer_summary:
            customer_summary[customer] = {
                "CustomerID": customer,
                "TotalSpend": 0.0,
                "Transactions": 0
            }

        customer_summary[customer]["TotalSpend"] += spend
        customer_summary[customer]["Transactions"] += 1

    result = []
    for data in customer_summary.values():
        if data["TotalSpend"] >= 50000:
            segment = "High Value"
        elif data["TotalSpend"] >= 10000:
            segment = "Medium Value"
        else:
            segment = "Low Value"

        data["Segment"] = segment
        result.append(data)

    return result
def daily_sales_trend(transactions):
    """
    Calculates daily sales revenue.
    Returns a dictionary with Date as key and TotalRevenue as value.
    """
    daily_sales = {}

    for txn in transactions:
        date = txn["Date"]
        revenue = txn["Quantity"] * txn["UnitPrice"]

        if date not in daily_sales:
            daily_sales[date] = 0.0

        daily_sales[date] += revenue

    return daily_sales
def find_peak_sales_day(daily_sales):
    """
    Identifies the day with the highest sales.
    Returns a tuple (date, revenue).
    """
    if not daily_sales:
        return None, 0.0

    peak_date = max(daily_sales, key=daily_sales.get)
    peak_revenue = daily_sales[peak_date]

    return peak_date, peak_revenue
def low_performing_products(transactions, threshold=10):
    """
    Identifies products with total quantity sold below the given threshold.
    Returns a list of product summaries.
    """
    product_summary = {}

    for txn in transactions:
        product = txn["ProductName"]
        quantity = txn["Quantity"]
        revenue = txn["Quantity"] * txn["UnitPrice"]

        if product not in product_summary:
            product_summary[product] = {
                "ProductName": product,
                "TotalQuantity": 0,
                "Revenue": 0.0
            }

        product_summary[product]["TotalQuantity"] += quantity
        product_summary[product]["Revenue"] += revenue

    low_products = [
        data for data in product_summary.values()
        if data["TotalQuantity"] < threshold
    ]

    return low_products


