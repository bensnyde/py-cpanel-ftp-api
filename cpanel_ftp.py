"""
=====================================================
 Cpanel API2 FTP Module Python Library
=====================================================
:Info: See http://docs.cpanel.net/twiki/bin/view/ApiDocs/Api2/ApiFtp for API implementation.
:Author: Benton Snyder introspectr3@gmail.com
:Website: Noumenal Designs <http://www.noumenaldesigns.com>
:Description: Python library for interfacing FTP functions with Cpanel http://www.cpanel.net
"""
import logging
import base64 
import httplib
import json
import socket

WHMURL = "whm.example.com"
WHMROOT = "root"
WHMPASS = "mystrongpassword"
apilogger = "api_logger"

class Cpanel:
    def __init__(self, username):
        """Constructor

            Cpanel FTP library public constructor.

        Parameters
            username: str cpanel account to run scripts as
        """
        self.user = username

    def cQuery(self, script, **kwargs):
        """Query Cpanel 

            Queries specified WHM server's JSON API with specified query string.

        Parameters
            script: str cpanel api method name
            kwargs: key,val pairs to append to api call
        Returns
            JSON decoded response from server
        """
        # Build Query String
        queryStr = '/json-api/cpanel?cpanel_xmlapi_version=2&cpanel_jsonapi_module=Ftp&cpanel_jsonapi_user=%s&cpanel_jsonapi_func=%s' % (self.username, script)
        for key,val in kwargs.iteritems():
            queryStr = "%s&%s=%s" % (queryStr, key, val)

        # Make API call
        try:       
            conn = httplib.HTTPSConnection(WHMURL, 2087)
            conn.request('GET', queryStr, headers={'Authorization':'Basic ' + base64.b64encode(WHMROOT+':'+WHMPASS).decode('ascii')})
            response = conn.getresponse()
            data = json.loads(response.read())
            conn.close()

            return data
        # Log any errors
        except httplib.HTTPException as ex:
            logging.getLogger(apilogger).critical("HTTPException from CpanelFTP API: %s" % ex)
        except socket.error as ex:
            logging.getLogger(apilogger).critical("Socket.error connecting to CpanelFTP API: %s" % ex)
        except ValueError as ex:
            logging.getLogger(apilogger).critical("ValueError decoding CpanelFTP API response string: %s" % ex)
        except Exception as ex:
            logging.getLogger(apilogger).critical("Unhandled Exception while querying CpanelFTP API: %s" % ex)


    def listftp(self, include_account_types="", skip_account_types=""):
        """Get FTP Accounts

            Lists FTP accounts associated with the authenticated user's account.
            http://docs.cpanel.net/twiki/bin/view/ApiDocs/Api2/ApiFtp#Ftp::listftp
        
        Parameters
            include_account_types: str ftp account types you wish to view
            skip_account_types: str exclude ftp account types from the list
        Returns
            JSON
                success: int success of api call
                message: str summary of api call 
                *data:
                    accounts: cpanel array 
        """
        result = self.cQuery('listftp', **{
                'include_account_types': include_account_types,
                'skip_account_types': skip_account_types,
            }
        )

        try:
            if result["cpanelresult"]["event"]["result"] == 1:
                return {
                    'success': 1,
                    'message': 'FTP accounts successfully retrieved.',
                    'data': {
                        'accounts': result["cpanelresult"]["data"]
                    }
                }
            logging.getLogger(apilogger).error("Remote server returned error: %s" % result["cpanelresult"]["error"])
        except IndexError as ex:
            logging.getLogger(apilogger).critical("Unexpected response from remote server: %s" % ex)
        except TypeError as ex:
            pass

        return {
            'success': 0,
            'message': 'There was a problem retrieving the FTP accounts listing.'
        }

    def listftpsessions(self):
        """Get FTP Sessions

            Retrieves a list of active FTP sessions associated with the authenticated account.
            http://docs.cpanel.net/twiki/bin/view/ApiDocs/Api2/ApiFtp#Ftp::listftpsessions

        Parameters
            None
        Returns
            JSON
                success: int success of api call
                message: str summary of api call  
                *data:
                    sessions: cpanel array                 
        """
        result = self.cQuery('listftpsessions')

        try:
            if result["cpanelresult"]["event"]["result"] == 1:
                return {
                    'success': 1,
                    'message': 'FTP sessions successfully retrieved.',
                    'data': {
                        'sessions': result["cpanelresult"]["data"]
                    }
                }
            logging.getLogger(apilogger).error("Remote server returned error: %s" % result["cpanelresult"]["error"])
        except IndexError as ex:
            logging.getLogger(apilogger).critical("Unexpected response from remote server: %s" % ex)
        except TypeError as ex:
            pass            

        return {
            'success': 0,
            'message': 'There was a problem retrieving the FTP sessions listing.'
        }        

    def listftpwithdisk(self, dirhtml="", include_account_types=None, skip_acct_types=None):
        """Get FTP Accounts

            Generates a list of FTP accounts, including disk information, associated with a cPanel account.
            http://docs.cpanel.net/twiki/bin/view/ApiDocs/Api2/ApiFtp#Ftp::listftpwithdisk 

        Parameters
            dirhtml: str allows you to prepend the 'dir' return variable with a URL
            include_acct_types: str allows you to specify the type of ftp account you wish to view
            skip_acct_types: str allows you to exclude certain ftp account types from the list
        Returns
            JSON
                success: int success of api call
                message: str summary of api call 
                *data:
                    accounts: cpanel array                      
        """
        data = {'dirhtml': dirhtml}

        if include_account_types:
            data.push({'include_account_types': include_account_types})
        if skip_acct_types:
            data.push({'skip-acct_types': skip_acct_types})

        result = self.cQuery('listftpwithdisk', **data)

        try:
            if result["cpanelresult"]["event"]["result"] == 1:
                return {
                    'success': 1,
                    'message': 'FTP accounts successfully retrieved.',
                    'data': {
                        'accounts': result["cpanelresult"]["data"]
                    }
                }
            logging.getLogger(apilogger).error("Remote server returned error: %s" % result["cpanelresult"]["error"])
        except IndexError as ex:
            logging.getLogger(apilogger).critical("Unexpected response from remote server: %s" % ex)
        except TypeError as ex:
            pass            

        return {
            'success': 0,
            'message': 'There was a problem retrieving the FTP accounts listing.'
        } 

    def passwd(self, username, password):
        """Change FTP Account password

            Updates FTP account's password.
            http://docs.cpanel.net/twiki/bin/view/ApiDocs/Api2/ApiFtp#Ftp::passwd
        
        Parameters
            username: str ftp account name
            password: str new password for the FTP account
        Returns
            JSON
                success: int success of api call
                message: str summary of api call          
        """
        result = self.cQuery('passwd', **{
            'user': username,
            'pass': password
        })

        try:
            if result["cpanelresult"]["data"][0]["result"] == 1:
                return {
                    'success': 1,
                    'message': 'FTP account password successfully changed.'
                }
            logging.getLogger(apilogger).error("Remote server returned error: %s" % result["cpanelresult"]["error"])
        except IndexError as ex:
            logging.getLogger(apilogger).critical("Unexpected response from remote server: %s" % ex)
        except TypeError as ex:
            pass            

        return {
            'success': 0,
            'message': 'There was a problem changing the FTP account password.'
        }                

    def addftp(self, user, password, quota, homedir):
        """Create FTP Account

            Adds a new FTP account.
            http://docs.cpanel.net/twiki/bin/view/ApiDocs/Api2/ApiFtp#Ftp::addftp
        
        Parameters
            user: str ftp account name
            password: str password
            quota: int quota in mb (0 for unlimited)
            homedir: str ftp account homedir path relative to the account's home directory
        Returns
            JSON
                success: int success of api call
                message: str summary of api call              
        """
        result = self.cQuery('addftp', **{
            'user': user,
            'pass': password,
            'quota': quota,
            'homedir': homedir
        })

        try:
            if result["cpanelresult"]["data"][0]["result"] == 1:
                return {
                    'success': 1,
                    'message': 'FTP account successfully created.'
                }
            logging.getLogger(apilogger).error("Remote server returned error: %s" % result["cpanelresult"]["error"])
        except IndexError as ex:
            logging.getLogger(apilogger).critical("Unexpected response from remote server: %s" % ex)
        except TypeError as ex:
            pass            

        return {
            'success': 0,
            'message': 'There was a problem creating the FTP account.'
        }           

    def setquota(self, user, quota):
        """Set FTP Account quota

            Updates FTP account quota.
            http://docs.cpanel.net/twiki/bin/view/ApiDocs/Api2/ApiFtp#Ftp::setquota
        
        Parameters
            user: str ftp account name
            quota: int new quota in mb (0 for unlimmited)
        Returns
            JSON
                success: int success of api call
                message: str summary of api call                     
        """
        result = self.cQuery('setquota', **{
            'user': user,
            'quota': quota
        })

        try:
            if result["cpanelresult"]["data"][0]["result"] == 1:
                return {
                    'success': 1,
                    'message': 'FTP account quota successfully updated.'
                }
            logging.getLogger(apilogger).error("Remote server returned error: %s" % result["cpanelresult"]["error"])
        except IndexError:
            logging.getLogger(apilogger).critical("Unexpected response from remote server: %s" % ex)
        except TypeError as ex:
            pass            

        return {
            'success': 0,
            'message': 'There was a problem updating the FTP account quota.'
        }           

    def delftp(self, user, destroy=False):
        """Delete FTP Account

            Deletes an FTP account.
            http://docs.cpanel.net/twiki/bin/view/ApiDocs/Api2/ApiFtp#Ftp::delftp
        
        Parameters
            user: str ftp account name
            destroy: bool whether or not to destroy user's data
        Returns
            JSON
                success: int success of api call
                message: str summary of api call     
        """
        result = self.cQuery('delftp', **{
            'user': user,
            'destroy': destroy
        })

        try:
            if result["cpanelresult"]["data"][0]["result"] == 1:
                return {
                    'success': 1,
                    'message': 'FTP account deleted successfully.'
                }
            logging.getLogger(apilogger).error("Remote server returned error: %s" % result["cpanelresult"]["error"])
        except IndexError as ex:
            logging.getLogger(apilogger).critical("Unexpected response from remote server: %s" % ex)
        except TypeError as ex:
            pass            

        return {
            'success': 0,
            'message': 'There was a problem deleting the FTP account.'
        }   
