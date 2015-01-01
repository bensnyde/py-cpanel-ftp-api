py-cpanel-ftp-api
=================

**Python Library for WHM/Cpanel's API2 FTP Module**

:Info: See <http://docs.cpanel.net/twiki/bin/view/ApiDocs/Api2/ApiFtp> for API implementation.<br />
:Author: Benton Snyder <introspectr3@gmail.com><br />
:Website: Noumenal Designs <http://www.noumenaldesigns.com><br />
:Date: $Date: 2013-08-15 23:02:21 -0600 (Thurs, 15 Aug 2013) $<br />
:Revision: $Revision: 0004 $<br />
:Description: Python library for interfacing FTP functions with Cpanel <http://www.cpanel.net><br />

https://documentation.cpanel.net/display/SDK/cPanel+API+2+-+Ftp

- Author: Benton Snyder
- Website: http://bensnyde.me
- Created: 8/15/13
- Revised: 1/1/15

Usage
---
```
cpanel = Cpanel("whm.example.com", "root", "strongpassword", "some_cpanel_user")
print cpanel.listftp()
```
