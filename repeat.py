from app import app, db, cli
from app.models import User, Post, Visit

# This function creates a shell context that adds the database instance and models to the shell session
# After adding the shell context processor function we can work with database entities without having to import them
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post, 'Visit': Visit}