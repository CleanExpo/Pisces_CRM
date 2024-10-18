from main import create_app, db
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def initialize_database():
    logger.info("Starting database initialization")
    app, _ = create_app()
    with app.app_context():
        try:
            db.create_all()
            logger.info("Database tables created successfully.")
        except Exception as e:
            logger.error(f"Error creating database tables: {str(e)}")
            raise

if __name__ == "__main__":
    initialize_database()
