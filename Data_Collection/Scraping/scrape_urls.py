"""
Scrapes the text from the Media Cloud urls collected
"""
# Imports
from bs4 import BeautifulSoup as bs
import requests
import time
import random
import universal_functions as uf
import re
import glob
import json
from lxml import etree

from Data_Collection.Scraping import error_handling as e
mediacloud_dir = uf.repo_loc / "Data_Collection/Media_Cloud"


def check_empty_ptags(url:str, soup_text:str)->str:
    # If there's not content in the ptags, check the soup.text for error handling
    # Also checks the url in some cases
    text = True
    if 'pantsonfirenews.com' in url:
        text = 'ERROR: 403 Forbidden'
    if 'fox2now.com/news' in url or 'ktla.com/news/' in url:
        text = 'ERROR: 451 Unavailable for legal reasons'
    if soup_text == ' ':
        text = 'ERROR: 404 Page not found'
    if 'mediamatters.org' in url and 'clips' in url:
        text = "ERROR: Video/ Image content only"
    if 'theepochtimes.com' in url and 'epoch video' in soup_text.lower():
        text = "ERROR: Video/ Image content only"
    if 'chinadaily.com.cn' in url:  # TODO: this could be more sophisticated
        text = soup_text
    if 'gmanetwork.com' in url or 'ecowatch' in url:
        text = 'ERROR: Not scrapable content'

    for n in e.empty_ptag_url_errors['404 Page not found']:
        if n in url:
            text = 'ERROR: 404 Page not found'

    for obj in e.empty_ptag_url_errors['Article has been archived']:
        if obj in url:
            text = "ERROR: Article has been archived"

    for nf in e.empty_ptag_text_errors['Article not found']:
        if nf in soup_text.lower():
            text = "ERROR: Article not found"

    for item in e.empty_ptag_url_errors['Article not found']:
        if item in url:
            text = "ERROR: Article not found"

    for elt in e.empty_ptag_text_errors['Blocked from website']:
        if elt in soup_text.lower():
            text = 'ERROR: Blocked from website'

    for x in e.empty_ptag_url_errors['Video/ Image content only']:
        if x in url:
            text = "ERROR: Video/ Image content only"

    return text


def check_never_scrapable(url:str):
    # For urls that will never be able to be scraped
    error = True # returns true if the url is not any of the ones listed below

    for item in e.n_scrapable_url_errors['Website is no longer maintained']:
        if item in url:
            error = 'ERROR: Website is no longer maintained'

    for elt in e.n_scrapable_url_errors['Video/ Image content only']:
        if elt in url:
            error = 'ERROR: Video/ Image content only'

    if url.endswith('.jpg'):
        error = 'ERROR: Video/ Image content only'

    for obj in e.n_scrapable_url_errors['Not scrapable content']:
        if obj in url:
            error = 'ERROR: Not scrapable content'

    if 'msnbc' in url and 'watch' in url:
        error = 'ERROR: Video/ Image content only'
    if 'ir.voanews' in url or 'paper.li' in url or "hani.co.kr" in url or 'destentor.nl' in url or 'thenewsdoctors.com' in url:
        error = 'ERROR: Not in English'
    if '.pdf' in url:
        error = 'ERROR: Content is a pdf'
    return error


