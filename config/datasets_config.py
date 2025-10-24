from pathlib import Path

cohort_paths = {
    "ABL": {
        "original_file": Path(r"L:\CVPZ\CHVC\MANAGEMENT\BIM\Epic\01_ABL_Epic_Verrichtingen_CAR.xlsx"),
        "json_rules": Path(r"L:\CVPZ\CHVC\MANAGEMENT\BIM\Python_Programmas\NHR_excepties\nhr_template_creation\rules\abl_rules.json"),
        "input_variables_path": Path(r"L:\CVPZ\CHVC\MANAGEMENT\BIM\Python_Programmas\NHR_handboek_converter\src\data\2_NHR_kolomlijsten_per_cohort\Kolomnamen_lijst_Ablatie_behorend_bij_Handboek_versie_24.1.1.xlsx"),
        "sheet_name": "ABL_NHR",
        "header_row": 0
    },
    "PMICD": {
        "original_file": Path(r"L:\CVPZ\CHVC\MANAGEMENT\BIM\Epic\01_PMICD_Epic_Verrichtingen_CAR.xlsx"),
        "json_rules": Path(r"L:\CVPZ\CHVC\MANAGEMENT\BIM\Python_Programmas\NHR_excepties\nhr_template_creation\rules\pmicd_rules.json"),
        "input_variables_path": Path(r"L:\CVPZ\CHVC\MANAGEMENT\BIM\Python_Programmas\NHR_handboek_converter\src\data\2_NHR_kolomlijsten_per_cohort\Kolomnamen_lijst_Pacemaker_ICD_behorend_bij_Handboek_versie_25.1.1.xlsx"),
        "sheet_name": "PMICD_NHR",
        "header_row": 0
    }
    ,
    "PCI": {
        "original_file": Path(r"L:\CVPZ\CHVC\MANAGEMENT\BIM\Epic\01_PCI_Epic_Verrichtingen_CAR.xlsx"),
        "json_rules": Path(r"L:\CVPZ\CHVC\MANAGEMENT\BIM\Python_Programmas\NHR_excepties\nhr_template_creation\rules\pci_rules.json"),
        "input_variables_path": Path(r"L:\CVPZ\CHVC\MANAGEMENT\BIM\Python_Programmas\NHR_handboek_converter\src\data\2_NHR_kolomlijsten_per_cohort\Kolomnamen_lijst_PCI_behorend_bij_Handboek_versie_23.1.3.xlsx"),
        "sheet_name": "PCI_NHR",
        "header_row": 0
    },
    "OHO": {
        "original_file": Path(r"L:\CVPZ\CHVC\MANAGEMENT\BIM\Epic\01_OHO_Epic_Verrichtingen_CTC.xlsx"),
        "json_rules": Path(r"L:\CVPZ\CHVC\MANAGEMENT\BIM\Python_Programmas\NHR_excepties\nhr_template_creation\rules\oho_rules.json"),
        "input_variables_path": Path(r"L:\CVPZ\CHVC\MANAGEMENT\BIM\Python_Programmas\NHR_handboek_converter\src\data\2_NHR_kolomlijsten_per_cohort\Kolomnamen_lijst_Cardiochirurgie_behorend_bij_Handboek_versie_22.2.1.xlsx"),
        "sheet_name": "OHO_NHR",
        "header_row": 0

    },
    "THI": {
        "original_file": Path(r"L:\CVPZ\CHVC\MANAGEMENT\BIM\Epic\01_THI_Epic_Verrichtingen_CAR_CTC.xlsx"),
        "input_variables_path": Path(r"L:\CVPZ\CHVC\MANAGEMENT\BIM\Python_Programmas\NHR_handboek_converter\src\data\2_NHR_kolomlijsten_per_cohort\Kolomnamen_lijst_THI_behorend_bij_Handboek_25.1.2.xlsx"),
        "sheet_name": "THI_NHR",
        "header_row": 0

    }
}
