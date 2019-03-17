## Need to install  pip with 9.0.3 
#Install with following command  
#python -m pip install --user --upgrade pip==9.0.3 or python -m pip install --upgrade pip
import pip

def install(package):
    if hasattr(pip, 'main'):
        pip.main(['install', package])
    else:
        pip._internal.main(['install', package])
		
if __name__ == '__main__':
	with open ('requirements.txt') as f:
		package = f.readlines()
		print (package)
		for p in package:
			print (p)
			install(p)
