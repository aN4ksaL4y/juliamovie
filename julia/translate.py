import json
import requests
import random, re
import urllib3
import logging
from urllib.parse import quote

from julia.constant import LANGUAGES, DEFAULT_SERVICE_URLS

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

URLS_SUFFIX = [re.search('translate.google.(.*)', url.strip()).group(1) for url in DEFAULT_SERVICE_URLS]
URL_SUFFIX_DEFAULT = 'cn'
class google_translator:
    def __init__(self, url_suffix="cn", timeout=5, proxies=None):
        self.proxies = proxies
        if url_suffix not in URLS_SUFFIX:
            self.url_suffix = URL_SUFFIX_DEFAULT
        else:
            self.url_suffix = url_suffix
        url_base = "https://translate.google.{}".format(self.url_suffix)
        self.url = url_base + "/_/TranslateWebserverUi/data/batchexecute"
        self.timeout = timeout

    def _package_rpc(self, text, lang_src='auto', lang_tgt='auto'):
        GOOGLE_TTS_RPC = ["MkEWBc"]
        parameter = [[text.strip(), lang_src, lang_tgt, True], [1]]
        escaped_parameter = json.dumps(parameter, separators=(',', ':'))
        rpc = [[[random.choice(GOOGLE_TTS_RPC), escaped_parameter, None, "generic"]]]
        espaced_rpc = json.dumps(rpc, separators=(',', ':'))
        # text_urldecode = quote(text.strip())
        freq_initial = "f.req={}&".format(quote(espaced_rpc))
        freq = freq_initial
        return freq

    def translate(self, text, lang_tgt='in', lang_src='en', pronounce=False):
        try:
            lang = LANGUAGES[lang_src]
        except:
            lang_src = 'auto'
        try:
            lang = LANGUAGES[lang_tgt]
        except:
            lang_src = 'auto'
        text = str(text)
        if len(text) >= 5000:
            return "Warning: Can only detect less than 5000 characters"
        if len(text) == 0:
            return ""
        headers = {
            "Referer": "http://translate.google.{}/".format(self.url_suffix),
            "User-Agent":
                "Mozilla/5.0 (Windows NT 10.0; WOW64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/47.0.2526.106 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded;charset=utf-8"
        }
        freq = self._package_rpc(text, lang_src, lang_tgt)
        response = requests.Request(method='POST',
                                    url=self.url,
                                    data=freq,
                                    headers=headers,
                                    )
        try:
            if self.proxies == None or type(self.proxies) != dict:
                self.proxies = {}
            with requests.Session() as s:
                s.proxies = self.proxies
                r = s.send(request=response.prepare(),
                           verify=False,
                           timeout=self.timeout)
            for line in r.iter_lines(chunk_size=1024):
                decoded_line = line.decode('utf-8')
                if "MkEWBc" in decoded_line:
                    try:
                        response = decoded_line
                        response = json.loads(response)
                        response = list(response)
                        response = json.loads(response[0][2])
                        response_ = list(response)
                        response = response_[1][0]
                        if len(response) == 1:
                            if len(response[0]) > 5:
                                sentences = response[0][5]
                            else: ## only url
                                sentences = response[0][0]
                                if pronounce == False:
                                    return sentences
                                elif pronounce == True:
                                    return [sentences,None,None]
                            translate_text = ""
                            for sentence in sentences:
                                sentence = sentence[0]
                                translate_text += sentence.strip() + ' '
                            translate_text = translate_text
                            if pronounce == False:
                                return translate_text
                            elif pronounce == True:
                                pronounce_src = (response_[0][0])
                                pronounce_tgt = (response_[1][0][0][1])
                                return [translate_text, pronounce_src, pronounce_tgt]
                        elif len(response) == 2:
                            sentences = []
                            for i in response:
                                sentences.append(i[0])
                            if pronounce == False:
                                return sentences
                            elif pronounce == True:
                                pronounce_src = (response_[0][0])
                                pronounce_tgt = (response_[1][0][0][1])
                                return [sentences, pronounce_src, pronounce_tgt]
                    except Exception as e:
                        raise e
            r.raise_for_status()
        except requests.exceptions.ConnectTimeout as e:
            raise e
        except requests.exceptions.HTTPError as e:
            # Request successful, bad response
            pass
        except requests.exceptions.RequestException as e:
            # Request failed
            pass

    def detect(self, text):
        text = str(text)
        if len(text) >= 5000:
            return log.debug("Warning: Can only detect less than 5000 characters")
        if len(text) == 0:
            return ""
        headers = {
            "Referer": "http://translate.google.{}/".format(self.url_suffix),
            "User-Agent":
                "Mozilla/5.0 (Windows NT 10.0; WOW64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/47.0.2526.106 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded;charset=utf-8"
        }
        freq = self._package_rpc(text)
        response = requests.Request(method='POST',
                                    url=self.url,
                                    data=freq,
                                    headers=headers)
        try:
            if self.proxies == None or type(self.proxies) != dict:
                self.proxies = {}
            with requests.Session() as s:
                s.proxies = self.proxies
                r = s.send(request=response.prepare(),
                           verify=False,
                           timeout=self.timeout)

            for line in r.iter_lines(chunk_size=1024):
                decoded_line = line.decode('utf-8')
                if "MkEWBc" in decoded_line:
                    # regex_str = r"\[\[\"wrb.fr\",\"MkEWBc\",\"\[\[(.*).*?,\[\[\["
                    try:
                        # data_got = re.search(regex_str,decoded_line).group(1)
                        response = (decoded_line + ']')
                        response = json.loads(response)
                        response = list(response)
                        response = json.loads(response[0][2])
                        response = list(response)
                        detect_lang = response[0][2]
                    except Exception:
                        raise Exception
                    # data_got = data_got.split('\\\"]')[0]
                    return [detect_lang, LANGUAGES[detect_lang.lower()]]
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            # Request successful, bad response
            log.debug(str(e))
            pass
        except requests.exceptions.RequestException as e:
            # Request failed
            log.debug(str(e))
            pass