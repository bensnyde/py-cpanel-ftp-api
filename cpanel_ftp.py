"""
=====================================================
 Cpanel API2 FTP Module Python Library
=====================================================
:Info: See <http://docs.cpanel.net/twiki/bin/view/ApiDocs/Api2/ApiFtp> for SolusVM XMLRPC API implementation.
:Author: Benton Snyder <goodger@python.org>
:Date: $Date: 2013-08-15 23:02:21 -0600 (Thurs, 15 Aug 2013) $
:Revision: $Revision: 0004 $
:Description: Python library for interfacing FTP functions with Cpanel <http://www.cpanel.net>
"""
from httplib import HTTPSConnection
from base64 import b64encode

class Cpanel:
        def __init__(self, url, username, password, scriptuser):
                """Cpanel FTP library public constructor.

                :param url: Base URL to WHM server
                :param username: API Username
                :param password: API Password
                :param scriptuser: WHM account to run scripts as
                """
                self.user = scriptuser
                self.url = url
                self.authHeader = {'Authorization':'Basic ' + b64encode(username+':'+password).decode('ascii')}

        def cQuery(self, script, **kwargs):
                """Queries specified WHM server's JSON API with specified query string.

                :param script: Cpanel script name
                :param user: Cpanel username underwhich to call from
                :param kwargs: Dictionary parameter pairs
                :returns: json formatted string
                """
                # Build Query String
                queryStr = '/json-api/cpanel?cpanel_jsonapi_user=%s&cpanel_jsonapi_module=Ftp&cpanel_jsonapi_func=%s&cpanel_xmlapi_version=2&' % (self.user, script)
                for key,val in kwargs.iteritems():
                        queryStr = queryStr + str(key) + '=' + str(val) + '&'

                # Make JSON API call
                conn = HTTPSConnection(self.url, 2087)
                conn.request('GET', queryStr, headers=self.authHeader)
                response = conn.getresponse()
                data = response.read()

                # Cleanup
                conn.close()
                return data


        def listftp(self, include_account_types="", skip_account_types=""):
                """List FTP accounts associated with the authenticated user's account.
                http://docs.cpanel.net/twiki/bin/view/ApiDocs/Api2/ApiFtp#Ftp::listftp

                :param include_account_types: which FTP account types you wish to view
                :param skip_account_types: exclude certain FTP account types from the list
                :returns: json formatted string
                """
                data = {
                        'include_account_types': include_account_types,
                        'skip_account_types': skip_account_types,
                }
                return self.cQuery('listftp', **data)

        def listftpsessions(self):
                """Retrieve a list of FTP sessions associated with the authenticated account.
                http://docs.cpanel.net/twiki/bin/view/ApiDocs/Api2/ApiFtp#Ftp::listftpsessions

                :returns: json formatted string
                """
                return self.cQuery('listftpsessions')

        def listftpwithdisk(self, dirhtml="", include_account_types=None, skip_acct_types=None):
                """Generate a list of FTP accounts, including disk information, associated with a cPanel account.
                http://docs.cpanel.net/twiki/bin/view/ApiDocs/Api2/ApiFtp#Ftp::listftpwithdisk

                :param dirhtml: allows you to prepend the 'dir' return variable with a URL
                :param include_acct_types: allows you to specify the type of FTP account you wish to view
                :param skip_acct_types: allows you to exclude certain FTP account types from the list
                :returns: json formatted string
                """
                data = {'dirhtml': dirhtml}
                if include_account_types:
                        data.push({'include_account_types': include_account_types})
                if skip_acct_types:
                        data.push({'skip-acct_types': skip_acct_types})
                return self.cQuery('listftpwithdisk', **data)

        def passwd(self, username, password):
                """Change an FTP account's password.
                http://docs.cpanel.net/twiki/bin/view/ApiDocs/Api2/ApiFtp#Ftp::passwd

                :param username: The name of the FTP account whose password should be changed
                :param password: The new password for the FTP account
                :returns: json formatted string
                """
                data = {
                        'user': username,
                        'pass': password
                }
                return self.cQuery('passwd', **data)

        def addftp(self, user, password, quota, homedir):
                """Add a new FTP account.
                http://docs.cpanel.net/twiki/bin/view/ApiDocs/Api2/ApiFtp#Ftp::addftp

                :param user: The username portion of the new FTP account, without the domain
                :param password: The password for the new FTP account
                :param quota: The new FTP account's quota
                :param homedir: The path to the FTP account's root directory. This value should be relative to the account's home directory
                :returns: json formatted string
                """
                data = {
                        'user': user,
                        'pass': password,
                        'quota': quota,
                        'homedir': homedir
                }
                return self.cQuery('addftp', **data)

        def setquota(self, user, quota):
                """Change an FTP account's quota.
                http://docs.cpanel.net/twiki/bin/view/ApiDocs/Api2/ApiFtp#Ftp::setquota

                :param user: The name of the FTP account whose quota should be changed
                :param quota: The new quota (in megabytes) for the FTP account
                :returns: json formatted string
                """
                data = {
                        'user': user,
                        'quota': quota
                }
                return self.cQuery('setquota', **data)

        def delftp(self, user, destroy=False):
                """Delete an FTP account.
                http://docs.cpanel.net/twiki/bin/view/ApiDocs/Api2/ApiFtp#Ftp::delftp

                :param user: The name of the FTP account to be removed
                :param destroy: whether or not the FTP account's home directory should also be deleted
                :returns: json formatted string
                """
                data = {
                        'user': user,
                        'destroy': destroy
                }
                return self.cQuery('delftp', **data)
