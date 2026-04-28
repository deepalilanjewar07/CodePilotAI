from agent.prompts.architect_prompts import architect_prompt
from agent.states import TaskPlan, Plan


def architect_agent(state: dict) -> dict:
    llm = state["llm"]

    resp = llm.with_structured_output(TaskPlan).invoke(
        architect_prompt(state["plan"].model_dump_json())
    )

    return {
        **state,
        "task_plan": resp}