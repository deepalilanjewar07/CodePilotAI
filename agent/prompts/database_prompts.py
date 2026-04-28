def database_prompt(file_type: str, plan: str) -> str:

    if file_type == "db.py":
        return f"""
You are a backend database engineer.

Create SQLAlchemy database setup for a FastAPI project.

Requirements:
- Use SQLAlchemy (NOT sqlite3)
- SQLite database: images.db
- Create engine
- Create SessionLocal
- Create Base (declarative_base)

Return ONLY Python code.

Project:
{plan}
"""

    if file_type == "models.py":
        return f"""
You are a backend database engineer.

Create SQLAlchemy model for a photo gallery app.

Requirements:
- Table: images
- id: Integer primary key
- filename: String
- content: String (base64 image)

Return ONLY Python code.

Project:
{plan}
"""