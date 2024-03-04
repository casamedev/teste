import click
from api_flask.extensions.db import db
from dotenv import load_dotenv
import os
from api_flask.models.user import User, Role
#import hashpassword 
from werkzeug.security import generate_password_hash
from flask import current_app
from api_flask.scripts.seed_data import seed_agendas
load_dotenv()


def create_tables():
    """Creates database tables"""
    with current_app.app_context():
        db.create_all()
        # adicionar a criação das roles iniciais
        admin_role = Role(name="admin")
        admin_user = User(password=generate_password_hash("admin"), email="mds@gmail.com", roles=[admin_role], username= "admin")
        db.session.add(admin_role)
        db.session.add(admin_user)
        db.session.commit()

        user_role = Role(name="user")
        user_user = User(password=generate_password_hash("user"), email="user@gmail.com", roles=[user_role], username= "user")
        db.session.add(user_role)
        db.session.add(user_user)
        db.session.commit()
    print("Tables created")

def drop_db():
    """Cleans database"""
    db.drop_all()
    print("Tables dropped")

def seeda():  
    """Seed vendedores"""
    # seed_vendedores()
    # seed_produtos()
    # seed_cm_clientes_fornec()
    # seed_movimento()
    seed_agendas()

    pass


def create_super_user():
    """Creates a super user"""
    admin_username = os.getenv("ADMIN_USERNAME")
    admin_password = os.getenv("ADMIN_PASSWORD")
    admin_user = User.query.filter_by(username=admin_username).first()
    if not admin_user:
        admin_user = User(username=admin_username, password=generate_password_hash(admin_password))
        admin_user.roles.append(Role.query.filter_by(name="admin").first())
        db.session.add(admin_user)
        db.session.commit()
        print("Super user created")
    else :
        print("Super user already exists")


def init_app(app):
    for command in [create_tables, drop_db, create_super_user, seeda]:
        app.cli.add_command(app.cli.command()(command))

    @app.cli.command()
    @click.option("-username", "-u", prompt=True)
    @click.option(
        "-password", "-p", prompt=True, hide_input=True, confirmation_prompt=True
    )
    def create_simple_user(username, password):
        """Creates a simple user"""
        user = User.query.filter_by(username=username).first()
        if not user:
            user = User(username=username, password=generate_password_hash(password))
            user.roles.append(Role.query.filter_by(name="user").first())
            db.session.add(user)
            db.session.commit()
            print("Simple user created")
        else:
            print("Simple user already exists")
