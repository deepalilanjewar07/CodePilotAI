from agent.prompts.integration_prompts import integration_prompt
from agent.tools import read_file, write_file

def integration_agent(state: dict) -> dict:
    llm = state["llm"]

    print("\n🔗 Connecting frontend with backend...")

    # Read files
    frontend_js = read_file.run({"path": "frontend/app.js"})
    backend_code = read_file.run({"path": "backend/main.py"})

    prompt = integration_prompt(frontend_js, backend_code)

    res = llm.invoke(prompt)

    # Update frontend JS
    write_file.run({
        "path": "frontend/app.js",
        "content": res.content
    })

    return {
        **state
    }