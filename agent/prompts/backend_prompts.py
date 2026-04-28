def backend_prompt(plan: str) -> str:
    return f"""
Create a FastAPI backend.

Requirements:
- GET /images
- POST /upload
- DELETE /image/{{id}}

Use in-memory storage (list).

Return ONLY Python code.

Project:
{plan}
"""