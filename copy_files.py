import shutil
from config.datasets_config import cohort_paths

"""
Dit script kan eventueel gebruikt worden als er meerdere kopien tegelijk moeten worden gemaakt van de originele bestanden, stel dat jullie nieuwe functionaliteiten willen testen kan dat handig zijn. 
"""
def main():
    sources = [cohort_paths["PCI"]["original_file"], cohort_paths["PMICD"]["original_file"], cohort_paths["ABL"]["original_file"],
               cohort_paths["OHO"]["original_file"]]
    targets = [cohort_paths["PCI"]["input_file"], cohort_paths["PMICD"]["input_file"], cohort_paths["ABL"]["input_file"],
               cohort_paths["OHO"]["input_file"]]

    for source, target in zip(sources, targets):
        shutil.copy(source, target)


if __name__ == '__main__':
    main()
