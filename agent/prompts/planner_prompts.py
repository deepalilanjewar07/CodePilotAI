def planner_prompt(user_prompt: str) -> str:
    return f"""
You are a software planner.

Convert the user request into a structured plan.

User request:
{user_prompt}

Output:
- name
- description
- techstack (frontend + backend)
- features
- files needed
"""