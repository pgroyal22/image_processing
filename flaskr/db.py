import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext

'''
sqlite is a sql based database that we will use to store:
       - users and their creds
       - what photos are associated with each user
''' 
def get_db():

    # establishes a connection to database
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()
    
    # initializes database using sql commands stored in the schema
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))



@click.command('init-db')
@with_appcontext
def init_db_command():
    # provides flask with init_db command through command line
    init_db()
    # prints statement to console
    click.echo('Initialized the database.')

# registers Python DB commands with application instance so that when app is instaniated, DB is instantiated too
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
