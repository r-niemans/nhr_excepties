import shutil
from config.datasets_config import cohort_paths

def main():
    sources = [cohort_paths["PCI"]["original_file"], cohort_paths["PMICD"]["original_file"], cohort_paths["ABL"]["original_file"],
               cohort_paths["OHO"]["original_file"]]
    targets = [cohort_paths["PCI"]["input_file"], cohort_paths["PMICD"]["input_file"], cohort_paths["ABL"]["input_file"],
               cohort_paths["OHO"]["input_file"]]

    for source, target in zip(sources, targets):
        shutil.copy(source, target)


if __name__ == '__main__':
    main()
