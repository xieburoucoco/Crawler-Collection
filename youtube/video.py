"""
@FileName：video.py
@Description：
@Author：xieburou
@Time：2024/11/11/周一 22:44
@Website：wait...
"""

import os
import pathlib
import re
from urllib import parse

import requests


def extract_video_id(url: str, pattern=r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", group=1) -> str:
    """Extract the ``video_id`` from a YouTube url.

    This function supports the following patterns:

    - :samp:`https://youtube.com/watch?v={video_id}`
    - :samp:`https://youtube.com/embed/{video_id}`
    - :samp:`https://youtu.be/{video_id}`

    :param str url:
        A YouTube url containing a video id.
    :rtype: str
    :returns:
        YouTube video id.
    """
    regex = re.compile(pattern)
    results = regex.search(url)
    if not results:
        raise ValueError("regex_search err")
    return results.group(group)


# YouTube on TV client secrets
_client_id = '861556708454-d6dlm3lh05idd8npek18k6be8ba3oc68.apps.googleusercontent.com'
_client_secret = 'SboVhoG9s0rNafixCSGGKXAT'

# Extracted API keys -- unclear what these are linked to.
# API keys are not required, see: https://github.com/TeamNewPipe/NewPipeExtractor/pull/1168
_api_keys = [
    'AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8',
    'AIzaSyCtkvNIR1HCEwzsqK6JuE6KqpyjusIRI30',
    'AIzaSyA8eiZmM1FaDVjRy-df2KTyQ_vz_yYM39w',
    'AIzaSyC8UYZpvA2eknNex0Pjid0_eTLJoDu6los',
    'AIzaSyCjc_pVEDi4qsv5MtC2dMXzpIaDoRFLsxw',
    'AIzaSyDHQ9ipnphqTzDqZsbtd8_Ru4_kiKVQe2k'
]

_default_clients = {
    'WEB': {
        'innertube_context': {
            'context': {
                'client': {
                    'clientName': 'WEB',
                    'osName': 'Windows',
                    'osVersion': '10.0',
                    'clientVersion': '2.20240709.01.00',
                    'platform': 'DESKTOP'
                }
            }
        },
        'header': {
            'User-Agent': 'Mozilla/5.0',
            'X-Youtube-Client-Name': '1',
            'X-Youtube-Client-Version': '2.20240709.01.00'
        },
        'api_key': 'AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8',
        'require_js_player': True,
        'require_po_token': True
    },

    'WEB_EMBED': {
        'innertube_context': {
            'context': {
                'client': {
                    'clientName': 'WEB_EMBEDDED_PLAYER',
                    'osName': 'Windows',
                    'osVersion': '10.0',
                    'clientVersion': '2.20240530.02.00',
                    'clientScreen': 'EMBED'
                }
            }
        },
        'header': {
            'User-Agent': 'Mozilla/5.0',
            'X-Youtube-Client-Name': '56'
        },
        'api_key': 'AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8',
        'require_js_player': True,
        'require_po_token': False
    },

    'WEB_MUSIC': {
        'innertube_context': {
            'context': {
                'client': {
                    'clientName': 'WEB_REMIX',
                    'clientVersion': '1.20240403.01.00'
                }
            }
        },
        'header': {
            'User-Agent': 'Mozilla/5.0',
            'X-Youtube-Client-Name': '67'
        },
        'api_key': 'AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8',
        'require_js_player': True,
        'require_po_token': False
    },

    'WEB_CREATOR': {
        'innertube_context': {
            'context': {
                'client': {
                    'clientName': 'WEB_CREATOR',
                    'clientVersion': '1.20220726.00.00'
                }
            }
        },
        'header': {
            'User-Agent': 'Mozilla/5.0',
            'X-Youtube-Client-Name': '62'
        },
        'api_key': 'AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8',
        'require_js_player': True,
        'require_po_token': False
    },

    'WEB_SAFARI': {
        'innertube_context': {
            'context': {
                'client': {
                    'clientName': 'WEB',
                    'clientVersion': '2.20240726.00.00',
                }
            }
        },
        'header': {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Safari/605.1.15,gzip(gfe)',
            'X-Youtube-Client-Name': '1'
        },
        'api_key': 'AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8',
        'require_js_player': True,
        'require_po_token': True
    },

    'MWEB': {
        'innertube_context': {
            'context': {
                'client': {
                    'clientName': 'MWEB',
                    'clientVersion': '2.20240726.01.00'
                }
            }
        },
        'header': {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',
            'X-Youtube-Client-Name': '2'
        },
        'api_key': 'AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8',
        'require_js_player': True,
        'require_po_token': False
    },

    'ANDROID': {
        'innertube_context': {
            'context': {
                'client': {
                    'clientName': 'ANDROID',
                    'clientVersion': '19.29.37',
                    'platform': 'MOBILE',
                    'osName': 'Android',
                    'osVersion': '14',
                    'androidSdkVersion': '34'
                }
            }
        },
        'header': {
            'User-Agent': 'com.google.android.youtube/',
            'X-Youtube-Client-Name': '3'
        },
        'api_key': 'AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8',
        'require_js_player': False,
        'require_po_token': True
    },

    # Deprecated
    #   'ANDROID_EMBED': {
    #     'innertube_context': {
    #         'context': {
    #             'client': {
    #                 'clientName': 'ANDROID_EMBEDDED_PLAYER',
    #                 'clientVersion': '19.13.36',
    #                 'clientScreen': 'EMBED',
    #                 'androidSdkVersion': '30'
    #             }
    #         }
    #     },
    #     'header': {
    #         'User-Agent': 'com.google.android.youtube/',
    #         'X-Youtube-Client-Name': '55',
    #         'X-Youtube-Client-Version': '19.13.36'
    #     },
    #     'api_key': 'AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8',
    #     'require_js_player': False
    # },

    'ANDROID_VR': {
        'innertube_context': {
            'context': {
                'client': {
                    'clientName': 'ANDROID_VR',
                    'clientVersion': '1.57.29',
                    'deviceMake': 'Oculus',
                    'deviceModel': 'Quest 3',
                    'osName': 'Android',
                    'osVersion': '12L',
                    'androidSdkVersion': '32'
                }
            }
        },
        'header': {
            'User-Agent': 'com.google.android.apps.youtube.vr.oculus/1.57.29 (Linux; U; Android 12L; eureka-user Build/SQ3A.220605.009.A1) gzip',
            'X-Youtube-Client-Name': '28'
        },
        'api_key': 'AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8',
        'require_js_player': False,
        'require_po_token': False
    },

    'ANDROID_MUSIC': {
        'innertube_context': {
            'context': {
                'client': {
                    'clientName': 'ANDROID_MUSIC',
                    'clientVersion': '7.11.50',
                    'androidSdkVersion': '30',
                    'osName': 'Android',
                    'osVersion': '11'
                }
            }
        },
        'header': {
            'User-Agent': 'com.google.android.apps.youtube.music/7.11.50 (Linux; U; Android 11) gzip',
            'X-Youtube-Client-Name': '21'
        },
        'api_key': 'AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8',
        'require_js_player': False,
        'require_po_token': False
    },

    'ANDROID_CREATOR': {
        'innertube_context': {
            'context': {
                'client': {
                    'clientName': 'ANDROID_CREATOR',
                    'clientVersion': '24.30.100',
                    'androidSdkVersion': '30',
                    'osName': 'Android',
                    'osVersion': '11'
                }
            }
        },
        'header': {
            'User-Agent': 'com.google.android.apps.youtube.creator/24.30.100 (Linux; U; Android 11) gzip',
            'X-Youtube-Client-Name': '14'
        },
        'api_key': 'AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8',
        'require_js_player': False,
        'require_po_token': False
    },

    'ANDROID_TESTSUITE': {
        'innertube_context': {
            'context': {
                'client': {
                    'clientName': 'ANDROID_TESTSUITE',
                    'clientVersion': '1.9',
                    'platform': 'MOBILE',
                    'osName': 'Android',
                    'osVersion': '14',
                    'androidSdkVersion': '34'
                }
            }
        },
        'header': {
            'User-Agent': 'com.google.android.youtube/',
            'X-Youtube-Client-Name': '30',
            'X-Youtube-Client-Version': '1.9'
        },
        'api_key': 'AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8',
        'require_js_player': False,
        'require_po_token': False
    },

    'ANDROID_PRODUCER': {
        'innertube_context': {
            'context': {
                'client': {
                    'clientName': 'ANDROID_PRODUCER',
                    'clientVersion': '0.111.1',
                    'androidSdkVersion': '30',
                    'osName': 'Android',
                    'osVersion': '11'
                }
            }
        },
        'header': {
            'User-Agent': 'com.google.android.apps.youtube.producer/0.111.1 (Linux; U; Android 11) gzip',
            'X-Youtube-Client-Name': '91'
        },
        'api_key': 'AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8',
        'require_js_player': False,
        'require_po_token': False
    },

    'IOS': {
        'innertube_context': {
            'context': {
                'client': {
                    'clientName': 'IOS',
                    'clientVersion': '19.29.1',
                    'deviceMake': 'Apple',
                    'platform': 'MOBILE',
                    'osName': 'iPhone',
                    'osVersion': '17.5.1.21F90',
                    'deviceModel': 'iPhone16,2'
                }
            }
        },
        'header': {
            'User-Agent': 'com.google.ios.youtube/19.29.1 (iPhone16,2; U; CPU iOS 17_5_1 like Mac OS X;)',
            'X-Youtube-Client-Name': '5'
        },
        'api_key': 'AIzaSyB-63vPrdThhKuerbB2N_l7Kwwcxj6yUAc',
        'require_js_player': False,
        'require_po_token': False
    },

    # Deprecated
    # 'IOS_EMBED': {
    #     'innertube_context': {
    #         'context': {
    #             'client': {
    #                 'clientName': 'IOS_MESSAGES_EXTENSION',
    #                 'clientVersion': '19.16.3',
    #                 'deviceMake': 'Apple',
    #                 'platform': 'MOBILE',
    #                 'osName': 'iOS',
    #                 'osVersion': '17.4.1.21E237',
    #                 'deviceModel': 'iPhone15,5'
    #             }
    #         }
    #     },
    #     'header': {
    #         'User-Agent': 'com.google.ios.youtube/',
    #         'X-Youtube-Client-Name': '66'
    #     },
    #     'api_key': 'AIzaSyB-63vPrdThhKuerbB2N_l7Kwwcxj6yUAc',
    #     'require_js_player': False
    # },

    'IOS_MUSIC': {
        'innertube_context': {
            'context': {
                'client': {
                    'clientName': 'IOS_MUSIC',
                    'clientVersion': '7.08.2',
                    'deviceMake': 'Apple',
                    'platform': 'MOBILE',
                    'osName': 'iPhone',
                    'osVersion': '17.5.1.21F90',
                    'deviceModel': 'iPhone16,2'
                }
            }
        },
        'header': {
            'User-Agent': 'com.google.ios.youtubemusic/7.08.2 (iPhone16,2; U; CPU iOS 17_5_1 like Mac OS X;)',
            'X-Youtube-Client-Name': '26'
        },
        'api_key': 'AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8',
        'require_js_player': False,
        'require_po_token': False
    },

    'IOS_CREATOR': {
        'innertube_context': {
            'context': {
                'client': {
                    'clientName': 'IOS_CREATOR',
                    'clientVersion': '24.30.100',
                    'deviceMake': 'Apple',
                    'deviceModel': 'iPhone16,2',
                    'osName': 'iPhone',
                    'osVersion': '17.5.1.21F90'
                }
            }
        },
        'header': {
            'User-Agent': 'com.google.ios.ytcreator/24.30.100 (iPhone16,2; U; CPU iOS 17_5_1 like Mac OS X;)',
            'X-Youtube-Client-Name': '15'
        },
        'api_key': 'AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8',
        'require_js_player': False,
        'require_po_token': False
    },

    'TV_EMBED': {
        'innertube_context': {
            'context': {
                'client': {
                    'clientName': 'TVHTML5_SIMPLY_EMBEDDED_PLAYER',
                    'clientVersion': '2.0',
                    'clientScreen': 'EMBED',
                    'platform': 'TV'
                }
            }
        },
        'header': {
            'User-Agent': 'Mozilla/5.0',
            'X-Youtube-Client-Name': '85'
        },
        'api_key': 'AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8',
        'require_js_player': True,
        'require_po_token': False
    },

    'MEDIA_CONNECT': {
        'innertube_context': {
            'context': {
                'client': {
                    'clientName': 'MEDIA_CONNECT_FRONTEND',
                    'clientVersion': '0.1'
                }
            }
        },
        'header': {
            'User-Agent': 'Mozilla/5.0',
            'X-Youtube-Client-Name': '95'
        },
        'api_key': 'AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8',
        'require_js_player': False,
        'require_po_token': False
    }
}
_token_timeout = 1800
_cache_dir = pathlib.Path(__file__).parent.resolve() / '__cache__'
_token_file = os.path.join(_cache_dir, 'tokens.json')

base_headers = {"User-Agent": "Mozilla/5.0", "accept-language": "en-US,en"}


class InnerTube:
    """Object for interacting with the innertube API."""

    def __init__(
            self,
            url,
            client='ANDROID_VR',
            use_oauth=False,
            allow_cache=True,
            token_file=None,
            oauth_verifier=None,
            use_po_token=False,
            po_token_verifier=None

    ):
        """Initialize an InnerTube object.

        :param str client:
            Client to use for the object.
            The default is ANDROID_TESTSUITE because there is no need to decrypt the
            signature cipher and throttling parameter.
        :param bool use_oauth:
            (Optional) Whether or not to authenticate to YouTube.
        :param bool allow_cache:
            (Optional) Allows caching of oauth tokens on the machine.
        :param str token_file:
            (Optional) Path to the file where the OAuth and Po tokens will be stored.
            Defaults to None, which means the tokens will be stored in the pytubefix/__cache__ directory.
        :param Callable oauth_verifier:
            (Optional) Verifier to be used for getting outh tokens.
            Verification URL and User-Code will be passed to it respectively.
            (if passed, else default verifier will be used)
        :param bool use_po_token:
            (Optional) Whether or not to use po_token to bypass YouTube bot detector.
            It must be sent with the API along with the linked visitorData and
            then passed as a `po_token` query parameter to affected clients.
        :param Callable po_token_verifier:
            (Optional) Verified used to obtain the visitorData and po_token.
            The verifier will return the visitorData and po_token respectively.
            (if passed, else default verifier will be used)
        """
        self.innertube_context = _default_clients[client]['innertube_context']
        # video_id part of /watch?v=<video_id>
        self.video_id = extract_video_id(url)

    @property
    def base_url(self) -> str:
        """Return the base url endpoint for the innertube API."""
        return 'https://www.youtube.com/youtubei/v1'

    @property
    def base_data(self) -> dict:
        """Return the base json data to transmit to the innertube API."""
        return self.innertube_context

    @property
    def base_params(self):
        """Return the base query parameters to transmit to the innertube API."""
        return {
            'prettyPrint': "false"
        }

    def _call_api(self, endpoint, query, data):
        """Make a request to a given endpoint with the provided query parameters and data."""
        # When YouTube used an API key, it was necessary to remove it when using oauth
        # if self.use_oauth:
        #     del query['key']

        endpoint_url = f'{endpoint}?{parse.urlencode(query)}'

        headers = {
            'Content-Type': 'application/json',
        }
        base_headers.update(headers)
        return requests.post(endpoint_url, headers=base_headers, json=data)

    def player(self):
        """Make a request to the player endpoint.

        :param str video_id:
            The video id to get player info for.
        :rtype: dict
        :returns:
            Raw player info results.
        """
        endpoint = f'{self.base_url}/player'
        query = self.base_params

        self.base_data.update({'videoId': self.video_id, 'contentCheckOk': "true"})
        return self._call_api(endpoint, query, self.base_data)

    def search(self, search_query, continuation=None, data=None):
        """Make a request to the search endpoint.

        :param str search_query:
            The query to search.
        :param str continuation:
            Continuation token if there is pagination
        :param dict data:
            Additional data to send with the request.
        :rtype: dict
        :returns:
            Raw search query results.
        """
        endpoint = f'{self.base_url}/search'
        query = self.base_params
        data = data if data else {}

        self.base_data.update({'query': search_query})
        if continuation:
            data['continuation'] = continuation
        data.update(self.base_data)
        return self._call_api(endpoint, query, data)


if __name__ == '__main__':
    yt = InnerTube(
        url="https://www.youtube.com/watch?v=IiA2KZ77zgQ",  # 主页链接
    )
    response = yt.player()
    res = response.json()
    formats = res["streamingData"]["adaptiveFormats"]
    for row in formats:
        print(row)
