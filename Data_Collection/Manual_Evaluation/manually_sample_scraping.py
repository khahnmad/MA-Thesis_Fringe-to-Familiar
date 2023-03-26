import universal_functions as uf
import random
import scraping as scrape


# change uf importation, check that the usage in the scraping evaluation works
def get_partisanship_year(filename):
    valid_years = ['2016', '2017', '2018', '2019', '2020', '2021']
    partisan_ids = {'CO': 'FarRight', 'FR': 'FarRight', 'HR': 'FarRight', 'RR': 'Right', 'CR': 'CenterRight',
                    'NA': 'Center', 'CE': 'Center', 'CL': 'CenterLeft', 'LL': 'Left', 'HL': 'FarLeft'}
    for yr in valid_years:
        if yr in filename:
            for key in partisan_ids.keys():
                if key in filename:
                    dataset_name = f"{partisan_ids[key]}_{yr}"
    return dataset_name

def manually_sample(files:list, n:int):
    manual_file_name = 'C:\\Users\\khahn\\Documents\\Github\\Thesis\\scraping_evals\\associated_python\\Manual_evaluation.csv'
    record_dict = uf.load_manual_eval_as_dict() # Import the manual evaluation file as a dictionary

    progress_file = uf.import_csv('/dataset_eval\\Manual_Evaluation_Progress.csv')
    progress_dict = {x[0]:float(x[1]) for x in progress_file} # Records the percent of the dataset that has been manually evaluated

    try:
        for file in files: # Iterate through the text unprepped dataset
            if file not in record_dict.keys(): # create new k,v pair if there's a new file in the list
                print(f'Creating the entry for {file}\n')
                record_dict[file]=[[],[],[],[]] # file: scraped text: success, fail; error found: success, fail

            dataset_name = get_partisanship_year(file)

            if progress_dict[dataset_name] > 2:
                print(f"{progress_dict[dataset_name]}% of {file} has already been evaluated\n")
                continue

            # if file not in record_dict.keys(): # create new k,v pair if there's a new file in the list
            #     print(f'Creating the entry for {file}\n')
            #     record_dict[file]=[[],[],[],[]] # file: scraped text: success, fail; error found: success, fail
            if len(record_dict[file])==2:
                record_dict[file].append([])
                record_dict[file].append([])
            data = uf.import_csv(file) # import the data
            # Check for handled previous failures
            updated_text_fails, updated_error_fails = [],[]
            for fail in record_dict[file][1]: # iterate through the identified failed scrapes
                failed_text = data[fail][-1]
                if "ERROR:" not in failed_text:
                    updated_text_fails.append(fail) # only re-add them if no update has happened
            record_dict[file][1]=updated_text_fails
            for error_fail in record_dict[file][3]:
                failed_error = data[error_fail][-1]
                if 'ERROR:' in failed_error:
                    updated_error_fails.append(error_fail)
            record_dict[file][3] = updated_error_fails
            if len(data)<=1:
                print(f'No data for {file}')
            else:
                for i in range(n):
                    index= random.randint(1,len(data)-1)
                    if 'ERROR:' in data[index][-1]:
                        print(f"ERROR VALIDATION")
                        result = scrape.access_article(data[index][3])
                        print(f"URL: {data[index][3]}")
                        print("Recorded error:",data[index][-1])
                        print('Rescrape result:',result)
                        print(f"\nSuccess/ Failure (s/f):")
                        s_f = input()
                        if s_f == 's':
                            record_dict[file][2].append(index)
                        if s_f == 'f':
                            record_dict[file][3].append(index)
                        if s_f == 'escape':
                            exportable_record = [list(row) for row in record_dict.items()]
                            uf.export_nested_list(manual_file_name, exportable_record)
                            return "Exited before complete cycle"
                    else:
                        print("TEXT VALIDATION")
                        print(f"URL: {data[index][3]}")
                        print(data[index][-1])
                        print(f"\nSuccess/ Failure (s/f):")
                        s_f = input()
                        if s_f=='s': # Successful number goes in the first list
                            record_dict[file][0].append(index)
                        if s_f=='f': # Failed goes in the second list
                            record_dict[file][1].append(index)
                        if s_f =='escape':
                            exportable_record = [list(row) for row in record_dict.items()]
                            uf.export_nested_list(manual_file_name,exportable_record)
                            return 'Exited before a complete cycle'

                # record.append(file_record)
        exportable_record = [list(row) for row in record_dict.items()]
        uf.export_nested_list(manual_file_name,exportable_record)
        return 'Exited after complete cycle'
    except Exception as e:
        print(e)
        exportable_record = [list(row) for row in record_dict.items()]
        uf.export_nested_list(manual_file_name,exportable_record)
        return 'Exited because of an error'

complete_text = uf.load_files_from_dataset(['text'])
result = manually_sample(complete_text, 1)
print(result)
# fix
# manual_eval = uf.import_csv('C:\\Users\\khahn\\Documents\\Github\\Thesis\\scraping_evals\\Manual_evaluation.csv')
# for item in manual_eval:
#     filename = item[0]
#     item[0]=filename.replace('PycharmProjects\\Thesis_explo','Documents\\Github\\Thesis')
#     print('check')
# uf.export_nested_list('C:\\Users\\khahn\\Documents\\Github\\Thesis\\scraping_evals\\Manual_evaluation.csv',manual_eval)