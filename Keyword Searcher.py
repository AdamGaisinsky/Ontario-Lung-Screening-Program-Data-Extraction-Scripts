import pandas as pd

# Load Excel file
df = pd.read_excel("Report Data 11092025 v1.xlsx")

# Define keywords and their corresponding output codes
keywords_map = {
    "respiratory bronchiolitis": "RB",
    "clustered nodule": "CLN",
    "clustered": "CL",
    "solid nodule": "SN",
    "inflammatory": "INF",
    "inflammation": "INF",
    "ground-glass": "GG",
    "groundglass": "GG",
    "ground glass": "GG",
    "ground-glass opacit": "GGO",
    "groundglass opacit": "GGO",
    "ground glass opacit": "GGO",
    "tree-in-bud": "TIB",
    "consolidation": "CON",
    "pneumonia": "PNEU",
    "infectio": "INFEC",
}

# Column order with new SN added
ordered_codes = ["RB", "CL", "CLN", "SN", "INF", "GG", "GGO", "TIB", "CON", "PNEU", "INFEC"]

# Function to check for all keywords in a row
def check_keywords(row):
    row_text = " ".join(row.astype(str)).lower()
    found_codes = []
    row_results = {code: "" for code in ordered_codes}
    for keyword, code in keywords_map.items():
        if keyword.lower() in row_text:
            if row_results[code] == "":  # avoid duplicates
                row_results[code] = code
                found_codes.append(code)
    return " ".join(found_codes), row_results

# Apply function across rows
combined_flags = []
per_keyword_results = {code: [] for code in ordered_codes}

for _, row in df.iterrows():
    combined, row_results = check_keywords(row)
    combined_flags.append(combined)
    for code in ordered_codes:
        per_keyword_results[code].append(row_results[code])

# Add combined column
df["Keyword_Flag"] = combined_flags

# Add individual keyword columns (in fixed order)
for code in ordered_codes:
    df[code] = per_keyword_results[code]

# Add combo columns
df["CL+INF"] = df.apply(lambda r: "CL+INF" if r["CL"] and r["INF"] else "", axis=1)
df["CLN+INF"] = df.apply(lambda r: "CLN+INF" if r["CLN"] and r["INF"] else "", axis=1)
df["GG+INF"] = df.apply(lambda r: "GG+INF" if r["GG"] and r["INF"] else "", axis=1)
df["GGO+INF"] = df.apply(lambda r: "GGO+INF" if r["GGO"] and r["INF"] else "", axis=1)

# Add Rightmost_Flag column
def get_rightmost_flag(flags):
    if not flags:
        return ""
    codes = flags.split()
    for code in reversed(ordered_codes):  # check from rightmost priority
        if code in codes:
            return code
    return ""

df["Rightmost_Flag"] = df["Keyword_Flag"].apply(get_rightmost_flag)

# Save to new Excel file
df.to_excel("output_with_flags.xlsx", index=False)
