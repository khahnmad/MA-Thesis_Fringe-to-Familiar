"""
Requirements:
- only English
- only error free
- combine datasets where necessary
- from the right time period
- balanced in size
- handle duplicates

10 day cycle? Exclude what's outside of 10 days?
"""
import universal_functions as uf
from datetime import datetime
import random
from typing import List


def create_datasets(year: int, dataset_name: str, codenames: List[str]):
    print(f"Prepping {dataset_name} {year}")
    export_name = f'{dataset_name}_2-{year}.csv'
    incomplete_export_name = f'{dataset_name}_2-{year}_INCOMPLETE.csv'
    completed_files = uf.load_all_complete_datasets()
    for file in completed_files:
        if "\\"+export_name in file or "\\"+incomplete_export_name in file:
            print('    Already exists')
            return

    text_filenames = uf.load_files_from_dataset(['text', str(year)])  # get all text files for the given year
    specific_filenames = []
    for file in text_filenames:  # iterate through all text files
        for codename in codenames:  # iterate through the prefixes that identify the dataset
            if codename in file:
                specific_filenames.append(file)  # get all the relevant filenames

    # Filter out the ones that are already completed
    # specific_filenames = [x for x in specific_filenames if x not in completed_files] # TODO

    start_date = datetime(year, 2, 1)
    end_date = datetime(year, 2, 12)  # allow a 12 day period

    headings = uf.import_csv(specific_filenames[0])[0]
    new_dataset, id_counts = [headings], []

    doesnt_count = 0
    for file in specific_filenames:  # go through each file
        data = uf.import_csv(file)

        for row in data[1:]:
            # if the article has no error, hasn't been included already, and it's in english...
            if 'ERROR:' not in row[-1]:
                if row[0] not in id_counts:
                    if row[1] == '':  # include those that have no date
                        id_counts.append(row[0])
                        new_dataset.append(row)
                    else:  # if there is date data
                        try:
                            date = datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S')
                        except ValueError:
                            date = datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S.%f')
                        if start_date <= date <= end_date:
                            id_counts.append(row[0])
                            new_dataset.append(row)
            doesnt_count +=1
    missing_data = 2000 - len(new_dataset)
    if missing_data > 0:
        print(f"    Missing {missing_data} articles to be complete")

        uf.export_nested_list(incomplete_export_name, new_dataset)
    else:
        print(f"    Dataset has {len(new_dataset)} rows...")
        uf.export_nested_list(f'{dataset_name}_2-{year}_OVERBY_{len(new_dataset)}.csv', new_dataset)
        sampled_data = []
        # choose {abs(missing_data))} to be removed from the dataset
        chosen_ids = random.sample(id_counts, abs(missing_data))
        for elt in new_dataset:
            if elt[0] not in chosen_ids:
                sampled_data.append(elt)

        uf.export_nested_list(export_name, sampled_data)


def create_far_right_datasets(year: int):
    create_datasets(year, 'FarRight', ["CO", "FR", "HR"])


def create_center_right_dataset(year):
    create_datasets(year, 'CenterRight', ["CR"])


def create_right_datset(year):
    create_datasets(year, 'Right',["RR"])


def create_center_dataset(year):
    create_datasets(year, "Center", ["CE"])


def create_center_left_dataset(year):
    create_datasets(year, "CenterLeft", ['CL'])


def create_left_dataset(year):
    create_datasets(year, "Left", ["LL"])


def create_far_left_dataset(year):
    create_datasets(year, "FarLeft", ["HL"])


for i in range(2016, 2022):
    create_far_left_dataset(i)
    create_left_dataset(i)
    create_center_left_dataset(i)
    create_center_dataset(i)
    create_center_right_dataset(i)
    create_right_datset(i)
    create_far_right_datasets(i)
    print('')