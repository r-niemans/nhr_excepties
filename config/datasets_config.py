from pathlib import Path

cohort_paths = {
    "ABL": {
        "original_file": Path(r"L:\CVPZ\CHVC\MANAGEMENT\BIM\Epic\01_ABL_Epic_Verrichtingen_CAR.xlsx"),
        "output_file": Path(r"L:\CVPZ\CHVC\MANAGEMENT\BIM\Python_Programmas\NHR_automatisering\ablaties\ablaties_NHR_template.xlsx"),
        "json_rules": Path(r"L:\CVPZ\CHVC\MANAGEMENT\BIM\Python_Programmas\NHR_excepties\nhr_template_creation\rules\abl_rules.json"),
        "input_file": Path(r"L:\CVPZ\CHVC\MANAGEMENT\BIM\Python_Programmas\NHR_automatisering\ablaties\ABL_Epic_Verrichtingen_CAR.xlsx"),
        "sheet_name": "ABL NHR template",
        "header_row": 6
    },
    "PMICD": {
        "original_file": Path(r"L:\CVPZ\CHVC\MANAGEMENT\BIM\Epic\01_PMICD_Epic_Verrichtingen_CAR.xlsx"),
        "output_file": Path(r"L:\CVPZ\CHVC\MANAGEMENT\BIM\Python_Programmas\NHR_automatisering\pmicd\PMICD_NHR_template.xlsx"),
        "json_rules": Path(r"L:\CVPZ\CHVC\MANAGEMENT\BIM\Python_Programmas\NHR_excepties\nhr_template_creation\rules\pmicd_rules.json"),
        "input_file": Path(r"L:\CVPZ\CHVC\MANAGEMENT\BIM\Python_Programmas\NHR_automatisering\pmicd\PMICD_Epic_Verrichtingen.xlsx"),
        "sheet_name": "PMICD_NHR",
        "header_row": 0
    }
    ,
    "PCI": {
        "original_file": Path(r"L:\CVPZ\CHVC\MANAGEMENT\BIM\Epic\01_PCI_Epic_Verrichtingen_CAR.xlsx"),
        "output_file": Path(r"L:\CVPZ\CHVC\MANAGEMENT\BIM\Python_Programmas\NHR_automatisering\pci\PCI_NHR_template.xlsx"),
        "json_rules": Path(r"L:\CVPZ\CHVC\MANAGEMENT\BIM\Python_Programmas\NHR_excepties\nhr_template_creation\rules\pci_rules.json"),
        "input_file": Path(r"L:\CVPZ\CHVC\MANAGEMENT\BIM\Python_Programmas\NHR_automatisering\pci\PCI_Epic_Verrichtingen.xlsx"),
        "sheet_name": "PCI_NHR",
        "header_row": 0
    },
    "OHO": {
        "original_file": Path(r"L:\CVPZ\CHVC\MANAGEMENT\BIM\Epic\01_OHO_Epic_Verrichtingen_CTC.xlsx"),
        "output_file": Path(r"L:\CVPZ\CHVC\MANAGEMENT\BIM\Python_Programmas\NHR_automatisering\oho\OHO_NHR_template.xlsx"),
        "json_rules": Path(r"L:\CVPZ\CHVC\MANAGEMENT\BIM\Python_Programmas\NHR_excepties\nhr_template_creation\rules\oho_rules.json"),
        "input_file": Path(r"L:\CVPZ\CHVC\MANAGEMENT\BIM\Python_Programmas\NHR_automatisering\oho\OHO_Epic_Verrichtingen.xlsx"),
        "sheet_name": "OHO_NHR",
        "header_row": 0

    },
    "THI": {
        "original_file": Path(
            r"L:\CVPZ\CHVC\MANAGEMENT\BIM\Epic\01_THI_Epic_Verrichtingen_CAR_CTC.xlsx"),
        "output_file": Path(
            r"L:\CVPZ\CHVC\MANAGEMENT\BIM\Python_Programmas\NHR_automatisering\thi\THI_NHR_template.xlsx"),
        "input_file": Path(
            r"L:\CVPZ\CHVC\MANAGEMENT\BIM\Python_Programmas\NHR_automatisering\oho\THI_Epic_Verrichtingen_CAR_CTC.xlsx"),
        "sheet_name": "THI_NHR",
        "header_row": 0

    }
}
