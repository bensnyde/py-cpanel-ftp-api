py-cpanel-ftp-api
=================

**Python Library for WHM/Cpanel's API2 FTP Module**

https://documentation.cpanel.net/display/SDK/cPanel+API+2+-+Ftp

- Author: Benton Snyder
- Website: http://bensnyde.me
- Created: 8/15/13
- Revised: 1/2/15

Installation
---
```
# pip install py-cpanel-ftp-api
```

Usage
---
```
from cpanel_ftp_api import CpanelFTP

cpanel = CpanelFTP("whm.example.com", "root", "strongpassword", "some_cpanel_user")
print cpanel.listftp()
```
