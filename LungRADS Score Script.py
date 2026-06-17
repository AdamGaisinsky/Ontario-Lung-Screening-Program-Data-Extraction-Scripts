import pandas as pd
import re

# Load Excel file
file_path = "For Adam 11092025.xlsx"  # change to your filename
df = pd.read_excel(file_path, header=None, engine="openpyxl")

results = []

# Iterate over columns
for col in df.columns:
    found = None
    for cell in df[col].dropna():
        text = str(cell)
        if "2. Nodules ACR Lung-RADS Category: '" in text:
            # Extract two characters after the first '
            match = re.search(r"2\. Nodules ACR Lung-RADS Category: '(.{2})", text)
            if match:
                found = match.group(1)
                break  # stop at first match in this column
    # Append result (blank if none found)
    results.append(found if found else "")

# Convert to DataFrame (single column, one row per input column)
output_df = pd.DataFrame(results, columns=["Lung-RADS"])

# Save to Excel
output_df.to_excel("lung_rads_output.xlsx", index=False)

print("Extraction complete! Results saved to lung_rads_output.xlsx")
