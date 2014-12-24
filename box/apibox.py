from flask.ext.script import Server, Manager
from main import create_app

manager = Manager(create_app)
manager.add_command("start", Server())
manager.add_option('-c', '--config', dest='config')
if __name__ == '__main__':
    manager.run()
