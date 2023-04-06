
import os, scrapetube, json, requests, pandas as pd, csv
from datetime import datetime


def create_txt_files():
    # Read file
    with open('git/hillside-hermitage-talks/resources/all_recordings.txt', encoding = 'utf8') as mr:
        lines = mr.readlines()
    all_lines = []
    for i in lines:
        all_lines.append(i.replace('\n', '') + '.txt')
    for i in all_lines:
        with open('git/hillside-hermitage-talks/working/' + i, 'w') as wd:
            wd.write('In process...')
        print('Created: ' + i)


def scrape_hh():
    # Change working directory to this file
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    # To find channel ID: https://commentpicker.com/youtube-channel-id.php
    videos = scrapetube.get_channel('UCKejmWAt_kNpRMq5gQEGAqw')
    list_tid = []
    list_name = []
    list_date = []
    list_link = []
    # Save completed talk data to be referenced later
    cdf = pd.read_csv('completed_results.csv')    
    for i in videos:
        # print(json.dumps(i, indent = 2))
        print('Working: ' + i['title']['runs'][0]['text'])
        # Save video ID
        yid = i['videoId']
        ylink = 'https://www.youtube.com/watch?v=' + str(yid)
        # Check if file is already completed from before
        ltid = 0
        # Only change variable if value was found, and only append if it was found
        for j in cdf.iterrows():
            if j[1][3] == ylink:
                ltid = 1
                break
            else:
                ltid = 0
        if ltid == 1:
            list_tid.append(j[1][1])
        else:
            list_tid.append('-')
        # Append data to appropriate lists
        list_name.append(i['title']['runs'][0]['text'])
        list_link.append(ylink)
        # Start API search
        access_token = ''
        url_search = 'https://youtube.googleapis.com/youtube/v3/videos?part=snippet%2CcontentDetails%2Cstatistics&id=' + yid + '&key=' + access_token
        response = requests.get(url_search)
        # Parse date, convert, then append to list; must be converted to json first
        dtime = response.json()['items'][0]['snippet']['publishedAt']
        updated_dtime = datetime.strptime(dtime[:10], '%Y-%m-%d')
        list_date.append(updated_dtime.strftime('%m/%d/%Y'))
    # Save all results in dictionary
    results = {'TALK_ID': list_tid,
               'NAME': list_name,
               'PUBLISHED_DATE': list_date,
               'LINK': list_link,
              }
    df = pd.DataFrame(results)
    df.to_csv('results.csv')
    print(df)


def get_urls():
    # Change current working directory to this file
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    dir_comp = '../completed'
    clist_num = []
    clist_name = []
    clist_link = []
    for i in os.listdir(dir_comp):
        # Remove leading 0's
        clist_num.append(i.split('_')[1].lstrip('0'))
        # Open file and read lines
        with open(dir_comp + '/' + i, encoding = 'utf8') as mr:
            lines = mr.readlines()
        # Parse TITLE and LINK
        for j in lines:
            if j.startswith('TITLE: '):
                clist_name.append(j.replace('TITLE: ', '').replace('\n', ''))
            if j.startswith('LINK: '):
                clist_link.append(j.replace('LINK: ', '').replace('\n', ''))
    # Add to data frame
    results = {'TALK_NUM': clist_num,
               'TITLE': clist_name,
               'LINK': clist_link
               }
    # Save as pandas data frame
    df = pd.DataFrame(results)
    df.to_csv('completed_results.csv')


# Error check: shows correct amount of records that have been referenced
def number_check():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    df = pd.read_csv('results.csv')
    x = 0
    for i in df.iterrows():
        if i[1][1] != '-':
            x += 1
    print(x)


#create_txt_files()
#scrape_hh()
#get_urls()
#dev003()


