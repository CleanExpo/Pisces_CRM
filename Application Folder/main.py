import logging
import os
from flask import Flask, render_template
from flask_socketio import SocketIO
from extensions import db
from routes import register_routes

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_app():
    logger.debug("Creating Flask app")
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'fallback_secret_key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    logger.debug("Initializing database")
    db.init_app(app)
    
    logger.debug("Initializing SocketIO")
    socketio = SocketIO(app, cors_allowed_origins="*", logger=True, engineio_logger=True)

    with app.app_context():
        logger.debug("Creating database tables")
        try:
            db.create_all()
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Error creating database tables: {str(e)}")
            raise

    logger.debug("Registering routes")
    register_routes(app, socketio)

    @app.route('/')
    def index():
        return render_template('index.html')

    return app, socketio

app, socketio = create_app()

if __name__ == '__main__':
    try:
        logger.info("Starting application")
        port = int(os.environ.get('PORT', 5000))
        logger.info(f"Running app on port {port}")
        socketio.run(app, host='0.0.0.0', port=port, debug=True)
    except Exception as e:
        logger.error(f"Error starting the server: {str(e)}")
        raise
