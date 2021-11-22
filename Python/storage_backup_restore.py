#!/usr/bin/python3
"""
call this script with following parameter
-ssan : source storage account name
-dsak : destination storage account key
-ssak : source storage account key
-cl : coma seperated list of container eg. "container1,container2,...."
backup_storage_account.py backup/restore ssan ssak dsan dsak cl rp
"""

from os import system
import sys
import os
import time
import azure.storage.blob.baseblobservice
from datetime import datetime, timedelta
from backup_status_monitor import sendelastic

__version__ = '1.0.0'
__description__ = "storage backup script"

def backup(source_storage_name, source_storage_data_keys, destination_Storage_AccountName, destination_storage_data_keys, container_list):
    if container_list:
        container_list=container_list.split(",")
    else:    
        container_list=[]
    timestamptemp = datetime.now()
    timestamp = timestamptemp.strftime('%Y%m%d%H%M')

    blob_service_destination = azure.storage.blob.baseblobservice.BaseBlobService(account_name=destination_Storage_AccountName, account_key=destination_storage_data_keys)
    
    blob_service_source = azure.storage.blob.baseblobservice.BaseBlobService(account_name=source_storage_name, account_key=source_storage_data_keys)

    sourceContainerList = []
    sourceContainerListGenerator = blob_service_source.list_containers()
    for sourceContainer in sourceContainerListGenerator:
        sourceContainerList.append(sourceContainer.name)
        if "tfstate" in sourceContainer.name:
            container_list.append(sourceContainer.name)
    status_flag = 1
    for container in container_list:
        if (container not in sourceContainerList):
            print("please provide correct Container list, given "+ container + " conatainer is not valid")
            status_flag = 0
        else:
            destcontainer=container
            if len(destcontainer) > 50:
                destcontainer = container[:50]
            blob_service_destination.create_container(destcontainer + timestamp)
            azcopycommand = "AzCopy /Source:https://" + source_storage_name + ".blob.core.windows.net/" + container + " /Dest:https://" + destination_Storage_AccountName + ".blob.core.windows.net/" + destcontainer + timestamp + "/ /SourceKey:" + source_storage_data_keys + " /DestKey:" + destination_storage_data_keys + " /S /SyncCopy /Z:./"+container+" "
            backup_status=system(azcopycommand)
            if not backup_status:
                print("Copied container :- " + container + " from " + source_storage_name + "/" + container + " to " + destination_Storage_AccountName + "/" + container + timestamp)
            else:
                status_flag = 0
    #send data to elastic search           
    sendelastic(status_flag)            

def restore(source_storage_name, source_storage_data_keys, destination_Storage_AccountName, destination_storage_data_keys, container_list):
    container_list=container_list.split(",")
    blob_service_destination = azure.storage.blob.baseblobservice.BaseBlobService(account_name=destination_Storage_AccountName, account_key=destination_storage_data_keys)
    blob_service_source = azure.storage.blob.baseblobservice.BaseBlobService(account_name=source_storage_name, account_key=source_storage_data_keys)
    sourceContainerList = []
    sourceContainerListGenerator = blob_service_source.list_containers()
    for sourceContainer in sourceContainerListGenerator:
        sourceContainerList.append(sourceContainer.name)
    print(container_list)
    status_flag = 1
    for container in container_list:
        if (container not in sourceContainerList):
            print("please provide correct Container list, given "+ container + " conatainer is not valid")
        else:
            blob_service_destination.create_container( container[:-12])
            azcopycommand = "AzCopy /Source:https://" + source_storage_name + ".blob.core.windows.net/" + container + " /Dest:https://" + destination_Storage_AccountName + ".blob.core.windows.net/" + container[:-12] + "/ /SourceKey:" + source_storage_data_keys + " /DestKey:" + destination_storage_data_keys + " /S /SyncCopy /Z:./"+container+" "
            backup_status=system(azcopycommand)
            if not backup_status:
                print("Copied container :- " + container + " from " + source_storage_name + "/" + container + " to " + destination_Storage_AccountName + "/" + container[:-12])
            else:
                status_flag = 0
    #send data to elastic search           
    sendelastic(status_flag)

def cleanup(destination_Storage_AccountName, destination_storage_data_keys, retaintion_period):
    blob_service_destination = azure.storage.blob.baseblobservice.BaseBlobService(account_name=destination_Storage_AccountName, account_key=destination_storage_data_keys)
    destinationContainerListGenerator = blob_service_destination.list_containers()
    
    timestamptemp = datetime.now()
    timestamptemp=timestamptemp - timedelta(days=int(retaintion_period))
    timestamp = timestamptemp.strftime('%Y%m%d%H%M')
    for destinationContainer in destinationContainerListGenerator:
        try:
            dest_timestamp=destinationContainer.name[-12:] 
            if(int(dest_timestamp) < int(timestamp)):
                blob_service_destination.delete_container(destinationContainer.name)
                print("container : "+ destinationContainer.name + "has been deleted")
        except ValueError:
            continue
            
def getdata():

    args = sys.argv[1:]
    try:
        ssan=args[1]
        ssak=args[2]
        dsan=args[3]
        dsak=args[4]
        cl=args[5]
        rp=args[6]
        if args[0] == "backup":
            print("******* backup started *********")
            backup(ssan,ssak,dsan,dsak,cl)
            print("******* backup cleaneup started *********")
            cleanup(dsan,dsak,rp)
        if args[0] == "restore":
            print("******* backup cleaneup started *********")
            restore(ssan,ssak,dsan,dsak,cl)
    except IndexError as identifier:
        print("indexerror please provide correct sequence of input")
    
getdata()
