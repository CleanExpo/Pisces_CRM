from main import create_app, db

def setup_database():
    app, _ = create_app()
    with app.app_context():
        db.create_all()
        print("Database tables created successfully.")

if __name__ == "__main__":
    setup_database()
