# utils/api_handler.py

import requests

def fetch_all_products():
    """
    Fetches all products from DummyJSON API
    Returns: list of product dictionaries
    """
    url = "https://dummyjson.com/products?limit=100"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()
        products = data.get("products", [])

        result = []
        for p in products:
            result.append({
                "id": p.get("id"),
                "title": p.get("title"),
                "category": p.get("category"),
                "brand": p.get("brand"),
                "price": p.get("price"),
                "rating": p.get("rating")
            })

        return result

    except requests.exceptions.RequestException as e:
        print(f"API ERROR: {e}")
        return []
def create_product_mapping(api_products):
    """
    Creates a dictionary mapping product ID to product details.
    Returns: dict
    """
    product_mapping = {}

    for product in api_products:
        product_id = product.get("id")
        if product_id is not None:
            product_mapping[product_id] = product

    return product_mapping
def extract_numeric_product_id(product_id):
    """
    Extracts numeric product ID from sales ProductID (e.g., 'P107' -> 107)
    Returns integer or None if invalid
    """
    if not product_id or not product_id.startswith("P"):
        return None

    numeric_part = product_id[1:]

    if numeric_part.isdigit():
        return int(numeric_part)

    return None
def enrich_sales_data(transactions, product_mapping):
    """
    Enriches sales transactions with API product details.
    Returns list of enriched transactions.
    """
    enriched_transactions = []

    for txn in transactions:
        enriched_txn = txn.copy()

        numeric_id = extract_numeric_product_id(txn.get("ProductID"))
        product = product_mapping.get(numeric_id)

        if product:
            enriched_txn["ProductTitle"] = product.get("title")
            enriched_txn["Category"] = product.get("category")
            enriched_txn["Brand"] = product.get("brand")
            enriched_txn["API_Price"] = product.get("price")
            enriched_txn["Rating"] = product.get("rating")
        else:
            enriched_txn["ProductTitle"] = None
            enriched_txn["Category"] = None
            enriched_txn["Brand"] = None
            enriched_txn["API_Price"] = None
            enriched_txn["Rating"] = None

        enriched_transactions.append(enriched_txn)

    return enriched_transactions
