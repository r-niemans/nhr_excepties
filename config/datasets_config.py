from pathlib import Path

cohort_paths = {
    "ABL": {
        "original_file": Path(r"L:\CVPZ\CHVC\MANAGEMENT\BIM\Epic\01_ABL_Epic_Verrichtingen_CAR.xlsx"),
        "output_file": Path(r"L:\CVPZ\CHVC\MANAGEMENT\BIM\Python_Programmas\NHR_automatisering\ablaties\ablaties_NHR_template.xlsx"),
        "json_rules": Path(r"C:\Users\G10068679\PycharmProjects\nhr_excepties\nhr_template_creation\rules\abl_rules.json"),
        "input_file": Path(r"L:\CVPZ\CHVC\MANAGEMENT\BIM\Python_Programmas\NHR_automatisering\ablaties\ABL_Epic_Verrichtingen_CAR.xlsx"),
        "sheet_name": "ABL NHR template",
        "header_row": 6
    },
    "PMICD": {
        "original_file": Path(r"L:\CVPZ\CHVC\K-EN-V\Ned-Hart-Registratie\aanlevering NHR PMICD\PMICD_2024\01_PMICD_Masterfile_2024.xlsm"),
        "output_file": Path(r"L:\CVPZ\CHVC\MANAGEMENT\BIM\Python_Programmas\NHR_automatisering\pmicd\PMICD_NHR_template.xlsx"),
        "json_rules": Path(r"C:\Users\G10068679\PycharmProjects\nhr_excepties\nhr_template_creation\rules\pmicd_rules.json"),
        "input_file": Path(r"L:\CVPZ\CHVC\MANAGEMENT\BIM\Python_Programmas\NHR_automatisering\pmicd\PMICD_Epic_Verrichtingen.xlsm"),
        "sheet_name": "NHR_Template",
        "header_row": 1
    }
    ,
    "PCI": {
        "original_file": Path(r"L:\CVPZ\CHVC\K-EN-V\Ned-Hart-Registratie\aanlevering NHR PCI\PCI_2024\01_PCI_Masterfile_2024.xlsm"),
        "output_file": Path(r"L:\CVPZ\CHVC\MANAGEMENT\BIM\Python_Programmas\NHR_automatisering\pci\PCI_NHR_template.xlsx"),
        "json_rules": Path(r"C:\Users\G10068679\PycharmProjects\nhr_excepties\nhr_template_creation\rules\pci_rules.json"),
        "input_file": Path(r"L:\CVPZ\CHVC\MANAGEMENT\BIM\Python_Programmas\NHR_automatisering\pci\PCI_Epic_Verrichtingen.xlsm"),
        "sheet_name": "NHR_Template",
        "header_row": 1
    },
    "OHO": {
        "original_file": Path(r"L:\CVPZ\CHVC\K-EN-V\Ned-Hart-Registratie\aanlevering NHR OHO\OHO 2024\01_OHO_Masterfile_2024.xlsm"),
        "output_file": Path(r"L:\CVPZ\CHVC\MANAGEMENT\BIM\Python_Programmas\NHR_automatisering\oho\OHO_NHR_template.xlsx"),
        "json_rules": Path(r"C:\Users\G10068679\PycharmProjects\nhr_excepties\nhr_template_creation\rules\oho_rules.json"),
        "input_file": Path(r"L:\CVPZ\CHVC\MANAGEMENT\BIM\Python_Programmas\NHR_automatisering\oho\OHO_Epic_Verrichtingen.xlsm"),
        "sheet_name": "NHR_templ_ruw",
        "header_row": 3

    }
}
