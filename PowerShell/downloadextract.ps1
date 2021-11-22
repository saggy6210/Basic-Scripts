$container_name = 'backuprestoreutility'
$destination_path = 'C:\utility'
$connection_string = 'bkpConnStr'
New-Item -ItemType Directory -Force -Path 'C:\utility'
Install-PackageProvider -Name NuGet -MinimumVersion 2.8.5.201 -Force
Install-Module AzureRM -Force
$storage_account = New-AzureStorageContext -ConnectionString $connection_string

$blobs = Get-AzureStorageBlob -Container $container_name -Context $storage_account

foreach ($blob in $blobs)
    {
		New-Item -ItemType Directory -Force -Path $destination_path
  
        Get-AzureStorageBlobContent `
        -Container $container_name -Blob $blob.Name -Destination $destination_path `
		-Context $storage_account
    }

Add-Type -AssemblyName System.IO.Compression.FileSystem
function Unzip
{
    param([string]$zipfile, [string]$outpath)

    [System.IO.Compression.ZipFile]::ExtractToDirectory($zipfile, $outpath)
}

Unzip "C:\utility\BackupRestore.zip" "C:\utility\BackupRestore"
Copy-Item -Path C:\utility\appsettings.json -Destination c:\utility\BackupRestore\BackupRestore\Backup\appsettings.json
Start-Process -FilePath "C:\utility\dotnet-sdk-2.1.401-win-gs-x64.exe" -ArgumentList /S, /v, /qn -Wait
