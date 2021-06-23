## ETF SEARCH WEB
Web application for etfsearch.info

### Architecture
```
nginx -   gunicorn   - flask - elasticsearch
(WEB)   (MIDDLEWARE)   (WAS)   (SEARCH ENGINE)
```
