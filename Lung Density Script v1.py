import pandas as pd
from collections import OrderedDict

def is_measurement_header(cell):
    if pd.isna(cell):
        return False
    return str(cell).strip().startswith("MEASUREMENTS,")

def extract_section(cell):
    return str(cell).split(",", 1)[1].strip()

def split_measurement(cell):
    parts = [p.strip() for p in str(cell).split(",")]
    if len(parts) == 3:
        return parts[0], parts[1], parts[2]   # heading, value, unit
    elif len(parts) == 2:
        return parts[0], parts[1], ""        # heading, value, no unit
    return None, None, None

def process_excel(input_file, output_file):
    df = pd.read_excel(input_file, header=None)

    section_order = ['Both Lungs', 'Right Lung', 'Left Lung']

    # ✅ Extract metadata rows (full cell contents)
    study_ids      = df.iloc[0, :].tolist()  # row 1
    risk_dates     = df.iloc[1, :].tolist()  # row 2
    ct_dates       = df.iloc[5, :].tolist()  # row 6
    sexes          = df.iloc[2, :].tolist()  # row 3
    ages           = df.iloc[3, :].tolist()  # row 4
    risk_scores    = df.iloc[4, :].tolist()  # row 5

    # Global heading→unit mapping
    global_section_measurement_order = {section: [] for section in section_order}
    global_units = {}

    # Process each column (patient)
    patient_data = []
    for col_idx, col in enumerate(df.columns):
        current_section = None
        section_data = {section: OrderedDict() for section in section_order}

        for cell in df[col]:
            if is_measurement_header(cell):
                current_section = extract_section(cell)
            elif current_section:
                heading, value, unit = split_measurement(cell)
                if heading and value:
                    combined_heading = f"{heading} ({current_section})"

                    # Record heading + unit globally
                    if heading not in global_section_measurement_order[current_section]:
                        global_section_measurement_order[current_section].append(heading)
                    if combined_heading not in global_units and unit:
                        global_units[combined_heading] = unit

                    section_data[current_section][combined_heading] = value

        # Append all metadata + measurements for this patient
        patient_data.append((
            study_ids[col_idx],
            risk_dates[col_idx],
            ct_dates[col_idx],
            sexes[col_idx],
            ages[col_idx],
            risk_scores[col_idx],
            section_data
        ))

    # Build final column order
    final_column_order = [
        "Study ID",
        "Risk Assessment Date",
        "CT Date",
        "ParticipantSex",
        "Age (years)",
        "Risk Score (%)"
    ]
    for section in section_order:
        for heading in global_section_measurement_order[section]:
            full_heading = f"{heading} ({section})"
            unit = global_units.get(full_heading, "")
            if unit:
                full_heading = f"{full_heading} [{unit}]"
            final_column_order.append(full_heading)

    # Build final patient rows
    final_rows = []
    for study_id, risk_date, ct_date, sex, age, risk, section_data in patient_data:
        row_values = [study_id, risk_date, ct_date, sex, age, risk]
        for section in section_order:
            for heading in global_section_measurement_order[section]:
                full_heading = f"{heading} ({section})"
                row_values.append(section_data[section].get(full_heading, ""))
        final_rows.append(row_values)

    final_df = pd.DataFrame(final_rows, columns=final_column_order)
    final_df.to_excel(output_file, index=False)
    print(f"✅ Saved to: {output_file}")

# Example usage
process_excel("Quantitative AllData Sheet.xlsx", "Quantitative AllData v1.xlsx")
