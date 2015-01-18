jishu-pro
=========

Apache + sudo
---

```bash
sudo visudo

www-data  ALL=(ALL) NOPASSWD: /usr/bin/python
```

Hosting
---

edit `/etc/apache2/sites-available/jishupro.conf`
```
<VirtualHost *:80>
  ServerName keyopener.ddo.jp
  WSGIScriptAlias / /home/pi/Work/jishupro/website/jishupro.wsgi
</VirtualHost>
```

```bash
sudo a2ensite jishupro.conf
sudo apachectl restart
```
