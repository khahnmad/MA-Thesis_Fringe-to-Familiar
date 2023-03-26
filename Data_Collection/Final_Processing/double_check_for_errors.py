import universal_functions as uf
import scraping as scrape
import re
import glob


def check_error_handling(url:str, text:str):
    # error handling from scraping
    error = scrape.check_never_scrapable(url)
    if error is not True:
        return error

    error = scrape.check_soup_contents(text.lower())
    if error is not True:
        return error

    if len(text)<370:
        return 'ERROR: Insufficient text'

    return error


def get_partisanship(filename:str)->str:
    regex = r"(?<=prepped_dataset\\)(.*?)(?=\_2)"
    dataset_name = re.findall(regex, filename)[0]
    return dataset_name

def get_year(filename:str)->str:
    regex = r"(?<=2\-)(.*?)(?=\.csv)"
    dataset_name = re.findall(regex, filename)[0]
    return dataset_name

def get_collection(filename:str)->str:
    regex = r"(?<=datasets\\)(.*?)(?=\_text)"
    dataset_name = re.findall(regex, filename)[0]
    return dataset_name

def get_num_overby(filename:str)->str:
    regex = r"(?<=OVERBY\_)(.*?)(?=\.csv)"
    dataset_name = re.findall(regex, filename)[0]
    return dataset_name

def look_for_fp_in_dataset(file:str):
    conversion_dict = {'FarRight': ["CO", "FR", "HR"],
                       'CenterRight': ["CR"],
                       'Right': ["RR"],
                       'Center': ['NA', "CE"],
                       'CenterLeft': ['CL'],
                       'Left': ["LL"],
                       'FarLeft': ["HL"]
                       }

    partisanship = get_partisanship(file)
    collections = conversion_dict[partisanship]
    year = get_year(file)
    dataset = uf.import_csv(file)
    dataset_ids = [x[0] for x in dataset[1:]]

    relevant_keys = []
    for key in manual_dict.keys():
        for collect in collections:
            if collect in key and year in key:
                relevant_keys.append(key)

    failed_scrapes, failed_errors = [],[]
    for key in relevant_keys:
        # scrape_fails = manual_dict[key][1]
        try:
            error_fails = manual_dict[key][3]
        except IndexError:
            error_fails = []
        if len(error_fails) > 0:
            try:
                feeder_data = uf.import_csv(key)
            except FileNotFoundError:
                collection = get_collection(key)
                datasets = [x for x in glob.glob('C:\\Users\\khahn\\Documents\\Github\\Thesis\\datasets\\' + "/*.csv") if year in x and collection in x and 'text' in x]
                feeder_data = uf.import_csv(datasets[0])


            for ef in error_fails:
                if "ERROR:" not in feeder_data[ef][-1]:
                    failed_errors.append(feeder_data[ef])
    identified_problems= []
    for elt in failed_errors:
        if elt[0] in dataset_ids:
            print('we have an error')
            identified_problems.append(elt[0])
    return identified_problems

def find_successful_extras(file, bad_ids, bad_indexes):
    # Find overby file
    partisanship = get_partisanship(file)
    year = get_year(file)
    overby_files = [x for x in glob.glob('C:\\Users\\khahn\\Documents\\Github\\Thesis\\prepped_dataset\\' + "/*.csv") if
     year in x and partisanship in x and 'OVERBY' in x]

    if len(overby_files)==0:
        print('NO SURPLUS FILES FOUND')
        return 'ERROR'

    highest = [0, overby_files[0]]
    if len(overby_files)>1:
        highest = [0,'']
        for o_file in overby_files:
            num_overby = int(get_num_overby(o_file))
            if num_overby > highest[0]:
                highest = [num_overby, o_file]

    # REmove the bad stuff from the exisiting file
    existing_data = uf.import_csv(file)
    wo_bad_inices = [existing_data[i] for i in range(len(existing_data)) if i not in bad_indexes]
    wo_headings = [x for x in wo_bad_inices if x[0]!='stories_id']
    cleaned_existing = [x for x in wo_headings if x[0] not in bad_ids]
    existing_ids = [x[0] for x in cleaned_existing]
    missing_num = 2000- len(cleaned_existing)

    # Import surplus file
    surplus_file = uf.import_csv(highest[1])

    additional_articles = []

    for i in range(1,len(surplus_file)):

        if surplus_file[i][0] in existing_ids:
            continue
        result = check_error_handling(surplus_file[i][3],surplus_file[i][-1])
        if result is True:
            additional_articles.append(surplus_file[i])
            if len(additional_articles) == missing_num:
                return additional_articles + cleaned_existing
    if len(additional_articles) < missing_num:
        print(f"INCOMPLETE: Need {missing_num-len(additional_articles)} more articles")
        return additional_articles +cleaned_existing

# Necessary data
manual_dict = uf.load_manual_eval_as_dict() # Manual evaluation
complete_datasets = uf.load_all_complete_datasets() # Completed datasets




# Action
for file in complete_datasets:
    print(f'Running {file}...')
    dont_check = ['CenterRight_2-2016','CenterRight_2-2017',
                  'FarRight_2-2016', 'FarRight_2-2017','FarRight_2-2018','FarRight_2-2019','FarRight_2-2020',
                  'FarRight_2-2021',
                  'Left_2-2016',"Left_2-2017","Left_2-2018",
                  'CenterLeft_2-2016',"CenterLeft_2-2017",'CenterLeft_2-2018']
    dont_run=False
    for d in dont_check:
        if d in file:
            dont_run = True
    if dont_run==True:
        print('    Skipping this one...')
        continue
    indexes_to_replace=[]
    ids_to_replace =look_for_fp_in_dataset(file)
    data = uf.import_csv(file)
    for i in range(1,len(data)):
        text = data[i][-1].lower()
        url = data[i][3]

        error = check_error_handling(url, text)
        if error is not True:
            indexes_to_replace.append(i)
    if len(indexes_to_replace)>0 or len(ids_to_replace)>0:
        new_dataset = find_successful_extras(file, ids_to_replace, indexes_to_replace)
        if new_dataset!='ERROR':
            uf.export_nested_list(file, new_dataset)
            print('    Exported cleaned version')
        else:
            print('    Theres an error')
    else:
        print('    Already clean')
# TODO: remove the heading