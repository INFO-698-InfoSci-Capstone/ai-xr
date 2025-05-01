from app import db, FurniturePart, FurnitureType, TextureCategory, part_texture_categories
from flask import Flask
from dotenv import load_dotenv
import os
from sqlalchemy import text

# Load environment variables
load_dotenv()

def init_relationships():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://postgres:root@localhost:5432/texturedb')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    with app.app_context():
        try:
            # Read the SQL file
            with open('init_relationships.sql', 'r') as f:
                sql_content = f.read()
            
            # Split into individual statements and execute
            statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]
            
            for statement in statements:
                if statement and not statement.startswith('--'):
                    # Execute each statement with proper text() wrapper
                    db.session.execute(text(statement))
            
            db.session.commit()
            print("Successfully initialized relationships!")

            # Verify the data
            print("\nVerifying relationships...")
            
            print("\nFurniture Parts:")
            parts = FurniturePart.query.all()
            for part in parts:
                print(f"- {part.name}")

            print("\nFurniture Types with their parts:")
            types = FurnitureType.query.all()
            for ftype in types:
                print(f"\n{ftype.name} ({ftype.category}):")
                for part in ftype.parts:
                    print(f"- {part.name}")

            print("\nTexture Categories and their compatible parts:")
            categories = TextureCategory.query.all()
            for category in categories:
                print(f"\n{category.name}:")
                try:
                    # Use the relationship defined in the model
                    compatible_parts = category.compatible_parts
                    for part in compatible_parts:
                        print(f"- {part.name}")
                except Exception as e:
                    print(f"Error processing category {category.name}: {str(e)}")

        except Exception as e:
            print(f"Error initializing relationships: {str(e)}")
            db.session.rollback()
            raise e

if __name__ == '__main__':
    init_relationships() 