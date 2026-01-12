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