def check_soup_contents(low_soup_text: str) -> str:
    # Check for explicit error messages in the soup contents
    error = True
    if '401 authorization required' in low_soup_text or 'user is not authorized to perform this action' in low_soup_text:
        error = 'ERROR: 401 Authorization Required'

    for f in e.soup_contents_text_errors['403 Forbidden']:
        if f in low_soup_text:
            error = 'ERROR: 403 Forbidden'
    if low_soup_text=='forbidden' or low_soup_text=='403':
        error = 'ERROR: 403 Forbidden'

    if 'Looks like something went wrong.'.lower() == low_soup_text or 'Something went wrong. Wait a moment and try again.'.lower()==low_soup_text:
        error = 'ERROR: 404 Page not found'
    if ' BLACKLISTED NEWS FAVORITES'.lower()==low_soup_text:
        error = 'ERROR: 404 Page not found'
    for n in e.soup_contents_text_errors['404 Page not found']:
        if n in low_soup_text:
            error = 'ERROR: 404 Page not found'
    if low_soup_text=='not found':
        error =  'ERROR: 404 Page not found'

    if low_soup_text=='not acceptable':
        error = 'ERROR: 406 Not Acceptable'
    if '406 not acceptable' in low_soup_text:
        error = 'ERROR: 406 Not Acceptable'

    if '410 deleted by author' in low_soup_text:
        error = 'ERROR: 410 Deleted'

    for elt in e.soup_contents_text_errors['451 Unavailable for legal reasons']:
        if elt in low_soup_text:
            error = 'ERROR: 451 Unavailable for legal reasons'

    if 'reported a bad gateway error' in low_soup_text or '502 bad gateway' in low_soup_text:
        error = 'ERROR: 502 gateway error'

    if 'this content has been removed' in low_soup_text:
        error = "ERROR: Article has been archived"

    for obj in e.soup_contents_text_errors['Article behind a paywall or login page']:
        if obj in low_soup_text:
            error = "ERROR: Article behind a paywall or login page"

    for item in e.soup_contents_text_errors['Article not found']:
        if item in low_soup_text:
            error = "ERROR: Article not found"

    if 'blocked your ip' in low_soup_text or low_soup_text=='too many requests':
        error = 'ERROR: Blocked from website'
    for b in e.soup_contents_text_errors['Blocked from website']:
        if b in low_soup_text:
            error='ERROR: Blocked from website'

    if 'client-side exception' in low_soup_text:
        error = "ERROR: Client-Side Exception"

    if 'an unknown connection issue between Cloudflare and the origin web server'.lower() in low_soup_text:
        error = 'ERROR: Connection Issue'

    if 'internal server error' in low_soup_text:
        error = 'ERROR: Internal Server Error'

    if 'This error was generated by Mod_Security'.lower() in low_soup_text:
        error = 'ERROR: Mod_Security server-side error'

    for j in e.soup_contents_text_errors['Must enable cookies to access site']:
        if j in low_soup_text:
            error = 'ERROR: Must enable cookies to access site'

    if 'The provided host name is not valid for this server.'.lower() in low_soup_text:
        error = 'ERROR: Provided host name is not valid for this server'

    if 'server temporarily unavailable' in low_soup_text:
        error = "ERROR: Server side connection error"

    if '\nvia youtube' in low_soup_text:
        error = 'ERROR: Video/ Image content only'

    return error


