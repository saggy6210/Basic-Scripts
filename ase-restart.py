import sys
import yaml
import glob
import json
import requests

__author__  = ''
__version__ = '1.0.0'
__description__ = "This script is to suspend/resume the app service environment"

def suspend_ASE(rg,envs,cfg,headers):
    # Suspend The ASE
    print('Suspending This', envs['name'], 'Environment')
    suspend_uri = "https://management.azure.com/subscriptions/" + cfg['subscription_id'] + "/resourceGroups/" + rg['name'] + "/providers/Microsoft.Web/hostingEnvironments/" + envs['name'] + "/suspend?api-version=2017-08-01"
    get_status_suspend = requests.post(url=suspend_uri,headers=headers).status_code
    print(get_status_suspend)

def resume_ASE(rg,envs,cfg,headers):
    #Resume The ASE
	print('Starting This', envs['name'], 'Environment')
	resume_uri = "https://management.azure.com/subscriptions/" + cfg['subscription_id'] + "/resourceGroups/" + rg['name'] + "/providers/Microsoft.Web/hostingEnvironments/" + envs['name'] + "/resume?api-version=2017-08-01"
	get_status_resume = requests.post(url=resume_uri,headers=headers).status_code
	print(get_status_resume)

def getdata(status,file_name):
    print(file_name)
    with open(file_name, 'r') as ymlfile:
        cfg = yaml.load(ymlfile)

    ## Getting access token
    URI = "https://login.microsoftonline.com/" + cfg['tenant_id'] + "/oauth2/token?api-version=1.0"
    data = {
        'grant_type': 'client_credentials',
        'resource': 'https://management.core.windows.net/',
        'client_id': cfg['client_id'],
        'client_secret': cfg['client_secret']
    }
    accesstokendata = requests.post(URI, data=data).content
    accesstoken = (json.loads(accesstokendata).get('access_token'))
    headers = {'Authorization': 'Bearer ' + str(accesstoken)}

     # Get The ResourceGroups
    get_res_group_uri = "https://management.azure.com/subscriptions/" + cfg['subscription_id'] + "/resourcegroups?api-version=2017-05-10"
    list_res_group = requests.get(url=get_res_group_uri, headers=headers).content
    res_group_json = json.loads(list_res_group)

    for rg in res_group_json['value']:
        get_host_envs_uri = "https://management.azure.com/subscriptions/" + cfg['subscription_id'] + "/resourceGroups/" + rg['name'] + "/providers/Microsoft.Web/hostingEnvironments?api-version=2017-08-01"
        list_envs = requests.get(url=get_host_envs_uri, headers=headers).content
        host_envs_json = json.loads(list_envs)

        #print(host_envs_json)
        for envs in host_envs_json['value']:
            #print(envs['name'])
            tag = envs.get('tags')
            #print(tag['name'])
            if status.lower() == 'suspend':
                if tag is None:
                    suspend_ASE(rg,envs,cfg,headers)
                    print()
                else:
                    if 'suspend' not in tag:
                        suspend_ASE(rg,envs,cfg,headers)
                        print()
                    else:
                        if tag['suspend'] == 'true':
                             suspend_ASE(rg,envs,cfg,headers)
                             print()
                        else:
                            print('Do Not Suspend This', envs['name'], ' Environment')
                            print()
            if status.lower() == 'resume':
                resume_ASE(rg,envs,cfg,headers)
                print()

if __name__ == "__main__":
    for filename in glob.glob('*.yml'):
#       print(filename)
        try:
            if sys.argv[1] not in ['suspend','resume']:
                raise ValueError

            getdata(sys.argv[1],filename)
        except IndexError:
            print('Index Error : Fail To Provide Status Of The ASE !!!')
            print("Usage: forASE.py <suspend/resume>")
            print('Exiting......')
            sys.exit(1)     # exiting the program
        except ValueError:
            print('Value Error : Supplied Argument Is Wrong !!!')
            print("Usage: forASE.py <suspend/resume>")
            print('Exiting......')
            sys.exit(1)     # exiting the program
