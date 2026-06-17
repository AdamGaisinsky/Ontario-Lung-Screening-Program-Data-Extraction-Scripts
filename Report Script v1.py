import pandas as pd
import re

# Load the Excel file (no headers, to treat it as raw data)
input_file = 'Report AllData Sheet.xlsx'  # Replace with your actual file path
df = pd.read_excel(input_file, sheet_name=0, header=None)

# Regex patterns
pattern_a = r"Findings suggestive of an inflammatory process:\s*(.*)"
pattern_total_nodules = r"Number of lung nodules present in total:\s*(\d+)"
pattern_b = r"Number of nodules 4mm or greater:\s*(\d+)"
pattern_other_comments = r"Other comments \(Including nodules less than 4 mm\):\s*(.*)"

# Incidental Findings headings
incidental_headings = [
    "1. Lung or Pleura",
    "2. Emphysema",
    "3. Mediastinum and Hila",
    "4. Coronary Artery Calcification",
    "5. Chest Wall and Axilla",
    "6. Bones",
    "7. Upper Abdomen",
    "8. Other"
]
incidental_patterns = {
    heading: re.compile(re.escape(heading) + r":\s*(.*)", re.IGNORECASE)
    for heading in incidental_headings
}

# Impression section patterns
pattern_summary = r"1\. Pulmonary nodule summary:\s*(.*)"
pattern_lung_rads = r"2\. Nodules ACR Lung-RADS Category:\s*'?([0-9]+)"

# Actionable incidental findings
pattern_actionable = {
    "a) Actionable incidental findings": r"a\) Actionable incidental findings:\s*(.*)",
    "b) Actionable incidental finding (reiterate incidental finding(s))": r"b\) Actionable incidental finding \(reiterate incidental finding\(s\)\):\s*(.*)",
    "c) Recommendation for follow-up": r"c\) Recommendation for follow-up:\s*(.*)"
}

# Other Comments
pattern_other = r"4\. \+Other Comments:\s*(.*)"

# Process each patient (each column is a patient)
patient_data = []
for col in df.columns:
    # Initialize extracted values for each patient
    study_id = str(df.iloc[1, col]).strip() if len(df) > 1 else None
    findings_inflammatory = None
    total_nodules = None
    nodule_count = None
    other_comments = None
    pulmonary_summary = None
    lung_rads_category = None
    actionable_data = {key: None for key in pattern_actionable.keys()}
    incidental_data = {heading: None for heading in incidental_headings}
    other_section = None

    # Search through all rows of this column
    for row in range(len(df)):
        cell = str(df.iloc[row, col]).strip()

        if findings_inflammatory is None:
            match_a = re.search(pattern_a, cell, re.IGNORECASE)
            if match_a:
                findings_inflammatory = match_a.group(1).strip()

        if total_nodules is None:
            match_total = re.search(pattern_total_nodules, cell, re.IGNORECASE)
            if match_total:
                total_nodules = int(match_total.group(1))

        if nodule_count is None:
            match_b = re.search(pattern_b, cell, re.IGNORECASE)
            if match_b:
                nodule_count = int(match_b.group(1))

        if other_comments is None:
            match_oc = re.search(pattern_other_comments, cell, re.IGNORECASE)
            if match_oc:
                other_comments = match_oc.group(1).strip()

        for heading, pattern in incidental_patterns.items():
            if incidental_data[heading] is None:
                match = pattern.search(cell)
                if match:
                    incidental_data[heading] = match.group(1).strip()

        if pulmonary_summary is None:
            match_summary = re.search(pattern_summary, cell, re.IGNORECASE)
            if match_summary:
                pulmonary_summary = match_summary.group(1).strip()

        if lung_rads_category is None:
            match_rads = re.search(pattern_lung_rads, cell, re.IGNORECASE)
            if match_rads:
                lung_rads_category = match_rads.group(1).strip()

        for key, pat in pattern_actionable.items():
            if actionable_data[key] is None:
                match_act = re.search(pat, cell, re.IGNORECASE)
                if match_act:
                    actionable_data[key] = match_act.group(1).strip()

        if other_section is None:
            match_other = re.search(pattern_other, cell, re.IGNORECASE)
            if match_other:
                other_section = match_other.group(1).strip()

    # Build row for this patient
    data = {
        'Study ID': study_id,
        'Findings suggestive of an inflammatory process': findings_inflammatory,
        'Number of lung nodules present in total': total_nodules,
        'Number of nodules 4mm or greater': nodule_count,
        'Other comments (Including nodules less than 4 mm)': other_comments,
        '1. Pulmonary nodule summary': pulmonary_summary,
        '2. Nodules ACR Lung-RADS Category': lung_rads_category,
    }

    data.update(incidental_data)
    data.update(actionable_data)
    data['4. +Other Comments'] = other_section

    patient_data.append(data)

# Create final DataFrame and export
output_df = pd.DataFrame(patient_data)
output_file = 'Report AllData nodule.xlsx'
output_df.to_excel(output_file, index=False)

print(f"All patient findings extracted and saved to '{output_file}'")