def do_alternative_scraping(url, response, soup):
    app_json_art_body = ['qz.com', 'newtimes.com.rw', 'newtimes.co.rw', 'newsweek.com', 'scmp.com']
    for a in app_json_art_body:
        if a in url:
            if 'Forbidden' in response:
                return 'ERROR: 403 Forbidden'
            tree = etree.HTML(response)
            json_type_elts = tree.xpath('//script[@type="application/ld+json"]')
            for jte in json_type_elts:
                if 'articleBody' in jte.text:
                    json_obj = json.loads(jte.text)
                    try:
                        article_text = json_obj['articleBody']
                        return article_text
                    except KeyError:
                        return 'ERROR: No text gathered'
            paragraphs = soup.find_all('p')
            stripped_paragraph = [tag.get_text().strip() for tag in paragraphs]
            if len(stripped_paragraph)>0:
                return " ".join(stripped_paragraph)
            return  'ERROR: No text gathered'
    if 'miamiherald.typepad.com' in url:
        div_elts = soup.find_all('div',attrs={'id':"story-content"})
        stripped = [tag.get_text().strip() for tag in div_elts]
        return " ".join(stripped)
    if 'dailywire.com' in url:
        div_elts = soup.find_all('div',attrs={'id':'post-body-text'})
        stripped = [tag.get_text().strip() for tag in div_elts]
        return " ".join(stripped)
    if 'nationalreview.com' in url:
        # Try with tree
        tree = etree.HTML(response)
        json_type_elts = tree.xpath('//script[@type="text/javascript"]')

        # Original version: This has worked at least three times
        js_var = re.findall(r'nr.headless.preloadedData = .*;', response) # debug
        if len(js_var) > 0:
            js_var_data = js_var[0].replace('nr.headless.preloadedData = ', '')[:-1]
            json_obj = json.loads(js_var_data)
            first_key = list(json_obj.keys())[0]
            content = json_obj[first_key]['body']['queried_object']['content']['rendered']
            js_soup = bs(content, 'html.parser')
            text = js_soup.get_text().strip()
            return text
        return 'ERROR: No text fathered'
    if 'columbiaspectator.com' in url:
        # Try tree version #debug
        tree =etree.HTML(response)

        # Old version
        fusion_global_content = re.findall(r'Fusion\.globalContent=.*?};',
                                           response)  # find the data given the variable name
        fg_contents = fusion_global_content[0].replace('Fusion.globalContent=', '')[
                      :-1]  # get the contents of the variables
        json_vers = json.loads(fg_contents)  # make it a json obj
        content_elts = json_vers['content_elements']  # get the relevant section of the json obj
        text = []
        for item in content_elts:
            if item['type'] == 'text':
                text.append(item['content'])
        return " ".join(text)

    if 'toledoblade' in url:
        tree = etree.HTML(response)
        json_type_elts = tree.xpath('//script[contains(text(),"JSON")]')
        for jte in json_type_elts:
            if 'pgStoryZeroJSON' in jte.text:
                cleaned_json = jte.text.replace('pgStoryZeroJSON = ', '').replace('\n', '')
                try:
                    json_version = json.loads(cleaned_json)
                    article_body = json_version['articles'][0]['body']
                    soup_obj = bs(article_body, 'html.parser')
                    text= soup_obj.get_text().strip()
                    return text # works, 11
                except json.decoder.JSONDecodeError:
                    article_regex = re.findall(r'body": ".*?",', cleaned_json)
                    cleaned_article_regex = article_regex[0].replace('body": "','').replace('"','')
                    soup_obj = bs(cleaned_article_regex, 'html.parser')
                    text = soup_obj.get_text().strip()
                    return text

    if 'blacknews.com/news' in url:
        div_elts = soup.find_all('div', attrs={'class':"post-body entry-content"})
        stripped = [tag.get_text().strip() for tag in div_elts]
        return " ".join(stripped)

    if 'thepoliticalinsider' in url:
        blog_div_elts = soup.find_all('div', attrs={'class': 'text article-body font-default font-size-med'})
        stripped = [tag.get_text().strip() for tag in blog_div_elts]
        if len(stripped)>0:
            return " ".join(stripped)
        script_variable =  re.findall(r'class="yoast-schema-graph">[\S\s]*?<\/script>', response)
        try:
            script_data = script_variable[0].replace('class="yoast-schema-graph">', '').replace('</script>', '')
            json_option = json.loads(script_data)
            dv=True # Todo: finsih this
        except IndexError:
            return "ERROR: Scraping error during JSON conversion"

    if 'ibtimes.com' in url or 'ibtimes.co' in url:
        if 'Forbidden' in response:
            return 'ERROR: 403 Forbidden'
        tree = etree.HTML(response)
        json_type_elts = tree.xpath('//script[contains(@type,"json")]')
        # json_obj = json.loads(json_type_elts[-1].text)
        # contents = json_obj['props']['pageProps']['pageContent']['parsedBody']
        # text = [content for content in contents if isinstance(content, str)]
        # return " ".join(text)
        return 'ERROR: No text gathered'
    if 'tampabay.com' in url:
        tree = etree.HTML(response)
        json_elts = tree.xpath('//script[contains(@type,"json")]')
        return 'ERROR: No text gathered' # Doesnt seem to work
    if 'newsday.com' in url:
        tree =  etree.HTML(response)
        json_elts = tree.xpath('//script[contains(@type,"json")]')
        try:
            for elt in json_elts:
                if 'bodyText' in elt.text:
                    json_version = json.loads(elt.text)
                    text = json_version['props']['pageProps']['data']['page']['leaf']['bodyText']
                    return text
            return 'ERROR: No text gathered'
        except IndexError:
            return 'ERROR: No text gathered'
        except KeyError:
            return 'ERROR: No text gathered'

    if 'timesofindia' in url:
        if 'videoshow' in url or '/photostory' in url:
            return "ERROR: Video/ Image content only"
        alt_elts = soup.find_all('div', attrs={'data-articlebody': '1'})
        stripped = [tag.get_text().strip() for tag in alt_elts]
        if len(stripped) < 1:
            blog_div_elts = soup.find_all('div', attrs={'class': 'main-content single-article-content'})
            stripped = [tag.get_text().strip() for tag in blog_div_elts]
            if len(stripped) < 1:
                return 'ERROR: No text gathered'
            return " ".join(stripped)
        return " ".join(stripped)

    if 'newsmax.com' in url.lower():
        div_elts = soup.find_all('div', id='mainArticleDiv')
        stripped = [tag.get_text().strip() for tag in div_elts]
        return " ".join(stripped)

    if 'sbs.com.au' in url:
        tree = etree.HTML(response)
        json_type_elts = tree.xpath('//script[contains(@type,"json")]')
        json_obj = json.loads(json_type_elts[-1].text)
        contents = json_obj['props']['pageProps']['pageContent']['parsedBody']
        text = [content for content in contents if isinstance(content, str)]
        return " ".join(text)

    if 'NDTV-LatestNews' in url:
        div_elts = soup.find_all('div', id='ins_storybody')
        stripped = [tag.get_text().strip() for tag in div_elts]
        return " ".join(stripped)

    return None


