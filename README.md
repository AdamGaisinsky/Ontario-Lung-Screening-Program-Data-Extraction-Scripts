# Ontario-Lung-Screening-Program-Data-Extraction-Scripts
Code for the extraction of data from Ontario Lung Screening Program (OLSP) data for manuscript: Actionable Incidental Findings at Baseline Lung Cancer Screening: Identifying Opportunities in a Universal Healthcare System.

All scripts only function on OLSP data formatted in accordance with the LDCT Ontario Lung Cancer Screening Program (OLSP) Reporting Template (https://www.cancercareontario.ca/sites/ccocancercare/files/assets/LDCTLungCancerScreeningReportingTemplate.pdf).

Report Script v1 is used to extract most report headings and information from standardized reports. It takes the completed template as input and outputs an excel file with patients in rows and report sections in columns.

LungRADS Score Script is used to extract the LungRADS Score from standardized reports. It takes the completed template as input and outputs a single column containing the LungRADS scores of each patient.

NoduleNum is used to extract the number of lung nodules reported. It takes the completed template as input and outputs 2 columns containing the number of nodules present in total and the number of nodules 4mm or greater for each patient.
