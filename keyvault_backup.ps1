Param(
	[Parameter(Mandatory = $true)]
	[String]$vaultName,
    [Parameter(Mandatory = $true)]
	[String]$storageAccountName,
    [Parameter(Mandatory = $true)]
	[String]$storageContainerName
)

Write-Output "Login Successful"
New-Item -ItemType Directory -Force -Path C:\keyVaultBkp

#$basePath = C:\keyVaultBkp
#$basePath = $env:keyVaultBkp ##" $env:keyVaultBkp + '\'

#echo 	"basepath: $basePath" 
Set-Location C:\keyVaultBkp
$date = Get-Date;

$datePart = $date.ToString("yyyy") + '\' + $date.ToString("MMdd") + '\';

$backupcertificatePath = $basePath + $datePart + $vaultName + "\certificates\";

$backupKeyPath = $basePath + $datePart + $vaultName + "\Keys\";

$backupSecretPath = $basePath + $datePart + $vaultName + "\Secrets\";

$allCertificateNames = [System.Collections.ArrayList]@()

New-Item -ItemType Directory -Force -Path $backupKeyPath

New-Item -ItemType Directory -Force -Path $backupSecretPath

Write-Output "Backup key path is :" $backupKeyPath 

Write-Output "Backup secret path is :" $backupSecretPath

Write-Output "Backup certificate path is :" $backupcertificatePath

Write-Output "Getting keys for Vault : " $vaultName;

#In portal when a user adds a certificate, a key and secret with the same name gets added to the keys and secret list.
#Since the Get Key and Get Secret will all return the certificate name, we need to exclude the same while taking the back-up.
$allCertificates = Get-AzureKeyVaultCertificate -VaultName $VaultName

foreach ($certificate in $allCertificates) {

    $outputcertificatepath = $backupcertificatePath + $certificate.Name + ".blob"

    Write-Output "Backing up certificate: " $outputcertificatepath;

    Backup-AzureKeyVaultCertificate -VaultName $vaultName -Name $certificate.Name -OutputFile $outputcertificatepath -Force
    
    $allCertificateNames.Add($certificate.Name)
 }

$allKeys = Get-AzureKeyVaultKey -VaultName $VaultName

foreach ($key in $allKeys) {

    #If it's a certificate key, ignore as already backup has been taken
    if (!$allCertificateNames.Contains($key.Name))   {
        
        $outputkeypath = $backupKeyPath + $key.Name + ".blob"

        Write-Output "Backing up key: " $outputkeypath;

        Backup-AzureKeyVaultKey -VaultName $vaultName -Name $key.Name -OutputFile $outputkeypath -Force

    }else {
        Write-Output "NOT backing up key as it's a certificate key and explicit backup is already done: " $key.Name;
    }
  
 }

 $allSecrets = Get-AzureKeyVaultSecret -VaultName $VaultName
 
 foreach ($secret in $allSecrets) {
    #If it's a certificate secret, ignore as already backup has been taken
    if (!$allCertificateNames.Contains($secret.Name))   {

        $outputsecretpath = $backupSecretPath + $secret.Name + ".blob"

        Write-Output "Backing up secret: " $outputsecretpath;

        Backup-AzureKeyVaultSecret -VaultName $vaultName -Name $secret.Name -OutputFile $outputsecretpath -Force

    }else {
        Write-Output "NOT backing up secret as it's a certificate secret and explicit backup is already done: " $secret.Name;
    }
 }

Write-Output "Backup completed"

Write-Output "Upload Starts"

#Back up to Azure Storage Starts
$storageContainer = Get-AzureRmStorageAccount | where {$_.StorageAccountName -eq $storageAccountName} | Get-AzureStorageContainer | where {$_.Name -eq $storageContainerName}

#Get all the generated files
$allFiles = Get-ChildItem -Path "C:\keyVaultBkp" –Recurse -File

foreach ($file in $allFiles){ 
   
   $filePath = $file.FullName 

   Write-Output "Uploading " $filePath

   $blobPath = $filePath.Replace("C:\keyVaultBkp", "")
   
   $storageContainer | Set-AzureStorageBlobContent –File $filePath –Blob $blobPath -Force

} 

Write-Output "Upload Completed"