def access_article(url:str)->str:
    # First - check if it's a website that we can never scrape from
    scrapable = check_never_scrapable(url)
    if scrapable is not True:
        return scrapable

    # Next - try to scrape and handle any errors that appear
    try:
        response = requests.get(url, timeout=20).text
        # timeout for the request is 20 seconds; should never take longer than 10 seconds for a working link
        soup = bs(response, "html.parser")
    except requests.exceptions.ConnectionError:
        return "ERROR: requests.exceptions.ConnectionError"
    except requests.exceptions.ReadTimeout:
        return "ERROR: requests.exceptions.ReadTimeout"
    except requests.exceptions.TooManyRedirects:
        return "ERROR: Too Many redirects"
    except Exception as e:
        return f"ERROR: {e}"

    if len(response) == 0:
        return "ERROR: Article not found"

    if soup:  # if we do get contents from the scrape
        valid_soup = check_soup_contents(soup.text.lower())  # check to see if errors from the soup must be handled
        if valid_soup is not True:
            return valid_soup  # return the error if it is found

        js_scraping = do_alternative_scraping(url, response, soup)
        if js_scraping is not None:
            return js_scraping

        if 'conspiracydailyupdate' in url and 'View on YouTube' in soup.text:
            return "ERROR: Video/ Image content only"
        # Get contents of the page - catch-all scraping
        paragraphs = soup.find_all('p')
        stripped_paragraph = [tag.get_text().strip() for tag in paragraphs]

        if len(stripped_paragraph) == 0:  # if no contents from the page can be found
            handled_text = check_empty_ptags(url, soup.text)  # classify the reason we're not getting text
            if handled_text is not True:
                return handled_text
            if 'huffingtonpost' in url: #
                div_elts = soup.find_all('div', attrs={'class': 'caption-container'})
                alt_div = soup.find_all('div', attrs={'data-vars-affiliate':"jenifoto/iStock"})
                stripped = [tag.get_text().strip() for tag in div_elts]
                return " ".join(stripped)
            if 'ynetnews.com' in url:
                span_elts = soup.find_all('span', attrs={'data-text': 'true'})
                stripped = [tag.get_text().strip() for tag in span_elts]
                return " ".join(stripped)
            if 'refinery29' in url:
                alt_elts = soup.find_all('div', attrs={'class': 'section-text'})
                stripped = [tag.get_text().strip() for tag in alt_elts]
                return " ".join(stripped)
            if 'calciomercato.com' in url:
                div_elts = soup.find_all('div',attrs={'class':'text'})
                stripped = [tag.get_text().strip() for tag in div_elts]
                return " ".join(stripped)
            if 'Mashable' in url: # Note: seems to work # Note: not always
                article_elts =  soup.find_all('article',attrs={'class':'editor-content font-serif'})
                stripped = [tag.get_text().strip() for tag in article_elts]
                if len(stripped) >0:
                    return " ".join(stripped)
                else:
                    tree =etree.HTML(response)
                    debug = True
            if 'cnbctv18.com' in url:
                div_id_elts = soup.find_all('div', attrs={'id':'content'})
                first_stripped =  [tag.get_text().strip() for tag in div_id_elts]
                return " ".join(first_stripped)
            if 'ozy.com' in url: # TODO: doesnt work
                tree = etree.HTML(response)
                div_elts = soup.find_all('div',attrs={'class':'storytext'})
                stripped =  [tag.get_text().strip() for tag in div_elts]
                return " ".join(stripped)
            if 'wral.com' in url:
                return 'ERROR: 404 Page not found'
            if 'kake' in url:
                return  "ERROR: Video/ Image content only"
            if 'shadowandact.com' in url: # no article showed up on one of the articles checked for this # todo
                meta_elts = soup.find_all('meta', attrs={'data-n-head':'srr'}) # attempt 1
                tree = etree.HTML(response) # none of this seems to work
                meta_type_elts = tree.xpath('//meta[contains(@type,"json")]')
                return  'ERROR: No text gathered'
            if 'post-gazette.com' in url:
                return "ERROR: Article behind a paywall or login page"

            alt = soup.text
            print(f"    No text found for {url}")
            return 'ERROR: No text gathered'
        if stripped_paragraph == [""]:
            if 'grabien' in url:
                return "ERROR: Video/ Image content only"
            if 'israelnationalnews' in url:
                return 'ERROR: Article not found'
            if 'koreaherald.com' in url:
                br_elts = soup.find_all('br')
                div_elts = soup.find_all('div', attrs={'class': 'view_con_t'})
                stripped = [tag.get_text().strip() for tag in br_elts]
                if len(stripped)<1:
                    stripped= [tag.get_text().strip() for tag in div_elts]
                    if len(stripped)<1:
                        return 'ERROR: No text gathered'
                    return " ".join(stripped)
                return " ".join(stripped)
            if 'avoiceformen' in url:
                return "ERROR: Article not found"
            return 'ERROR: No text gathered'

        return " ".join(stripped_paragraph)  # return the content as one string
    else:
        return "ERROR: No soup"


