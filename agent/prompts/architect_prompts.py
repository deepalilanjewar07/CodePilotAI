def architect_prompt(plan: str) -> str:
    return f"""
Break this project into frontend tasks.

Project:
{plan}

Files:
- index.html
- style.css
- app.js

Each step must describe implementation clearly.
"""