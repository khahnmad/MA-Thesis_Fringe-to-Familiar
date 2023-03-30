"""
This script queries Media Cloud collections and collects urls
"""
from dotenv import load_dotenv
load_dotenv()
# Imports
import os, mediacloud.api
import datetime
import time
# import mediacloud.tags
import csv
import requests
import universal_functions as uf

mediacloud_dir = uf.repo_loc / 'Data_Collection/Media_Cloud'

# Functions
def setup():
    # Read API and check that the connection works

    MC_API_KEY = os.getenv('MC_API_KEY') # Read the API key
    # mc = mediacloud.api.MediaCloud(MC_API_KEY) # Check that the key works with mediacloud
    mc = mediacloud.api.BaseApi(MC_API_KEY)
    # print('MEDIACLOUD VERSION:', mediacloud.__version__)

    # make sure your connection and API key work by asking for the high-level system statistics
    # a = time.time()
    # mc.stats()
    # b = time.time()
    # print('CONNECTION CHECK:', b - a)
    return mc


def all_matching_stories(mc_client, q, fq):
    """
    Return all the stories matching a query within Media Cloud. Page through the results automatically.
    :param mc_client: a `mediacloud.api.MediaCloud` object instantiated with your API key already
    :param q: your boolean query
    :param fq: your date range query
    :return: a list of media cloud story items
    """
    last_id = 0
    more_stories = True
    stories = []
    while more_stories:
        try:
            page = mc_client.storyList(q, fq, last_processed_stories_id=last_id, rows=500, sort='processed_stories_id')
        except requests.exceptions.ConnectionError:
            print(f"ERROR: Connection aborted. Returning the stories that have been collected so far ")
            return stories
        print("  got one page with {} stories".format(len(page)))
        if len(page) == 0:
            more_stories = False
        else:
            stories += page
            last_id = page[-1]['processed_stories_id']
    return stories


def collect_stories(query, dates):
    # Check how many stories are there
    print(f'There are {mc.storyCount(query, dates)["count"]} stories for the query')

    # Fetch all the stories that match the query
    a = time.time()
    all_stories = all_matching_stories(mc, query, dates)
    b = time.time()
    print(f'Takes {b - a} seconds to run')

    # flatten things a little bit to make writing a CSV easier
    for s in all_stories:
        # see the "language" notebook for more details on themes
        theme_tag_names = ','.join(
            [t['tag'] for t in s['story_tags'] if t['tag_sets_id'] == mediacloud.tags.TAG_SET_NYT_THEMES])
        s['themes'] = theme_tag_names
    return all_stories


def write_csv(all_stories, name):
    fieldnames = ['stories_id', 'publish_date', 'title', 'url', 'language', 'ap_syndicated', 'themes', 'media_id',
                  'media_name', 'media_url']
    with open(name, 'w', newline='', encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        for s in all_stories:
            writer.writerow(s)


def collection_pipeline(start_date, keyword, collection, length):
    query = f"'{keyword}' and tags_id_media:{collection}" # define query

    end_date = start_date + datetime.timedelta(days=length) # define end date

    time_segment = mc.dates_as_query_clause(start_date, end_date)

    stories = collect_stories(query, time_segment)

    # Export data
    if keyword:
        title = str(mediacloud_dir / 'Urls') + f'{start_date.year}-{start_date.month}-{start_date.day}_{keyword}.csv'
    else:
        # title = f'{start_date.year}-{start_date.month}-{start_date.day}_{collection}.csv'
        title = str(mediacloud_dir / 'Urls') + f'{collection}_urls_{start_date.month}-{start_date.day}-{start_date.year}.csv'
    write_csv(stories, title)
    print('PROCESS COMPLETE')

# Setup
mc = setup()

# Collection Names
us_top_2018 = '186572516'
conservative_blogs = '8875111'

# Already used
buzfeed_hyperpartisan_right = '31653028' # HR
us_farright = '214598068' # FR
conspiracies = '214609438' # CO
us_right_2016 ='9360524' #RR16
us_right_2019 = '200363049' # RR19
us_center_right_2016 ='9360523' # CR16
us_center_right_2019 = '200363062' # CR19
us_national = '34412234' # NA
us_center_2016 = '9360522' # CE16
us_center_2019 = '200363050' # CE19
us_center_left_2016 = '9360521' #CL16
us_center_left_2019 = '200363048' #CL19
us_left_2016 = '9360520' # LL16
us_left_2019 = '200363061' # LL19
buzzfeed_hyperpartisan_left = '31653029' #HL

# Queries
empty_query = ''

# Run the collection pipeline
# Center
for i in range(2016,2022):
    feb_1_datetime = datetime.datetime(year=i,month=2, day=1)
    # feb_4_datetime = datetime.datetime(year=i,month=2, day=4)
    collection_pipeline(feb_1_datetime, empty_query, buzzfeed_hyperpartisan_left, 3)

# Far left
# for i in range(2017,2022):
#     # feb_1_datetime = datetime.datetime(year=i,month=2, day=1)
#     feb_4_datetime = datetime.datetime(year=i,month=2, day=4)
#     collection_pipeline(feb_4_datetime, empty_query, buzzfeed_hyperpartisan_left, 3)

# # Center Right 16
# for i in range(2019,2022):
#     feb_1_datetime = datetime.datetime(year=i,month=2, day=1)
#     collection_pipeline(feb_1_datetime, empty_query, us_center_right_2016, 3)


# # # Specific query
# year = 2017
# collection = us_left_2016
#
# datetime_obj = datetime.datetime(year=year,month=2, day=1)
# collection_pipeline(datetime_obj, empty_query, collection, 3)