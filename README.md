Usage example
================

Create an instance of `ParseContext` class.

```
from free_proxy import ParseContext

pcn = ParseContext()
```

Get random User-Agent

```
ua = pcn.get_ua()
print(ua)

>>> 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'
```

Get proxy-server

```
# Get available proxy-server
proxy = pcn.pop_proxy()
print(proxy)

>>>'123.xxx.xxx.109:80'

# Push back valid server
pcn.push_proxy(proxy)
```
