from flask import Flask

def create_app():
    app = Flask(__name__)
    
    #Chargement de la configuration
    app.config.from_object('config')
    
    #Importation des routes 
    from .routes import main
    app.register_blueprint(main)
    
    return app