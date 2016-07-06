from werkzeug.utils import secure_filename
from flask_script import Manager
from app import create_app,db,models
from flask_migrate import Migrate,MigrateCommand,upgrade
from flask.ext.script import Shell

app = create_app()
manager = Manager(app)
migrate = Migrate(app,db)
manager.add_command('db',MigrateCommand)


def make_shell_context():
    return dict(app=app, db=db, User=models.User)
manager.add_command("shell", Shell(make_context=make_shell_context))

@manager.command
def dev():
    from livereload import Server
    live_server = Server(app.wsgi_app)
    live_server.watch('**/*.*')
    live_server.serve(open_url=True)

@manager.command
def test():
    pass

@manager.command
def deploy():
    upgrade()


if __name__ == '__main__':
    #dev()
    #deploy()
    manager.run()