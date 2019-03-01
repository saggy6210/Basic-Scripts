#!/bin/bash
##Scope: to Clean old files and directory 
##
ftp -ipn $ftphost <<EOF
  user $username $pswd
  binary
  del file1
  del file2
  cd dir1
  mdel *
  cd ..
  rmdir dir1
  mkdir dir1
  mput file1
  mput file2
  quit
EOF
fi

## Function to upload artifact from dir 
uploadftp(){
  filetoupload=$1
  echo "Uploading to ftp $filetoupload"

## open ftp shell to upload
ftp -ipn $ftphost <<EOF1
  user $username $pswd
  binary
  cd dir
  put $filetoupload
  quit
EOF1
sleep 1
}   

## Loop to upload
cd dir
ls |while read items; do
  uploadftp $items
done