def collect_text(dataset, title, starting_point=1):
    error_count = 0
    if dataset[0][0] == 'stories_id':
        dataset[0].append('article_text')

    for i in range(starting_point, len(dataset)):
        if dataset[i][4] != 'en':  # only scrape English text
            dataset[i].append('ERROR: Not in English')
            continue
        if dataset[i][9] == dataset[i - 1][9]:  # if the same publication is accessed twice in a row, sleep some seconds
            random_time = random.randint(1, 5)
            time.sleep(random_time)
        text = access_article(dataset[i][3])
        dataset[i].append(text)
        if 'ERROR:' in text:
            error_count+=1
        if str(i).endswith('00'):
            # export checkpoint
            uf.export_nested_list(f"{title}_unclean_text_checkpoint_{i}.csv", dataset[:i])
            print(f'Export checkpoint: Creating "{title}_unclean_text_checkpoint_{i}.csv"...')
            properly_scraped = i-starting_point- error_count
            print(f"    {properly_scraped} articles have been successfully scraped")


    # Final export
    uf.export_nested_list(f"{title}_complete_unclean_text.csv", dataset)
    print('PROCESS COMPLETE')

# MAIN FUNCTIONS

def scrape_normally():
    all_queries = [x for x in glob.glob(str(mediacloud_dir)  + "/*.csv")]
    url_queries = [x for x in glob.glob(str(mediacloud_dir)  + "/*.csv") if 'urls' in x]
    for file in url_queries:
        completed_file = file.replace('urls', 'text')
        if completed_file not in all_queries:
            print('Should I scrape this file? Input Y for yes:', file)
            skip = input()
            if skip == 'Y':
                imported_data = uf.import_csv(file)
                new_file_name = file[:-4]
                collect_text(imported_data, new_file_name)


def scrape_from_checkpoint():
    all_queries = [x for x in glob.glob(str(mediacloud_dir) + "/*.csv")]
    url_queries = [x for x in glob.glob(str(mediacloud_dir)  + "/*.csv") if
                   'urls' in x]
    for file in url_queries:
        completed_file = file.replace('urls', 'text')
        if completed_file not in all_queries:
            print('Should I scrape this file? Input Y for yes:', file)
            skip = input()
            if skip == 'Y':
                checkpoint = input("What number should I start at?")
                imported_data = uf.import_csv(file)
                new_file_name = file[:-4]
                collect_text(imported_data, new_file_name, int(checkpoint))

# # # # NORMAL RUN # # #
# scrape_normally()
#
# ## Post-checkpoint run
# scrape_from_checkpoint()


