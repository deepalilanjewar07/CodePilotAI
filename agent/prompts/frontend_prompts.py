def frontend_prompt(filepath: str, existing_code: str, task: str) -> str:
    return f"""
You are editing a frontend file.

FILE: {filepath}

EXISTING CODE:
{existing_code}

TASK:
{task}

Rules:
- Return FULL updated file
- Do not break existing code
"""