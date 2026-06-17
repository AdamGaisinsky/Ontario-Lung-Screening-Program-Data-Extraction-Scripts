import pandas as pd
import re

# ==== CONFIGURE THESE ====
input_file = "Book1.xlsx"
sheet_name = 0       # or the sheet name as a string, e.g. "Sheet1"
output_file = "nodule_summary.xlsx"
# =========================

# Read everything as data (since patients are in columns, not rows)
df = pd.read_excel(input_file, sheet_name=sheet_name, header=0)

search_terms = [
    "Number of lung nodules present in total:",
    "Number of nodules 4mm or greater:"
]

def extract_first_value_after_colon(text, key):
    """
    From a cell's text, extract the first integer or 'None' appearing
    after the colon in `key`. If a '(' is reached before any such match,
    return '' (blank). Handles values like ___5______ by pulling out 5.
    """
    if not isinstance(text, str):
        return ""

    # Ensure the key is actually in this text
    if key not in text:
        return ""

    # Everything after the *first* colon
    parts = text.split(":", 1)
    if len(parts) < 2:
        return ""
    after_colon = parts[1]

    # Stop at '(' if it appears before any valid value
    before_paren = after_colon.split("(", 1)[0]

    # Look for either 'None' or a number
    match = re.search(r'\b(None|\d+)\b', before_paren, flags=re.IGNORECASE)
    if not match:
        return ""

    value = match.group(1)
    if value.lower() == "none":
        return "None"

    # Return just the number (as a string to keep type consistent with "None")
    return value

# Prepare result storage
results = {term: [] for term in search_terms}
patient_ids = []

# Loop over each column (each patient)
for col in df.columns:
    col_series = df[col].astype(str)
    patient_ids.append(col)

    # For each search term, find the corresponding cell and extract the value
    for term in search_terms:
        # Find rows where this term appears in the text
        mask = col_series.str.contains(term, na=False)
        if not mask.any():
            # Term not found in this patient column -> blank
            results[term].append("")
            continue

        # Take the first matching cell
        cell_text = col_series[mask].iloc[0]

        # Extract the number or 'None' according to your rules
        extracted = extract_first_value_after_colon(cell_text, term)
        results[term].append(extracted)

# Build the output DataFrame
output_df = pd.DataFrame(results, index=patient_ids)
output_df.index.name = "Patient"

# Save to Excel
output_df.to_excel(output_file)

print("Done! Summary saved to:", output_file)