# Sample output of youtube api data:
# print(json.dumps(response.json(), indent = 2))
# {
#   "kind": "youtube#videoListResponse",
#   "etag": "rniwrlJSqipKBANcfY4CSBUnwV0",
#   "items": [
#     {
#       "kind": "youtube#video",
#       "etag": "IZQNliKId5i46j9RLCABn48AizM",
#       "id": "eJmutiITt6E",
#       "snippet": {
#         "publishedAt": "2023-04-05T12:30:31Z",        
#         "channelId": "UCKejmWAt_kNpRMq5gQEGAqw",      
#         "title": "When To Go Into Seclusion?",        
#         "description": "Skilful seclusion vs the unskilful one.\n ____________________________________\nIf you wish to support the monks of the Hillside Hermitage Sangha and this channel you are very welcome to do so via:\nhttps://www.hillsidehermitage.org/support-us\n____________________________________\nAUDIO FILES AND TRANSCRIPTS OF OUR YOUTUBE DHAMMA TALKS\nhttps://t.me/HillsideHermitage\n____________________________________\nMORE TEACHINGS:\nhttps://www.hillsidehermitage.org/teachings",
#         "thumbnails": {
#           "default": {
#             "url": "https://i.ytimg.com/vi/eJmutiITt6E/default.jpg",
#             "width": 120,
#             "height": 90
#           },
#           "medium": {
#             "url": "https://i.ytimg.com/vi/eJmutiITt6E/mqdefault.jpg",
#             "width": 320,
#             "height": 180
#           },
#           "high": {
#             "url": "https://i.ytimg.com/vi/eJmutiITt6E/hqdefault.jpg",
#             "width": 480,
#             "height": 360
#           },
#           "standard": {
#             "url": "https://i.ytimg.com/vi/eJmutiITt6E/sddefault.jpg",
#             "width": 640,
#             "height": 480
#           },
#           "maxres": {
#             "url": "https://i.ytimg.com/vi/eJmutiITt6E/maxresdefault.jpg",
#             "width": 1280,
#             "height": 720
#           }
#         },
#         "channelTitle": "Hillside Hermitage",
#         "tags": [
#           "ajahn nyanamoli thero",
#           "ajahn chah",
#           "forest monks",
#           "sotapanna",
#           "sotapatti",
#           "nibbana",
#           "buddhist meditation",
#           "suttas",
#           "anagami",
#           "arahant",
#           "jhana",
#           "four jhanas",
#           "dhamma talk",
#           "dhammatalks",
#           "five hindrances",
#           "sutta reading",
#           "sutta simile",
#           "anicca",
#           "dukkha",
#           "jhana meditation",
#           "jhana technique",
#           "jhanas",
#           "four noble truths",
#           "virtue",
#           "samadhi",
#           "satipatthana",
#           "majjhima nikaya",
#           "ajahn brahm",
#           "theravada",
#           "early buddhist suttas",
#           "gradual training",
#           "dhamma interrogation",
#           "dhamma questions"
#         ],
#         "categoryId": "27",
#         "liveBroadcastContent": "none",
#         "defaultLanguage": "en-GB",
#         "localized": {
#           "title": "When To Go Into Seclusion?",      
#           "description": "Skilful seclusion vs the unskilful one.\n ____________________________________\nIf you wish to support the monks of the Hillside Hermitage Sangha and this channel you are very welcome to do 
# so via:\nhttps://www.hillsidehermitage.org/support-us\n____________________________________\nAUDIO FILES AND TRANSCRIPTS OF OUR YOUTUBE DHAMMA TALKS\nhttps://t.me/HillsideHermitage\n____________________________________\nMORE TEACHINGS:\nhttps://www.hillsidehermitage.org/teachings"
#         },
#         "defaultAudioLanguage": "en"
#       },
#       "contentDetails": {
#         "duration": "PT13M39S",
#         "dimension": "2d",
#         "definition": "hd",
#         "caption": "false",
#         "licensedContent": true,
#         "contentRating": {},
#         "projection": "rectangular"
#       },
#       "statistics": {
#         "viewCount": "656",
#         "likeCount": "50",
#         "favoriteCount": "0",
#         "commentCount": "3"
#       }
#     }
#   ],
#   "pageInfo": {
#     "totalResults": 1,
#     "resultsPerPage": 1
#   }
# }
