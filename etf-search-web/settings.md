### supervisorctl
```
vi /etc/supervisor/conf.d/etf-search-web.conf
[program:etf-search-web]
command=/home/jemin/work/etf-search-web/etf-search-web/venv/bin/python3 /home/jemin/work/etf-search-web/etf-search-web/venv/bin/gunicorn -w 4 -b 0.0.0.0:8888 "main:create_app('production')"
directory=/home/jemin/work/etf-search-web/etf-search-web
autostart=true
redirect_stderr=true
```
### nginx
```
vi /etc/nginx/sites-available/etfsearch.info.conf
server {
            listen 8080;
            server_name etfsearch.info www.etfsearch.info;
            location / {
               proxy_pass http://127.0.0.1:8888;
            }
}

ln -s /etc/nginx/sites-available/etfsearch.info.conf /etc/nginx/sites-enabled/etfsearch.info.conf
```