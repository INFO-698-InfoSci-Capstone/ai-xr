from app import db
from flask import Flask
from dotenv import load_dotenv
import os
from sqlalchemy import text

# Load environment variables
load_dotenv()

def init_db():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://postgres:root@localhost:5432/texturedb')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    
    with app.app_context():
        try:
            # First, execute the schema file to create tables
            print("Creating database schema...")
            with open('schema.sql', 'r') as f:
                schema_sql = f.read()
            
            # Split into individual statements and execute
            statements = [stmt.strip() for stmt in schema_sql.split(';') if stmt.strip()]
            for statement in statements:
                db.session.execute(text(statement))
            
            # Now execute the furniture and texture initialization file
            print("Initializing furniture types, parts, and textures...")
            with open('init_furniture.sql', 'r') as f:
                init_sql = f.read()
            
            # Split into individual statements and execute
            statements = [stmt.strip() for stmt in init_sql.split(';') if stmt.strip()]
            for statement in statements:
                if statement and not statement.startswith('--'):
                    db.session.execute(text(statement))
            
            db.session.commit()
            print("Successfully initialized database!")
            
            # Verify the data
            print("\nVerifying data...")
            
            print("\nFurniture Types:")
            from app import FurnitureType
            types = FurnitureType.query.all()
            for t in types:
                print(f"- {t.name} ({t.category})")
                print("  Parts:")
                for p in t.parts:
                    print(f"    - {p.name}")
                    print("      Compatible textures:")
                    for tc in p.compatible_textures:
                        print(f"        - {tc.name}")
            
        except Exception as e:
            print(f"Error initializing database: {str(e)}")
            db.session.rollback()
            raise e

if __name__ == '__main__':
    init_db() 