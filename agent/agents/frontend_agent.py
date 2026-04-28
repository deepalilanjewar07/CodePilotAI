from agent.prompts.frontend_prompts import frontend_prompt
from agent.tools import read_file, write_file
from agent.states import CoderState

def frontend_agent(state: dict) -> dict:
    llm = state["llm"]   # ✅ use shared LLM

    coder_state = state.get("coder_state")

    if coder_state is None:
        coder_state = CoderState(
            task_plan=state["task_plan"],
            current_step_idx=0
        )

    steps = coder_state.task_plan.implementation_steps

    # ✅ If all steps done → move to integration
    if coder_state.current_step_idx >= len(steps):
        return {"coder_state": coder_state, "status": "DONE"}

    step = steps[coder_state.current_step_idx]
    path = f"frontend/{step.filepath}"

    print(f"\n🧱 Working on frontend file: {path}")

    existing = read_file.run({"path": path})

    prompt = frontend_prompt(
        path,
        existing,
        step.task_description
    )

    res = llm.invoke(prompt)

    write_file.run({
        "path": path,
        "content": res.content
    })

    coder_state.current_step_idx += 1

    return {
        **state,
        "coder_state": coder_state,
        "status": "DONE"
    }