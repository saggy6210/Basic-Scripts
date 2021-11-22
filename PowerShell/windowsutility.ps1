# Container Name
$container_name = 'windows-node'

# Folder Path
$destination_path = 'C:\winutility'

# Connection String
$connection_string = 'DefaultEndpointsProtocol=https;AccountName=;AccountKey=;EndpointSuffix=core.windows.net'

# Create A Folder
New-Item -ItemType Directory -Force -Path 'C:\winutility'

# Install Required Packages
Install-PackageProvider -Name NuGet -MinimumVersion 2.8.5.201 -Force

# Install Azure RM Module
Install-Module AzureRM -Force

# Get Storage Account Details
$storage_account = New-AzureStorageContext -ConnectionString $connection_string

# Get Container Details
$blobs = Get-AzureStorageBlob -Container $container_name -Context $storage_account

# Download Each File From Blob To VM
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

# Unzip File
Unzip "C:\winutility\dt-1.8.1.zip" "C:\dt-1.8.1"

# Set To Environment Variable
$Env:Path+= ";" +  "C:\dt-1.8.1"
[Environment]::SetEnvironmentVariable("Path",$env:Path, [System.EnvironmentVariableTarget]::Machine)

# Unzip File
Unzip "C:\winutility\terraform_0.11.7_windows_amd64.zip" "C:\terraform"

# Set To Environment Variable
$Env:Path+= ";" +  "C:\terraform"
[Environment]::SetEnvironmentVariable("Path",$env:Path, [System.EnvironmentVariableTarget]::Machine)

# Install JDK
Start-Process 'C:\winutility\jdk-8u172-windows-x64.exe' -ArgumentList 'INSTALL_SILENT=Enable REBOOT=Disable SPONSORS=Disable' -Wait -PassThru

# Set To Environment Variable
[Environment]::SetEnvironmentVariable("JAVA_HOME", "C:\Program Files\Java\jdk1.8.0_172", "Machine")
