from os import path, getcwd
import logging
from requests import get
from random import choice, randint
from time import sleep
from bs4 import BeautifulSoup
from threading import Lock

log = logging.getLogger(__name__)


class ContextSingleton(type):
    _instances = {}
    lock = Lock()
    with lock:
        def __call__(cls, *args, **kwargs):
            if cls not in cls._instances:
                cls._instances[cls] = super(ContextSingleton, cls).__call__(*args, **kwargs)
            return cls._instances[cls]


class ParseContext(metaclass=ContextSingleton):
    """ Class provide convinient evironment for parsing, e.g. User-Agents and free elite proxies updated online from free-proxi-list.net.
        
        Methods
        ---------
        ParseContext.get_ua() -> str
            Return arbitirary User-Agent.

        ParseContext.pop_proxy() -> str
            Pop available proxie [LIFO].
        
        ParseContext.push_proxy() -> str
            Push back used proxie after success [LIFO].

        Private:
        self._init_proxie(self, full=False)
            - full=False: Method inits User-Agents only for desktop and mobile browsers.
            - full=True: Method inits all available types of User-Agents.
    """
    def __init__(self):
        self.user_agents = self._init_user_agents()
        self.proxies = self._init_proxies()
        self.lock = Lock()
    
    def _init_user_agents(self, full=False):
        """ Load fake User-Agents from file

            Parameters
            ----------
            full : bool
                Load Agents from long list if `True`.
            
            Return
            -------
            ua_list : list
                Return list of fake User-Agents if soure exist, else return default UA.
        """
        __location__ = path.realpath(path.join(getcwd(), path.dirname(__file__)))
        ua_source = ['useragents.csv','useragentswitcher_short.csv', 'useragentswitcher.csv']
        ua_list = list()
        try:
            i = 1 if full else 0
            if i == 0:
                log.debug('Init UA: Reading UA from `useragents.csv.`')
                with open(path.join(__location__, ua_source[i]), 'r') as f:
                    for line in f:
                        ua_list.append(line[:-2])
                return ua_list
            else:
                log.debug('Init UA: Reading UA from `useragentswitcher_short.csv.`')
                with open(path.join(__location__, ua_source[i]), 'r') as f:
                    f.readline()
                    for line in f:
                        ua_list.append(line.split('","')[2][:-2])
                return ua_list
        except:
            log.error('Init UA: No User-Agent source list found! Default User-Agent returned.')
            return ['Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36']

    def _init_proxies(self):
        """ Load list of 'elite' proxies from `free-proxy-list.net`.

            Raise `Exception` if no connection to server.
        """
        url = 'https://free-proxy-list.net/'
        log.debug('Init proxies: Getting proxy list from web...')
        try:
            soup = BeautifulSoup(get(url).text, "html5lib")
            proxies = list()
            for tr in soup.select('#proxylisttable > tbody > tr'):
                td = tr.select('td')
                if (td[4].text == 'elite proxy') & (td[6].text == 'yes'):
                    proxies.append(':'.join([td[0].text, td[1].text]))
            return proxies
        except:
            log.exception('Failed to download proxy list.')
            raise

    def get_ua(self):
        """Return random UA-string from UA list."""
        with self.lock:
            return choice(self.user_agents)

    def pop_proxy(self):
        """ Pop available proxy server address as `<ip>:<port>`
        
            Reload proxy list if there are less than 2 servers.
        """
        with self.lock:
            if len(self.proxies) > 2:
                return self.proxies.pop()
            elif not self.proxies:
                self.proxies = self._init_proxies()
                return self.proxies.pop()
            else:
                last_proxy = self.proxies[0]
                very_last_proxy = self.proxies[1]
                self.proxies = self._init_proxies()
                self.proxies.append(last_proxy)
                self.proxies.append(very_last_proxy)
                return self.proxies.pop()
        
    def push_proxy(self, proxy):
        """Push back used proxy after successful run."""
        with self.lock:
            self.proxies.append(proxy)

if __name__ == "__main__":
    pass
