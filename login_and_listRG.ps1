Connect-AzureRmAccount
$name = Read-Host 'What is subscription name?'
Select-AzureRmSubscription -Subscription "$name"
Get-AzureRmContext
$resourceGroup = Get-AzureRmResourceGroup
foreach ($rg in $resourceGroup)
{
	Write-Host $rg.ResourceGroupName	
}
