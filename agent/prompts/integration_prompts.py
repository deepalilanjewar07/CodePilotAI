def integration_prompt(frontend_code: str, backend_code: str) -> str:
    return f"""
Connect frontend with backend.

Backend:
{backend_code}

Frontend:
{frontend_code}

Use fetch() for API calls.

Return updated JS only.
"""