
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
        # https://youtube.googleapis.com/youtube/v3/videos?part=snippet%2CcontentDetails%2Cstatistics&id=[YID]&key=[ACCESS_KEY]
        # %2C = ,
        # OLD: url_search = 'https://youtube.googleapis.com/youtube/v3/videos?part=snippet%2CcontentDetails%2Cstatistics&id=' + yid + '&key=' + access_token
        url_search = 'https://youtube.googleapis.com/youtube/v3/videos?'
        url_parameters = {'part': 'snippet,contentDetails,statistics',
                          'id': yid,
                          'key': ''
                         }
        response = requests.get(url_search, params = url_parameters)
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
#number_check()


################################################################################
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
#
#
################################################################################
# Sample output from scrapetube
# {
#   "videoId": "eJmutiITt6E",
#   "thumbnail": {
#     "thumbnails": [
#       {
#         "url": "https://i.ytimg.com/vi/eJmutiITt6E/hqdefault.jpg?sqp=-oaymwEbCKgBEF5IVfKriqkDDggBFQAAiEIYAXABwAEG&rs=AOn4CLDYok_meCp1deQnsE29i0Y2rr58Ow",
#         "width": 168,
#         "height": 94
#       },
#       {
#         "url": "https://i.ytimg.com/vi/eJmutiITt6E/hqdefault.jpg?sqp=-oaymwEbCMQBEG5IVfKriqkDDggBFQAAiEIYAXABwAEG&rs=AOn4CLD7IhqEya7B2DoyfqvhbJb5Ms01VA",
#         "width": 196,
#         "height": 110
#       },
#       {
#         "url": "https://i.ytimg.com/vi/eJmutiITt6E/hqdefault.jpg?sqp=-oaymwEcCPYBEIoBSFXyq4qpAw4IARUAAIhCGAFwAcABBg==&rs=AOn4CLCTKvvJOtYIZc1JCfzmSk1FhS4U-Q",
#         "width": 246,
#         "height": 138
#       },
#       {
#         "url": "https://i.ytimg.com/vi/eJmutiITt6E/hqdefault.jpg?sqp=-oaymwEcCNACELwBSFXyq4qpAw4IARUAAIhCGAFwAcABBg==&rs=AOn4CLDYn-LPhc6KW8eZw5LS0yHTKO2l-g",
#         "width": 336,
#         "height": 188
#       }
#     ]
#   },
#   "title": {
#     "runs": [
#       {
#         "text": "When To Go Into Seclusion?"
#       }
#     ],
#     "accessibility": {
#       "accessibilityData": {
#         "label": "When To Go Into Seclusion? by Hillside Hermitage 1 day ago 13 minutes, 39 seconds 873 views"
#       }
#     }
#   },
#   "descriptionSnippet": {
#     "runs": [
#       {
#         "text": "Skilful seclusion vs the unskilful one.\n ____________________________________\nIf you wish to support the monks of the Hillside Hermitage Sangha and this channel you are very welcome to do so..."
#       }
#     ]
#   },
#   "publishedTimeText": {
#     "simpleText": "1 day ago"
#   },
#   "lengthText": {
#     "accessibility": {
#       "accessibilityData": {
#         "label": "13 minutes, 39 seconds"
#       }
#     },
#     "simpleText": "13:39"
#   },
#   "viewCountText": {
#     "simpleText": "873 views"
#   },
#   "navigationEndpoint": {
#     "clickTrackingParams": "COgBENwwIhMI_IKxubeV_gIVo4_lBx1g9wWsWhhVQ0tlam1XQXRfa05wUk1xNWdRRUdBcXeaAQYQ8jgY4AeqARpVVUxGS2VqbVdBdF9rTnBSTXE1Z1FFR0Fxdw==",
#     "commandMetadata": {
#       "webCommandMetadata": {
#         "url": "/watch?v=eJmutiITt6E",
#         "webPageType": "WEB_PAGE_TYPE_WATCH",
#         "rootVe": 3832
#       }
#     },
#     "watchEndpoint": {
#       "videoId": "eJmutiITt6E",
#       "watchEndpointSupportedOnesieConfig": {
#         "html5PlaybackOnesieConfig": {
#           "commonConfig": {
#             "url": "https://rr4---sn-q4flrne6.googlevideo.com/initplayback?source=youtube&oeis=1&c=WEB&oad=3200&ovd=3200&oaad=11000&oavd=11000&ocs=700&oewis=1&oputc=1&ofpcc=1&msp=1&odepv=1&id=7899aeb62213b7a1&ip=98.200.221.194&initcwndbps=1687500&mt=1680789911&oweuc="
#           }
#         }
#       }
#     }
#   },
#   "trackingParams": "COgBENwwIhMI_IKxubeV_gIVo4_lBx1g9wWsQKHvzpDi1uvMeKoBGlVVTEZLZWptV0F0X2tOcFJNcTVnUUVHQXF3",
#   "showActionMenu": false,
#   "shortViewCountText": {
#     "accessibility": {
#       "accessibilityData": {
#         "label": "873 views"
#       }
#     },
#     "simpleText": "873 views"
#   },
#   "menu": {
#     "menuRenderer": {
#       "items": [
#         {
#           "menuServiceItemRenderer": {
#             "text": {
#               "runs": [
#                 {
#                   "text": "Add to queue"
#                 }
#               ]
#             },
#             "icon": {
#               "iconType": "ADD_TO_QUEUE_TAIL"
#             },
#             "serviceEndpoint": {
#               "clickTrackingParams": "CO0BEP6YBBgGIhMI_IKxubeV_gIVo4_lBx1g9wWs",
#               "commandMetadata": {
#                 "webCommandMetadata": {
#                   "sendPost": true
#                 }
#               },
#               "signalServiceEndpoint": {
#                 "signal": "CLIENT_SIGNAL",
#                 "actions": [
#                   {
#                     "clickTrackingParams": "CO0BEP6YBBgGIhMI_IKxubeV_gIVo4_lBx1g9wWs",
#                     "addToPlaylistCommand": {
#                       "openMiniplayer": true,
#                       "videoId": "eJmutiITt6E",
#                       "listType": "PLAYLIST_EDIT_LIST_TYPE_QUEUE",        
#                       "onCreateListCommand": {
#                         "clickTrackingParams": "CO0BEP6YBBgGIhMI_IKxubeV_gIVo4_lBx1g9wWs",
#                         "commandMetadata": {
#                           "webCommandMetadata": {
#                             "sendPost": true,
#                             "apiUrl": "/youtubei/v1/playlist/create"      
#                           }
#                         },
#                         "createPlaylistServiceEndpoint": {
#                           "videoIds": [
#                             "eJmutiITt6E"
#                           ],
#                           "params": "CAQ%3D"
#                         }
#                       },
#                       "videoIds": [
#                         "eJmutiITt6E"
#                       ]
#                     }
#                   }
#                 ]
#               }
#             },
#             "trackingParams": "CO0BEP6YBBgGIhMI_IKxubeV_gIVo4_lBx1g9wWs"  
#           }
#         },
#         {
#           "menuServiceItemDownloadRenderer": {
#             "serviceEndpoint": {
#               "clickTrackingParams": "COwBENGqBRgHIhMI_IKxubeV_gIVo4_lBx1g9wWs",
#               "offlineVideoEndpoint": {
#                 "videoId": "eJmutiITt6E",
#                 "onAddCommand": {
#                   "clickTrackingParams": "COwBENGqBRgHIhMI_IKxubeV_gIVo4_lBx1g9wWs",
#                   "getDownloadActionCommand": {
#                     "videoId": "eJmutiITt6E",
#                     "params": "CAI%3D"
#                   }
#                 }
#               }
#             },
#             "trackingParams": "COwBENGqBRgHIhMI_IKxubeV_gIVo4_lBx1g9wWs"  
#           }
#         },
#         {
#           "menuServiceItemRenderer": {
#             "text": {
#               "runs": [
#                 {
#                   "text": "Share"
#                 }
#               ]
#             },
#             "icon": {
#               "iconType": "SHARE"
#             },
#             "serviceEndpoint": {
#               "clickTrackingParams": "COgBENwwIhMI_IKxubeV_gIVo4_lBx1g9wWs",
#               "commandMetadata": {
#                 "webCommandMetadata": {
#                   "sendPost": true,
#                   "apiUrl": "/youtubei/v1/share/get_share_panel"
#                 }
#               },
#               "shareEntityServiceEndpoint": {
#                 "serializedShareEntity": "CgtlSm11dGlJVHQ2RQ%3D%3D",      
#                 "commands": [
#                   {
#                     "clickTrackingParams": "COgBENwwIhMI_IKxubeV_gIVo4_lBx1g9wWs",
#                     "openPopupAction": {
#                       "popup": {
#                         "unifiedSharePanelRenderer": {
#                           "trackingParams": "COsBEI5iIhMI_IKxubeV_gIVo4_lBx1g9wWs",
#                           "showLoadingSpinner": true
#                         }
#                       },
#                       "popupType": "DIALOG",
#                       "beReused": true
#                     }
#                   }
#                 ]
#               }
#             },
#             "trackingParams": "COgBENwwIhMI_IKxubeV_gIVo4_lBx1g9wWs"      
#           }
#         }
#       ],
#       "trackingParams": "COgBENwwIhMI_IKxubeV_gIVo4_lBx1g9wWs",
#       "accessibility": {
#         "accessibilityData": {
#           "label": "Action menu"
#         }
#       }
#     }
#   },
#   "thumbnailOverlays": [
#     {
#       "thumbnailOverlayTimeStatusRenderer": {
#         "text": {
#           "accessibility": {
#             "accessibilityData": {
#               "label": "13 minutes, 39 seconds"
#             }
#           },
#           "simpleText": "13:39"
#         },
#         "style": "DEFAULT"
#       }
#     },
#     {
#       "thumbnailOverlayToggleButtonRenderer": {
#         "isToggled": false,
#         "untoggledIcon": {
#           "iconType": "WATCH_LATER"
#         },
#         "toggledIcon": {
#           "iconType": "CHECK"
#         },
#         "untoggledTooltip": "Watch later",
#         "toggledTooltip": "Added",
#         "untoggledServiceEndpoint": {
#           "clickTrackingParams": "COoBEPnnAxgBIhMI_IKxubeV_gIVo4_lBx1g9wWs",
#           "commandMetadata": {
#             "webCommandMetadata": {
#               "sendPost": true,
#               "apiUrl": "/youtubei/v1/browse/edit_playlist"
#             }
#           },
#           "playlistEditEndpoint": {
#             "playlistId": "WL",
#             "actions": [
#               {
#                 "addedVideoId": "eJmutiITt6E",
#                 "action": "ACTION_ADD_VIDEO"
#               }
#             ]
#           }
#         },
#         "toggledServiceEndpoint": {
#           "clickTrackingParams": "COoBEPnnAxgBIhMI_IKxubeV_gIVo4_lBx1g9wWs",
#           "commandMetadata": {
#             "webCommandMetadata": {
#               "sendPost": true,
#               "apiUrl": "/youtubei/v1/browse/edit_playlist"
#             }
#           },
#           "playlistEditEndpoint": {
#             "playlistId": "WL",
#             "actions": [
#               {
#                 "action": "ACTION_REMOVE_VIDEO_BY_VIDEO_ID",
#                 "removedVideoId": "eJmutiITt6E"
#               }
#             ]
#           }
#         },
#         "untoggledAccessibility": {
#           "accessibilityData": {
#             "label": "Watch later"
#           }
#         },
#         "toggledAccessibility": {
#           "accessibilityData": {
#             "label": "Added"
#           }
#         },
#         "trackingParams": "COoBEPnnAxgBIhMI_IKxubeV_gIVo4_lBx1g9wWs"      
#       }
#     },
#     {
#       "thumbnailOverlayToggleButtonRenderer": {
#         "untoggledIcon": {
#           "iconType": "ADD_TO_QUEUE_TAIL"
#         },
#         "toggledIcon": {
#           "iconType": "PLAYLIST_ADD_CHECK"
#         },
#         "untoggledTooltip": "Add to queue",
#         "toggledTooltip": "Added",
#         "untoggledServiceEndpoint": {
#           "clickTrackingParams": "COkBEMfsBBgCIhMI_IKxubeV_gIVo4_lBx1g9wWs",
#           "commandMetadata": {
#             "webCommandMetadata": {
#               "sendPost": true
#             }
#           },
#           "signalServiceEndpoint": {
#             "signal": "CLIENT_SIGNAL",
#             "actions": [
#               {
#                 "clickTrackingParams": "COkBEMfsBBgCIhMI_IKxubeV_gIVo4_lBx1g9wWs",
#                 "addToPlaylistCommand": {
#                   "openMiniplayer": true,
#                   "videoId": "eJmutiITt6E",
#                   "listType": "PLAYLIST_EDIT_LIST_TYPE_QUEUE",
#                   "onCreateListCommand": {
#                     "clickTrackingParams": "COkBEMfsBBgCIhMI_IKxubeV_gIVo4_lBx1g9wWs",
#                     "commandMetadata": {
#                       "webCommandMetadata": {
#                         "sendPost": true,
#                         "apiUrl": "/youtubei/v1/playlist/create"
#                       }
#                     },
#                     "createPlaylistServiceEndpoint": {
#                       "videoIds": [
#                         "eJmutiITt6E"
#                       ],
#                       "params": "CAQ%3D"
#                     }
#                   },
#                   "videoIds": [
#                     "eJmutiITt6E"
#                   ]
#                 }
#               }
#             ]
#           }
#         },
#         "untoggledAccessibility": {
#           "accessibilityData": {
#             "label": "Add to queue"
#           }
#         },
#         "toggledAccessibility": {
#           "accessibilityData": {
#             "label": "Added"
#           }
#         },
#         "trackingParams": "COkBEMfsBBgCIhMI_IKxubeV_gIVo4_lBx1g9wWs"      
#       }
#     },
#     {
#       "thumbnailOverlayNowPlayingRenderer": {
#         "text": {
#           "runs": [
#             {
#               "text": "Now playing"
#             }
#           ]
#         }
#       }
#     }
#   ],
#   "richThumbnail": {
#     "movingThumbnailRenderer": {
#       "movingThumbnailDetails": {
#         "thumbnails": [
#           {
#             "url": "https://i.ytimg.com/an_webp/eJmutiITt6E/mqdefault_6s.webp?du=3000&sqp=CPicu6EG&rs=AOn4CLAfCd74qFCic4X3RO2DFewxKJ0PTA",
#             "width": 320,
#             "height": 180
#           }
#         ],
#         "logAsMovingThumbnail": true
#       },
#       "enableHoveredLogging": true,
#       "enableOverlay": true
#     }
#   }
# }