
all:

install:
#install python
	sudo apt-get install python
	sudo apt-get install python-pip
	sudo apt-get install python-virtualenv

# creating virtual environment
	virtualenv envi 	
# in
	envi/bin/pip install -r requirements.txt                        		 

	
