import subprocess
import re
import os
subscription_id=''
print ("===============================================================================================================")	
print (" SUBSCRIPTION ID: "+subscription_id)
print ("===============================================================================================================")
proc = subprocess.Popen(["az", "account", "set", "--subscription", subscription_id], stdout=subprocess.PIPE, shell=True)
(out, err) = proc.communicate()
	
resourceGroupList=re.findall(r'resourceGroups\/([\d\S-]*)\"',str(out))
proc = subprocess.Popen(["az", "group", "list"], stdout=subprocess.PIPE, shell=True)
(out, err) = proc.communicate()
resourceGroupList=re.findall(r'resourceGroups\/([\d\S-]*)\"',str(out)) ##List of resource group
count = 0
for resource in resourceGroupList:
	if resource not in ['rg1', 'rg2', 'rg3']:
		count += 1
		print ("Deleting " +resource)
		os.system('az group delete -n '+ resource +' -y')
		print (resource+ " deleted successfully")
print (count)
