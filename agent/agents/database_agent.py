from agent.prompts.database_prompts import database_prompt
from agent.tools import write_file

def database_agent(state: dict) -> dict:
    llm = state["llm"]

    print("\n🗄️ Generating database layer...")

    plan = state["plan"].model_dump_json()

    # =========================
    # 1. Generate db.py
    # =========================
    db_code = llm.invoke(
        database_prompt("db.py", plan)
    ).content

    write_file.run({
        "path": "database/db.py",
        "content": db_code
    })

    # =========================
    # 2. Generate models.py
    # =========================
    model_code = llm.invoke(
        database_prompt("models.py", plan)
    ).content

    write_file.run({
        "path": "database/models.py",
        "content": model_code
    })

    # =========================
    # 3. Create __init__.py
    # =========================
    write_file.run({
        "path": "database/__init__.py",
        "content": ""
    })

    return {
        **state,
        "database_generated": True
    }