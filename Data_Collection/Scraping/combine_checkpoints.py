"""
This script combines the duplicate scraped files
"""
import universal_functions as uf


def combine_checkpoint_files(first_file:str, second_file:str):
    data1 = uf.import_csv(first_file)
    data2 = uf.import_csv(second_file)

    export_name = second_file

    new_file = []
    for row in data1:
        new_file.append(row)

    for item in data2[1:]:
        if len(item) == 11:
            new_file.append(item)

    no_duplicates = []
    for elt in new_file:
        if elt not in no_duplicates:
            no_duplicates.append(elt)
    uf.export_nested_list(export_name, no_duplicates)


# Former combo
checkpoint_2300_file = uf.load_files_from_dataset(["CR16","_600"])[0]
checkpoint_3500_file = uf.load_files_from_dataset(["CR16","3600"])[0]
combine_checkpoint_files(checkpoint_2300_file, checkpoint_3500_file)