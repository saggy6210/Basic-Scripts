#!/bin/bash

function configureAz(){
    info "Configuring Az..."
    az login --service-principal -u ${client_id} -p ${client_secret} --tenant ${tenant_id} || die "az login failed"
    az account set --subscription $subscription_id
}

function storagefirewallsetup(){
 configureAz
 RESOURCEGROUP="mdsp-${account_name_prefix}-${Environment}"
 STORAGE_ACCOUNT_NAME="mdsp${account_name_prefix}${Environment}storageact"
 VNET_NAME="${RESOURCEGROUP}-vnet"
 PRIVATE_SUBNET_NAME="${RESOURCEGROUP}-ase-private-subnet"
 
 az storage account network-rule add --resource-group ${RESOURCEGROUP} --account-name ${STORAGE_ACCOUNT_NAME} --vnet-name ${VNET_NAME} --subnet ${PRIVATE_SUBNET_NAME}
 if [ ! -z "${enable_pubsubnet_stfirewall}" ] 
 then
    PUBLIC_SUBNET_NAME="${RESOURCEGROUP}-public-subnet"
    az storage account network-rule add --resource-group ${RESOURCEGROUP} --account-name ${STORAGE_ACCOUNT_NAME} --vnet-name ${VNET_NAME} --subnet ${PUBLIC_SUBNET_NAME}
 fi
 if [ ! -z "${enable_mgmntsubnet_stfirewall}" ] 
 then
     MANAGEMENT_SUBNET_NAME="${RESOURCEGROUP}-management-subnet"
    az storage account network-rule add --resource-group ${RESOURCEGROUP} --account-name ${STORAGE_ACCOUNT_NAME} --vnet-name ${VNET_NAME} --subnet ${MANAGEMENT_SUBNET_NAME}
 fi
 az storage account update --name ${STORAGE_ACCOUNT_NAME} --resource-group ${RESOURCEGROUP} --default-action Deny
 az storage account update --name ${STORAGE_ACCOUNT_NAME} --resource-group ${RESOURCEGROUP} --bypass Logging Metrics AzureServices 

}
      
function run(){
  duty=$1
  pwd
  case $duty in   
  "stfirewall")
      storagefirewallsetup
  ;;
  
  *)
  ;;
  esac
}

run $1 
