
all:

install:
	#install python
	sudo apt-get -y install python
	sudo apt-get -y install python-pip
	sudo apt-get -y install python-virtualenv

	# creating virtual environment
	virtualenv envi
	envi/bin/pip install -r requirements.txt

	
