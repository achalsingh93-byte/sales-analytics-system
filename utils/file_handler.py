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
def read_sales_data(filename):
    """
    Reads sales data from file handling encoding issues.
    Returns list of raw transaction lines (without header).
    """
    encodings = ["utf-8", "latin-1", "cp1252"]

    for encoding in encodings:
        try:
            with open(filename, mode="r", encoding=encoding) as file:
                lines = file.readlines()

            cleaned_lines = []
            for line in lines[1:]:  # skip header
                line = line.strip()
                if line:
                    cleaned_lines.append(line)

            return cleaned_lines

        except UnicodeDecodeError:
            continue
        except FileNotFoundError:
            print(f"ERROR: File not found -> {filename}")
            return []
        except Exception as e:
            print(f"ERROR while reading file: {e}")
            return []

    print("ERROR: Unable to read file with supported encodings.")
    return []
