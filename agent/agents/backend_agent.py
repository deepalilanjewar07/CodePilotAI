from agent.prompts.backend_prompts import backend_prompt
from agent.tools import write_file, read_file

def backend_agent(state: dict) -> dict:
    llm = state["llm"]

    print("\n🔧 Generating / Updating backend...")

    # Read existing backend (if any)
    existing_code = read_file.run({
        "path": "backend/main.py"
    })

    # Create prompt
    prompt = backend_prompt(state["plan"].model_dump_json()) + f"""

EXISTING BACKEND CODE:
{existing_code}

INSTRUCTION:
- If code exists → improve it
- If empty → create full backend
- Must use FastAPI
- Must connect to database (database/db.py)
"""

    # Call LLM
    res = llm.invoke(prompt)

    # Write backend file
    write_file.run({
        "path": "backend/main.py",
        "content": res.content
    })

    return state