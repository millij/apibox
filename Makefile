
all:

install:
	#install python
	sudo apt-get -y install python
	sudo apt-get -y install python-pip
	sudo apt-get -y install python-virtualenv

	# creating virtual environment
	virtualenv virt_env
	virt_env/bin/pip install -r requirements.txt

