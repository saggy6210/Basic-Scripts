#!/bin/sh

scope="/subscriptions/sub-id"

az account show

# mdsp-resource-location

az policy definition create -n mdsp-resource-region --display-name mdsp-resource-region --description "This policy enables you to restrict the locations your organization can specify when deploying resources. Use to enforce your geo-compliance requirements." --mode All --rules '{ 
                                "if" : {
                        "not" : {
                            "field" : "location",
                                "in" : ["West Europe"]
                            }
                          },
                            "then" : {
                                "effect" : "audit"
                                }
                        }'

az policy assignment create --display-name mdsp-resource-region --policy mdsp-resource-region --scope $scope --sku standard

# mdsp-storageaccount-https

az policy definition create -n mdsp-storageaccount-https --display-name mdsp-storageaccount-https --description "Ensure https traffic only for storage account" --mode All --rules '{ 
                                "if":{  
                   "allOf":[  
                      {  
                         "field":"type",
                         "equals":"Microsoft.Storage/storageAccounts"
                      },
                      {  
                         "not":{  
                            "field":"Microsoft.Storage/storageAccounts/supportsHttpsTrafficOnly",
                            "equals":"true"
                         }
                      }
                   ]
                },
                            "then" : {
                                "effect" : "audit"
                                }
                        }'

az policy assignment create --display-name mdsp-storageaccount-https --policy mdsp-storageaccount-https --scope $scope --sku standard

# mdsp-storageacount-sku

az policy definition create -n mdsp-storageacount-sku --display-name mdsp-storageacount-sku --description "This policy enables you to specify a set of storage account SKUs that your organization can deploy" --mode All --rules '{   "if":{  
                   "allOf":[  
                      {  
                         "field":"type",
                         "equals":"Microsoft.Storage/storageAccounts"
                      },
                      {  
                         "not":{  
                            "field":"Microsoft.Storage/storageAccounts/sku.name",
                            "equals":"Standard_LRS"
                         }
                      }
                   ]
                },
                            "then" : {
                                "effect" : "audit"
                                }
                        }'
						
az policy assignment create --display-name mdsp-storageacount-sku --policy mdsp-storageacount-sku --scope $scope --sku standard

# mdsp-db-encryption

az policy definition create -n mdsp-db-encryption --display-name mdsp-db-encryption --description "Audit transparent data encryption status for SQL databases" --mode All --rules '{  "if":{  
                   "field":"type",
                   "equals":"Microsoft.SQL/servers/databases"
                },
                "then":{  
                   "effect":"auditIfNotExists",
                   "details":{  
                      "type":"Microsoft.SQL/servers/databases/transparentDataEncryption",
                      "name":"current",
                      "existenceCondition":{  
                         "field":"Microsoft.Sql/transparentDataEncryption.status",
                         "equals":"enabled"
                      }
                   }
                   }
                }'
				
az policy assignment create --display-name mdsp-db-encryption --policy mdsp-db-encryption --scope $scope --sku standard
