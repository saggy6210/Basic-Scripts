import subprocess
import re
import datetime
import sys,os
import json

__author__ = "Sagar Chavan"
__email__ = ""

#Variable Declaration 
containerName = 'azauditlogcontainer'
backupContainerName = 'azauditlogcontainerbackup'
storageAccountName = 'activitystorage'
backupStorageAccountName= 'activitystoragebackup'
storageAccountKey = ''
backupStorageAccountKey= ''
ClientID= ''
ClientSecret= ''
tenantID= ''
end_time=datetime.datetime.isoformat(datetime.datetime.now())[:-7]+'Z'
retaintionPeriod = 1095
proc = subprocess.Popen(["az", "login", "--service-principal", "-u", ClientID, "-p", ClientSecret, "--tenant", tenantID], stdout=subprocess.PIPE, shell=True)
(out, err) = proc.communicate()

#os.system('az login --service-principal -u '+ClientID+' -p '+ClientSecret+' --tenant '+tenantID)	
#os.system('az account list > accountList.txt')
#file=open('accountList.txt')
#text=file.read()
#subscriptionList=re.findall(r'id": "([\w\d-]*)',text) ##list of subscription id's
subscriptionList=re.findall(r'id": "([\w\d-]*)', str(out))
for subscription in subscriptionList:
	subscription_id=subscription
	print ("===============================================================================================================")
	print ("SUBSCRIPTION ID: "+subscription_id)
	print ("===============================================================================================================")
	proc = subprocess.Popen(["az", "account", "set", "--subscription", subscription_id], stdout=subprocess.PIPE, shell=True)
	(out, err) = proc.communicate()	
	resourceGroupList=re.findall(r'resourceGroups\/([\d\S-]*)\"',str(out))
	proc = subprocess.Popen(["az", "group", "list"], stdout=subprocess.PIPE, shell=True)
	(out, err) = proc.communicate()

	resourceGroupList=re.findall(r'resourceGroups\/([\d\S-]*)\"',str(out)) ##List of resource group 
	#end_time=datetime.datetime.isoformat(datetime.datetime.now())[:-7]+'Z'	
	start_time=datetime.datetime.isoformat(datetime.datetime.now()-datetime.timedelta(1))[:-7]+'Z'

	for resourceGroup in resourceGroupList:
		print ("===============================================================================================================")
		print ("GENERATING & UPLOADING LOGS OF RESOURCE GRUOP: "+resourceGroup)
		print ("===============================================================================================================")
		proc = subprocess.Popen(["az", "monitor", "activity-log", "list","--start-time", start_time, "--end-time", end_time, "--resource-group", resourceGroup, "--output", "json"], stdout=subprocess.PIPE, shell=True) #We can provide date 3 months before from now.
		(out, err) = proc.communicate()
		print(json.loads(out))
		jsondata= json.loads(out)
		with open(resourceGroup+'-'+subscription_id+'-'+str(datetime.datetime.now().day)+str(datetime.datetime.now().month)+str(datetime.datetime.now().year)+'.json','w') as outfile:
		    json.dump(jsondata, outfile)
		
		#print(str(err))
		#file=open(resourceGroup+'-'+subscription_id+'-'+str(datetime.datetime.now().day)+str(datetime.datetime.now().month)+str(datetime.datetime.now().year)+'.json','w')
		#file.write(json.loads(str(out))))
		#file.close()
		dirStr = subscription_id+ '\\' +resourceGroup+ '\\' +outfile.name
		print("")
		print('az storage blob upload --container-name '+containerName+' --file '+outfile.name+' --name '+dirStr+' --account-name '+storageAccountName+' --account-key '+storageAccountKey)
		print("")
		print("Uploading " +outfile.name+ "...")
		
		proc = subprocess.Popen(["az", "storage", "blob", "upload", "--container-name", containerName, "--file", outfile.name, "--name", dirStr, "--account-name", storageAccountName, "--account-key", storageAccountKey], stdout=subprocess.PIPE, shell=True)
		(out, err) = proc.communicate()
#		os.system('az storage blob upload --container-name '+containerName+' --file '+file.name+' --name '+str(resourceGroup+'-'+subscription_id)+'\\'+file.name+' --account-name '+storageAccountName+' --account-key '+storageAccountKey)
		print(" ")
		print('az storage blob upload --container-name '+backupContainerName+' --file '+outfile.name+' --name '+dirStr+' --account-name '+backupStorageAccountName+' --account-key '+backupStorageAccountKey)
		print("")
		print("Uploading " +outfile.name+ "...")
		print("")
		proc = subprocess.Popen(["az", "storage", "blob", "upload", "--container-name", backupContainerName, "--file", outfile.name, "--name", dirStr, "--account-name", backupStorageAccountName, "--account-key", backupStorageAccountKey], stdout=subprocess.PIPE, shell=True) 
		(out, err) = proc.communicate()
#		os.system('az storage blob upload --container-name '+backupContainerName+' --file '+file.name+' --name '+str(resourceGroup+'-'+subscription_id)+'\\'+file.name+' --account-name '+backupStorageAccountName+' --account-key '+backupStorageAccountKey) 
		os.remove(outfile.name)
#		print (file.name+" has been successfully uploaded and removed from local")	
Cleanup with specified retention period   
#os.system('az storage blob list --container-name ' + containerName + ' --account-name ' + storageAccountName + ' --account-key ' + storageAccountKey +' >> blobList.json')
#os.system('az storage blob list --container-name ' + containerName + ' --account-name ' + storageAccountName + ' --account-key ' + storageAccountKey +' >> blobList.json')
#os.system('az storage blob list --container-name ' + backupContainerName + ' --account-name ' + backupStorageAccountName + ' --account-key ' + backupStorageAccountKey +' >> blobList.json')

#with open('blobList.json') as json_data:
#	d = json.load(json_data)
#	count = 1
#	for item in d:
#		count += 1
#		blobName = item['name']
#		lastModifiedDate = item['properties']['lastModified']
#		lDate=re.sub(r'\+.*$', "Z", lastModifiedDate)
#		todaysDate = datetime.datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%SZ")
#		retainDate = datetime.datetime.strptime(lDate, "%Y-%m-%dT%H:%M:%SZ")
#		noOfDays = todaysDate - retainDate
#		noDays = re.search(r'\d+', str(noOfDays)).group()
#		if int(noDays) > retaintionPeriod:
#			os.system('az storage blob delete --container-name '+ containerName + ' --name ' + blobName + ' --account-name ' + storageAccountName + ' --account-key ' +storageAccountName)
#			print ("STORAGE:" + storageAccountName + " LOG:" + blobName + 	" deleted successfully")
#			os.system('az storage blob delete --container-name '+ backupContainerName + ' --name ' + blobName + ' --account-name ' + backupStorageAccountName + ' --account-key ' +backupStorageAccountKey)
#			print ("STORAGE:" + storageAccountName + "LOG:" + blobName + 	" deleted successfully")
