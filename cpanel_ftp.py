"""

Python Library for WHM/Cpanel's API2 FTP Module

        https://documentation.cpanel.net/display/SDK/Guide+to+cPanel+API+2

Author: Benton Snyder
Website: http://bensnyde.me
Created: 8/15/13
Revised: 2/10/16

"""
import logging
import base64
import httplib
import urllib
import json

class CpanelFTP:
    def __init__(self, whm_base_url, whm_username, whm_password, cpanel_username):
        """Constructor

            Cpanel FTP library public constructor.

        Parameters
            whm_base_url: str whm base url (ex. whm.example.com)
            whm_username: str whm root username
            whm_password: str whm password
            cpanel_username: str cpanel account to run scripts as
        """
        self.whm_base_url = whm_base_url
        self.whm_username = whm_username
        self.whm_password = whm_password
        self.cpanel_account = cpanel_username

    def _whm_api_query(self, script, kwargs):
        """Query Cpanel

            Queries specified WHM server's JSON API with specified query string.

        Parameters
            script: str cpanel api method name
            kwargs: key,val pairs to append to api call
        Returns
            JSON decoded response from server
        """
        headers = {
            'Authorization': 'Basic ' + base64.b64encode(self.whm_username+':'+self.whm_password).decode('ascii')
        }

        data = {
            'cpanel_xmlapi_version': 2,
            'cpanel_jsonapi_module': 'Ftp',
            'cpanel_jsonapi_user': self.cpanel_account,
            'cpanel_jsonapi_func': script
        }

        data.update(kwargs)
        params = '/json-api/cpanel?%s' % urllib.urlencode(data)

        try:
            conn = httplib.HTTPSConnection(self.whm_base_url, 2087)
            conn.request('GET', params, headers=headers)
            response = conn.getresponse()
            data = json.loads(response.read())
            conn.close()

            return data
        except httplib.HTTPException as ex:
            logging.critical("HTTPException from CpanelFTP API: %s" % ex)
        except ValueError as ex:
            logging.critical("ValueError decoding CpanelFTP API response string: %s" % ex)
        except Exception as ex:
            logging.critical("Unhandled Exception while querying CpanelFTP API: %s" % ex)


    def listftp(self, include_account_types="", skip_account_types=""):
        """List FTP Accounts

            Lists FTP accounts associated with the authenticated user's account.

                https://documentation.cpanel.net/display/SDK/cPanel+API+2+-+Ftp#cPanelAPI2-Ftp-Ftp::listftp

        Parameters
            include_account_types: str ftp account types you wish to view
            skip_account_types: str exclude ftp account types from the list
        Returns
            apiversion: int api version
            func: str api function name
            module: str api module name
            event:
                result: bool result status
            data:
                accounts:
                    user: str account username
                    type: str account type
                    homedir: str account's home directory
        """
        return self._whm_api_query('listftp', {
                'include_account_types': include_account_types,
                'skip_account_types': skip_account_types,
            }
        )


    def listftpsessions(self):
        """List active FTP Sessions

            Retrieves a list of active FTP sessions associated with the authenticated account.

                https://documentation.cpanel.net/display/SDK/cPanel+API+2+Functions+-+Ftp%3A%3Alistftpsessions

        Parameters
            None
        Returns
            apiversion: int api version
            func: str api function name
            module: str api module name
            event:
                result: bool result status
            data:
                sessions:
                    pid: str process id of ftp session
                    status: str status of transfer
                    user: str username associated with session
                    file: str filename in transfer
                    cmdline: str ps of ftp process
                    login: str login time
                    host: str hostname connected to session
        """
        return self._whm_api_query('listftpsessions')


    def listftpwithdisk(self, dirhtml="", include_account_types=None, skip_acct_types=None):
        """List FTP Accounts

            Generates a list of FTP accounts, including disk information, associated with a cPanel account.

                https://documentation.cpanel.net/display/SDK/cPanel+API+2+Functions+-+Ftp%3A%3Alistftpwithdisk

        Parameters
            dirhtml: str allows you to prepend the 'dir' return variable with a URL
            include_acct_types: str allows you to specify the type of ftp account you wish to view
            skip_acct_types: str allows you to exclude certain ftp account types from the list
        Returns
            apiversion: int api version
            func: str api function name
            module: str api module name
            event:
                result: bool result status
            data:
                accounts:
                    diskquota: str disk quota in Mb
                    diskusedpercent: int percentage of quota used
                    diskused: int space used in Mb
                    humandiskquota: str disk quota in Mb
                    reldir: str relative path
                    accttype: str account type
                    _diskused: int disk used in bytes
                    login: str username
                    dir: str absoulte path
                    deletable: bool is account deletable
                    serverlogin: str username@domain
                    humandiskused: int disk used in Mb
                    diskusedpercent20: int percentage of quota used
                    _diskquota: int disk quota in bytes
        """
        data = {'dirhtml': dirhtml}

        if include_account_types:
            data.push({'include_account_types': include_account_types})
        if skip_acct_types:
            data.push({'skip-acct_types': skip_acct_types})

        return self._whm_api_query('listftpwithdisk', data)


    def passwd(self, username, password):
        """Change FTP Account password

            Updates FTP account's password.

                https://documentation.cpanel.net/display/SDK/cPanel+API+2+Functions+-+Ftp%3A%3Apasswd

        Parameters
            username: str ftp account name
            password: str new password for the FTP account
        Returns
            apiversion: int api version
            func: str api function name
            module: str api module name
            event:
                result: bool result status
            data:
                reason: str result message
                result: bool result status
        """
        return self._whm_api_query('passwd', {
            'user': username,
            'pass': password
        })


    def addftp(self, user, password, quota, homedir):
        """Create FTP Account

            Adds a new FTP account.

                https://documentation.cpanel.net/display/SDK/cPanel+API+2+Functions+-+Ftp%3A%3Aaddftp

        Parameters
            user: str ftp account name
            password: str password
            quota: int quota in mb (0 for unlimited)
            homedir: str ftp account homedir path relative to the account's home directory
        Returns
            apiversion: int api version
            func: str api function name
            module: str api module name
            event:
                result: bool result status
            data:
                reason: str result message
                result: bool result status
        """
        return self._whm_api_query('addftp', {
            'user': user,
            'pass': password,
            'quota': quota,
            'homedir': homedir
        })


    def setquota(self, user, quota):
        """Set FTP Account quota

            Updates FTP account quota.

                https://documentation.cpanel.net/display/SDK/cPanel+API+2+Functions+-+Ftp%3A%3Asetquota

        Parameters
            user: str ftp account name
            quota: int new quota in mb (0 for unlimmited)
        Returns
            apiversion: int api version
            func: str api function name
            module: str api module name
            event:
                result: bool result status
            data:
                reason: str result message
                result: bool result status
        """
        return self._whm_api_query('setquota', {
            'user': user,
            'quota': quota
        })


    def delftp(self, user, destroy=False):
        """Delete FTP Account

            Deletes an FTP account.

                https://documentation.cpanel.net/display/SDK/cPanel+API+2+Functions+-+Ftp%3A%3Adelftp

        Parameters
            user: str ftp account name
            destroy: bool whether or not to destroy user's data
        Returns
            apiversion: int api version
            func: str api function name
            module: str api module name
            event:
                result: bool result status
            data:
                reason: str result message
                result: bool result status
        """
        return self._whm_api_query('delftp', **{
            'user': user,
            'destroy': destroy
        })
