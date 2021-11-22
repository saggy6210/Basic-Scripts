import requests 
import json
import sys
import time
import click
import os

__author__  = ''
__version__ = '1.0.0'
__emailid__ = ''
__description__ = "this is script to delete the all resources created by ARM trough Terraform"

@click.command()
@click.option('-tid',default='', help='tenantId of subscription')
@click.option('-sub',default='',  help='subscriptionsid of subscription')
@click.option('-cid', default='', help='clientId of subscription')
@click.option('-cs',default='', help='clientSecret of subscription')
@click.option('-wid', default= '', help = 'Workspace ID ')
@click.option('-rg', default= '', help = 'Resource group name')
@click.option('-dsn', default= 'DSenable', help = 'Dignostics setting name')

def EnableDignostics(tid, sub, cid, cs, wid, rg, dsn):
    ## Getting access token
  Uri = "https://login.microsoftonline.com/"+ tid + "/oauth2/token?api-version=1.0"
  data = {
		'grant_type':'client_credentials',
		'resource':'https://management.core.windows.net/',
		'client_id':cid,
		'client_secret':cs
		}
  accesstokendata = requests.post(Uri, data=data ).content
  accesstoken =  (json.loads(accesstokendata).get('access_token'))
  headers = {'Authorization': 'Bearer '+ str(accesstoken)}

    ## Getting All plan list
  getAllResourcesApi = "https://management.azure.com/subscriptions/"+ sub +"/resourceGroups/"+ rg +"/resources?api-version=2017-05-10"
  RG_ResourceList  = requests.get(url = getAllResourcesApi, headers=headers).content

  Servicebus_Dignosticsjson =  {
    "properties": {
    "workspaceId": wid ,
    "metrics": [
      {
        "category": "AllMetrics",
        "enabled": True,
        "retentionPolicy": {
          "enabled": False,
          "days": 0
        }
      }
    ],
    "logs": [
      {
        "category": "OperationalLogs",
        "enabled": True,
        "retentionPolicy": {
          "enabled": False,
          "days": 0
        }
      }
    ]
  }
}
  ApplicationGateway_Dignosticsjson={
    "properties": {
    "workspaceId": wid ,
    "metrics": [
      {
        "category": "AllMetrics",
        "enabled": True,
        "retentionPolicy": {
          "enabled": False,
          "days": 0
        }
      }
    ],
    "logs": [
      {
        "category": "ApplicationGatewayAccessLog",
        "enabled": True,
        "retentionPolicy": {
          "enabled": False,
          "days": 0
        }
      },
      {
        "category": "ApplicationGatewayPerformanceLog",
        "enabled": True,
        "retentionPolicy": {
          "enabled": False,
          "days": 0
        }
      },
      {
        "category": "ApplicationGatewayFirewallLog",
        "enabled": True,
        "retentionPolicy": {
          "enabled": False,
          "days": 0
        }
      }
    ]
  }
}
  CosmosDB_Dignosticsjson ={
    "properties": {
    "workspaceId": wid ,
    "metrics": [
      {
        "category": "Requests",
        "enabled": True,
        "retentionPolicy": {
          "enabled": False,
          "days": 0
        }
      }
    ],
    "logs": [
      {
        "category": "MongoRequests",
        "enabled": True,
        "retentionPolicy": {
          "enabled": False,
          "days": 0
        }
      },
      {
        "category": "DataPlaneRequests",
        "enabled": True,
        "retentionPolicy": {
          "enabled": False,
          "days": 0
        }
      }
    ]
  }
}
  EventHubs_Dignosticsjson = {
    "properties": {
    "workspaceId": wid ,
    "metrics": [
      {
        "category": "AllMetrics",
        "enabled": True,
        "retentionPolicy": {
          "enabled": False,
          "days": 0
        }
      }
    ],
    "logs": [
      {
        "category": "ArchiveLogs",
        "enabled": True,
        "retentionPolicy": {
          "enabled": False,
          "days": 0
        }
      },
      {
        "category": "OperationalLogs",
        "enabled": True,
        "retentionPolicy": {
          "enabled": False,
          "days": 0
        }
      },
      {
        "category": "AutoScaleLogs",
        "enabled": True,
        "retentionPolicy": {
          "enabled": False,
          "days": 0
        }
      }
    ]
  }
}
  KeyVault_Dignosticsjson = {
    "properties": {
    "workspaceId": wid ,
    "metrics": [
      {
        "category": "AllMetrics",
        "enabled": True,
        "retentionPolicy": {
          "enabled": False,
          "days": 0
        }
      }
    ],
    "logs": [
      {
        "category": "AuditEvent",
        "enabled": True,
        "retentionPolicy": {
          "enabled": False,
          "days": 0
        }
      }
    ]
  }
}
  NetworkSecurityGroups_Dignosticsjson={
    "properties": {
    "workspaceId": wid ,
    "logs": [
      {
        "category": "NetworkSecurityGroupEvent",
        "enabled": True,
        "retentionPolicy": {
          "enabled": False,
          "days": 0
        }
      },
      {
        "category": "NetworkSecurityGroupRuleCounter",
        "enabled": True,
        "retentionPolicy": {
          "enabled": False,
          "days": 0
        }
      }
    ]
  }
}
  SQLDatabase_Dignosticsjson= {
    "properties": {
    "workspaceId": wid ,
    "metrics": [
      {
        "category": "AllMetrics",
        "enabled": True,
        "retentionPolicy": {
          "enabled": False,
          "days": 0
        }
      }
    ],
    "logs": [
      {
        "category": "QueryStoreRuntimeStatistics",
        "enabled": True,
        "retentionPolicy": {
          "enabled": False,
          "days": 0
        }
      },
        {
        "category": "QueryStoreWaitStatistics",
        "enabled": True,
        "retentionPolicy": {
          "enabled": False,
          "days": 0
        }
      },
        {
        "category": "Errors",
        "enabled": True,
        "retentionPolicy": {
          "enabled": False,
          "days": 0
        }
      },
        {
        "category": "DatabaseWaitStatistics",
        "enabled": True,
        "retentionPolicy": {
          "enabled": False,
          "days": 0
        }
      },
        {
        "category": "Timeouts",
        "enabled": True,
        "retentionPolicy": {
          "enabled": False,
          "days": 0
        }
      },
        {
        "category": "Blocks",
        "enabled": True,
        "retentionPolicy": {
          "enabled": False,
          "days": 0
        }
      },
        {
        "category": "SQLInsights",
        "enabled": True,
        "retentionPolicy": {
          "enabled": False,
          "days": 0
        }
      },
        {
        "category": "Audit",
        "enabled": True,
        "retentionPolicy": {
          "enabled": False,
          "days": 0
        }
      }
    ]
  }
}
  AnalysisServices_Dignosticsjson = {
    "properties": {
    "workspaceId": wid ,
    "metrics": [
      {
        "category": "AllMetrics",
        "enabled": True,
        "retentionPolicy": {
          "enabled": False,
          "days": 0
        }
      }
    ],
    "logs": [
      {
        "category": "Engine",
        "enabled": True,
        "retentionPolicy": {
          "enabled": False,
          "days": 0
        }
      },
      {
        "category": "Service",
        "enabled": True,
        "retentionPolicy": {
          "enabled": False,
          "days": 0
        }
      }
    ]
  }
}
  ApiManagement_Dignosticsjson = {
    "properties": {
    "workspaceId": wid ,
    "metrics": [
      {
        "category": "AllMetrics",
        "enabled": True,
        "retentionPolicy": {
          "enabled": False,
          "days": 0
        }
      }
    ],
    "logs": [
      {
        "category": "GatewayLogs",
        "enabled": True,
        "retentionPolicy": {
          "enabled": False,
          "days": 0
        }
      }
    ]
  }
}
  automationAccounts_Dignosticsjson ={
    "properties": {
    "workspaceId": wid ,
    "metrics": [
      {
        "category": "AllMetrics",
        "enabled": True,
        "retentionPolicy": {
          "enabled": False,
          "days": 0
        }
      }
    ],
    "logs": [
      {
        "category": "JobStreams",
        "enabled": True,
        "retentionPolicy": {
          "enabled": False,
          "days": 0
        }
      },      
       {
        "category": "DscNodeStatus",
        "enabled": True,
        "retentionPolicy": {
          "enabled": False,
          "days": 0
        }
       }
    ]
  }
}
  CustomerInsights_dignosticsJson = {
    "properties": {
    "workspaceId": wid ,
    "metrics": [
      {
        "category": "AllMetrics",
        "enabled": True,
        "retentionPolicy": {
          "enabled": False,
          "days": 0
        }
      }
    ],
    "logs": [
      {
        "category": "AuditEvents",
        "enabled": True,
        "retentionPolicy": {
          "enabled": False,
          "days": 0
        }
      }
    ]
  }
}
  IotHubs__dignosticsJson ={
    "properties": {
    "workspaceId": wid ,
    "metrics": [
      {
        "category": "AllMetrics",
        "enabled": True,
        "retentionPolicy": {
          "enabled": False,
          "days": 0
        }
      }
    ],
    "logs": [
      {
        "category": "Connections",
        "enabled": True,
        "retentionPolicy": {
          "enabled": False,
          "days": 0
        }
      },{
        "category": "DeviceTelemetry",
        "enabled": True,
        "retentionPolicy": {
          "enabled": False,
          "days": 0
        }
      },
      {
        "category": "C2DCommands",
        "enabled": True,
        "retentionPolicy": {
          "enabled": False,
          "days": 0
        }
      },
      {
        "category": "FileUploadOperations",
        "enabled": True,
        "retentionPolicy": {
          "enabled": False,
          "days": 0
        }
      },
      {
        "category": "Routes",
        "enabled": True,
        "retentionPolicy": {
          "enabled": False,
          "days": 0
        }
      },
      {
        "category": "D2CTwinOperations",
        "enabled": True,
        "retentionPolicy": {
          "enabled": False,
          "days": 0
        }
      },
      {
        "category": "C2DTwinOperations",
        "enabled": True,
        "retentionPolicy": {
          "enabled": False,
          "days": 0
        }
      },
      {
        "category": "TwinQueries",
        "enabled": True,
        "retentionPolicy": {
          "enabled": False,
          "days": 0
        }
      },
      {
        "category": "JobsOperations",
        "enabled": True,
        "retentionPolicy": {
          "enabled": False,
          "days": 0
        }
      },
      {
        "category": "DirectMethods",
        "enabled": True,
        "retentionPolicy": {
          "enabled": False,
          "days": 0
        }
      },
      {
        "category": "DeviceIdentityOperations",
        "enabled": True,
        "retentionPolicy": {
          "enabled": False,
          "days": 0
        }
      },
      {
        "category": "E2EDiagnostics",
        "enabled": True,
        "retentionPolicy": {
          "enabled": False,
          "days": 0
        }
      }

    ]
  }
}
  redis__dignosticsJson ={
    "properties": {
    "workspaceId": wid ,
    "metrics": [
      {
        "category": "AllMetrics",
        "enabled": True,
        "retentionPolicy": {
          "enabled": False,
          "days": 0
        }
      }
    ]
  }
} 
  batchAccounts__dignosticsJson=  {
    "properties": {
    "workspaceId": wid ,
    "metrics": [
      {
        "category": "AllMetrics",
        "enabled": True,
        "retentionPolicy": {
          "enabled": False,
          "days": 0
        }
      }
    ],
    "logs": [
      {
        "category": "ServiceLog",
        "enabled": True,
        "retentionPolicy": {
          "enabled": False,
          "days": 0
        }
      }
    ]
  }
}

  DataLakeAnalytics__dignosticsJson ={
    "properties": {
    "workspaceId": wid ,
    "metrics": [
      {
        "category": "AllMetrics",
        "enabled": True,
        "retentionPolicy": {
          "enabled": False,
          "days": 0
        }
      }
    ],
    "logs": [
      {
        "category": "Audit",
        "enabled": True,
        "retentionPolicy": {
          "enabled": False,
          "days": 0
        }
      },
      {
        "category": "Requests",
        "enabled": True,
        "retentionPolicy": {
          "enabled": False,
          "days": 0
        }
      }
    ]
  }
}
  DataLakeStore__dignosticsJson = {
    "properties": {
    "workspaceId": wid ,
    "metrics": [
      {
        "category": "AllMetrics",
        "enabled": True,
        "retentionPolicy": {
          "enabled": False,
          "days": 0
        }
      }
    ],
    "logs": [
      {
        "category": "Audit",
        "enabled": True,
        "retentionPolicy": {
          "enabled": False,
          "days": 0
        }
      },
      {
        "category": "Requests",
        "enabled": True,
        "retentionPolicy": {
          "enabled": False,
          "days": 0
        }
      }
    ]
  }
}
  loadBalancers__dignosticsJson = {
    "properties": {
    "workspaceId": wid ,
    "metrics": [
      {
        "category": "AllMetrics",
        "enabled": True,
        "retentionPolicy": {
          "enabled": False,
          "days": 0
        }
      }
    ],
    "logs": [
      {
        "category": "LoadBalancerAlertEvent",
        "enabled": True,
        "retentionPolicy": {
          "enabled": False,
          "days": 0
        }
      },
      {
        "category": "LoadBalancerProbeHealthStatus",
        "enabled": True,
        "retentionPolicy": {
          "enabled": False,
          "days": 0
        }
      }
    ]
  }
}
  LogicApp_dignosticsJson =  {
    "properties": {
    "workspaceId": wid ,
    "metrics": [
      {
        "category": "AllMetrics",
        "enabled": True,
        "retentionPolicy": {
          "enabled": False,
          "days": 0
        }
      }
    ],
    "logs": [
      {
        "category": "WorkflowRuntime",
        "enabled": True,
        "retentionPolicy": {
          "enabled": False,
          "days": 0
        }
      }
    ]
  }
}
  RecoveryServices_Dignosticsjson= {
    "properties": {
    "workspaceId": wid ,
    "logs": [
      {
        "category": "AzureBackupReport",
        "enabled": True,
        "retentionPolicy": {
          "enabled": False,
          "days": 0
        }
      },
      {
        "category": "AzureSiteRecoveryJobs",
        "enabled": True,
        "retentionPolicy": {
          "enabled": False,
          "days": 0
        }
      },
      {
        "category": "AzureSiteRecoveryEvents",
        "enabled": True,
        "retentionPolicy": {
          "enabled": False,
          "days": 0
        }
      },
      {
        "category": "AzureSiteRecoveryReplicatedItems",
        "enabled": True,
        "retentionPolicy": {
          "enabled": False,
          "days": 0
        }
      },
      {
        "category": "AzureSiteRecoveryReplicationStats",
        "enabled": True,
        "retentionPolicy": {
          "enabled": False,
          "days": 0
        }
      },
      {
        "category": "AzureSiteRecoveryRecoveryPoints",
        "enabled": True,
        "retentionPolicy": {
          "enabled": False,
          "days": 0
        }
      },
      {
        "category": "AzureSiteRecoveryReplicationDataUploadRate",
        "enabled": True,
        "retentionPolicy": {
          "enabled": False,
          "days": 0
        }
      },
      {
        "category": "AzureSiteRecoveryProtectedDiskDataChurn",
        "enabled": True,
        "retentionPolicy": {
          "enabled": False,
          "days": 0
        }
      }
    ]
  }
}
  SearchServices_Dignosticsjson = {
    "properties": {
    "workspaceId": wid ,
    "logs": [
      {
        "category": "OperationLogs",
        "enabled": True,
        "retentionPolicy": {
          "enabled": False,
          "days": 0
        }
      }
    ]
  }
}
  virtualMachines__dignosticsJson = {
    "properties": {
    "workspaceId": wid ,
    "metrics": [
      {
        "category": "AllMetrics",
        "enabled": True,
        "retentionPolicy": {
          "enabled": False,
          "days": 0
        }
      }
    ]
  }
} 

  list_dignosticsJson= {
        "Microsoft.AnalysisServices/servers":AnalysisServices_Dignosticsjson,
        "Microsoft.ApiManagement/service": ApiManagement_Dignosticsjson,
        "Microsoft.Network/applicationGateways": ApplicationGateway_Dignosticsjson,
        "Microsoft.Automation/automationAccounts":automationAccounts_Dignosticsjson,
        "Microsoft.Batch/batchAccounts": batchAccounts__dignosticsJson,
        "Microsoft.CustomerInsights/hubs": CustomerInsights_dignosticsJson,
        "Microsoft.DocumentDB/databaseAccounts":CosmosDB_Dignosticsjson,
        "Microsoft.DataLakeAnalytics/accounts" : DataLakeAnalytics__dignosticsJson,
        "Microsoft.DataLakeStore/accounts" : DataLakeStore__dignosticsJson,
        "Microsoft.EventHub/namespaces": EventHubs_Dignosticsjson,
        "Microsoft.Devices/IotHubs": IotHubs__dignosticsJson,
        "Microsoft.KeyVault/vaults": KeyVault_Dignosticsjson,
        "Microsoft.Network/loadBalancers" : loadBalancers__dignosticsJson,
        "Microsoft.Logic/workflows" : LogicApp_dignosticsJson,
        "Microsoft.Network/networkSecurityGroups": NetworkSecurityGroups_Dignosticsjson,
        "Microsoft.RecoveryServices/Vaults" :RecoveryServices_Dignosticsjson,
        "Microsoft.Search/searchServices" : SearchServices_Dignosticsjson,
        "Microsoft.ServiceBus/namespaces": Servicebus_Dignosticsjson ,
        "Microsoft.Sql/servers/databases":SQLDatabase_Dignosticsjson,
        "Microsoft.Cache/Redis": redis__dignosticsJson,
		"Microsoft.Compute/virtualMachines": virtualMachines__dignosticsJson 
        }
  supportedList= [
                  "Microsoft.AnalysisServices/servers",
                  "Microsoft.ApiManagement/service",
                  "Microsoft.Network/applicationGateways",
                  "Microsoft.Automation/automationAccounts",
                  "Microsoft.Batch/batchAccounts",
                  "Microsoft.CustomerInsights/hubs",
                  "Microsoft.DocumentDB/databaseAccounts",
                  "Microsoft.DataLakeAnalytics/accounts",
                  "Microsoft.DataLakeStore/accounts",
                  "Microsoft.EventHub/namespaces",
                  "Microsoft.Devices/IotHubs",
                  "Microsoft.KeyVault/vaults",
                  "Microsoft.Network/loadBalancers",
                  "Microsoft.Logic/workflows",
                  "Microsoft.Network/networkSecurityGroups",
                  "Microsoft.RecoveryServices/Vaults",
                  "Microsoft.Search/searchServices",
                  "Microsoft.ServiceBus/namespaces",
                  "Microsoft.Sql/servers/databases",
                  "Microsoft.Cache/Redis",
				  "Microsoft.Compute/virtualMachines"
                   ]
                   
  json_RG_ResourceList = json.loads(RG_ResourceList)
  for resource in json_RG_ResourceList['value']:
    if resource['type'] in(supportedList):
      try:
        url= "https://management.azure.com/"+resource['id']+"/providers/microsoft.insights/diagnosticSettings/"+dsn+"?api-version=2017-05-01-preview"
        responcestatus  = requests.put(url = url, headers=headers, json=list_dignosticsJson[resource['type']])
        if 200 == responcestatus.status_code:
          print("Enabled/Update Dignostics setting for resource: ",resource['name'], "Type Of Resource is: ",resource['type'] )
        else: 
          print("Something went wrong with resource:  ",resource['name'], "Type Of Resource is: ",resource['type'])
          print("Message: ", responcestatus.content )
      except requests.exceptions.RequestException as e:
          print("Error while request to add/update Dignostics setiing, Detail", e)
          
EnableDignostics(sys.argv[1:])
    
