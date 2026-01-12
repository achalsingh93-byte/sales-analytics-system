# utils/file_handler.py

def read_sales_file(file_path):
    """
    Reads the sales data file safely by handling encoding issues
    and returns non-empty raw lines.
    """
    lines = []

    try:
        # utf-8-sig handles BOM, errors='replace' avoids crashes
        with open(file_path, mode="r", encoding="utf-8-sig", errors="replace") as file:
            for line in file:
                line = line.strip()
                if line:  # skip empty lines
                    lines.append(line)

    except FileNotFoundError:
        print(f"ERROR: File not found at path: {file_path}")

    except Exception as e:
        print(f"ERROR while reading file: {e}")

    return lines
