from flask.ext.script import Server, Manager
from app22 import create_app

manager = Manager(create_app)
manager.add_command("runserver", Server())
manager.add_option('-c', '--config', dest='config')
if __name__ == '__main__':
    manager.run()
