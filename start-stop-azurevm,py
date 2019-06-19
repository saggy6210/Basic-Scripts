import sys
import yaml
import json
import glob
import requests

__version__ = '1.0.0'
__description__ = "This script is to start/stop the virtual machine"

def stop_VM(rg,vm,cfg,headers):
    print('Shutting Down This ', vm['name'], 'VM')
    get_status_stop_uri = "https://management.azure.com/subscriptions/" + cfg['subscription_id'] + "/resourceGroups/" + rg['name'] + "/providers/Microsoft.Compute/virtualMachines/" + vm['name'] + "/powerOff?api-version=2017-12-01"
    get_status_stop = requests.post(url=get_status_stop_uri, headers=headers).status_code
    print(get_status_stop)

def start_VM(rg,vm,cfg,headers):
    print('Starting This ', vm['name'], 'VM')
    get_status_start_uri = "https://management.azure.com/subscriptions/" + cfg['subscription_id'] + "/resourceGroups/" + rg['name'] + "/providers/Microsoft.Compute/virtualMachines/" + vm['name'] + "/start?api-version=2017-12-01"
    get_status_start = requests.post(url=get_status_start_uri, headers=headers).status_code
    print(get_status_start)

def getdata(state,file_name):
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

    get_res_group_uri = "https://management.azure.com/subscriptions/" + cfg['subscription_id'] + "/resourcegroups?api-version=2017-05-10"
    list_res_group = requests.get(url=get_res_group_uri, headers=headers).content
    res_group_json = json.loads(list_res_group)

    for rg in res_group_json['value']:
         get_vm_uri = "https://management.azure.com/subscriptions/" + cfg['subscription_id'] + "/resourceGroups/" + rg['name'] + "/providers/Microsoft.Compute/virtualmachines?api-version=2017-12-01"
         list_vm = requests.get(url=get_vm_uri, headers=headers).content
         vm_json = json.loads(list_vm)

         #print(vm_json)
         for vm in vm_json['value']:
            # print(vm['name'])
            tag = vm.get('tags')
            #print(tag)
            if state.lower() == 'stop':
                if tag is None:     # if tags object contains no key value pair
                    stop_VM(rg,vm,cfg,headers)
                    print()
                else:
                    if 'shutdown' not in tag:       # if tag does not contain shutdown key
                        stop_VM(rg,vm,cfg,headers)
                        print()
                    else:
                        if tag['shutdown'] == 'true':       # if shutdown key value is true
                             stop_VM(rg,vm,cfg,headers)
                             print()
                        else:
                            print('Do Not ShutDown This', vm['name'], 'VM')
                            print()
            if state.lower() == 'start':
                start_VM(rg,vm,cfg,headers)
                print()

if __name__ == "__main__":
    for filename in glob.glob('*.yml'):
#       print(filename)
        try:
            if sys.argv[1] not in ['start','stop']:
                raise ValueError

            getdata(sys.argv[1],filename)
        except IndexError:
            print('Index Error : Fail To Provide State Of The VM !!!')
            print("Usage: forVM.py <start/stop>")
            print('Exiting......')
            sys.exit(1)     # exiting the program
        except ValueError:
            print('Value Error : Supplied Argument Is Wrong !!!')
            print("Usage: forVM.py <start/stop>")
            print('Exiting......')
            sys.exit(1)     # exiting the program
