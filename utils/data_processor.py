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
