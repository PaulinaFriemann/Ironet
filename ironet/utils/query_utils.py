import requests
from requests.exceptions import ProxyError, ConnectionError
from bs4 import BeautifulSoup
import math
import time
import sys
from functools import wraps
import string


def retry(tries, delay=0.1, backoff=2):

    if backoff <= 1:
        raise ValueError("backoff must be greater than 1")

    tries = math.floor(tries)
    if tries < 0:
        raise ValueError("tries must be 0 or greater")

    if delay <= 0:
        raise ValueError("delay must be greater than 0")

    def deco_retry(f):
        @wraps(f)
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay  # make mutable

            while mtries > 0:
                try:
                    result = f(*args, **kwargs)  # first attempt
                    return result

                except ProxyError, e:
                    print str(e)

                    mtries -= 1  # consume an attempt
                    time.sleep(mdelay)  # wait...
                    mdelay *= backoff  # make future wait longer
                    print "try again"

            return f(*args, **kwargs)  # Ran out of tries :-(

        return f_retry  # true decorator -> decorated function
    return deco_retry  # @retry(arg[, ...]) -> true decorator


def search_query(query, vehicle):

    while True:
        try:
            r = requests.get('http://www.google.com/search',
                             params={'as_epq': query,
                                     "tbs": "qdr:a"},
                             #proxies={"http": "http://188.40.110.2"},
                             headers={"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.2.9) Gecko/20100722 Firefox/3.6.7 GTB7.1 (.NET CLR 3.5.30729)"},
                             timeout=30,
                             stream=True
                         )
        except ProxyError, e:
            print "shit ", e

        except ConnectionError, e:
            print "bla", e

        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise
        else:

            if str(r.url).startswith("http://ipv6.google.com/sorry/IndexRedirect?") or str(r.url).startswith("http://ipv4.google.com/sorry/IndexRedirect?"):
                print "got kicked out"
                raise ProxyError

            else:
                return get_result_stats(r, vehicle)


def get_result_stats(result, vehicle):
    soup = BeautifulSoup(result.text, "html.parser")
    bla = soup.find_all('b')
    blastr = [blabla.string for blabla in bla]
    if blastr.__contains__(vehicle.replace("_", " ")):
        return '0'

    # gets the number of search results
    return soup.find('div', {'id': 'resultStats'}).text


@retry(tries=4)
def get_num_results(query, vehicle):

    query = query.replace("_", " ")
    #print query
    try:
        text = search_query(query, vehicle)
    except ProxyError:
        print "had error, change proxy "
        raise

    print "text " + str(text)
    if text[0] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
        number = text.split(" ")[0]
    else:
        number = text.split(" ")[1]

    number = number.replace(".", "")
    number = number.replace(",", "")
    number = number.replace(" ", "")
    number = number.replace("\'", "")
    number = number.strip(string.whitespace)

    return int(number)
