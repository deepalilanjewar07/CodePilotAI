
from agent.prompts.planner_prompts import planner_prompt
from agent.states import Plan


def planner_agent(state: dict) -> dict:
    llm = state["llm"]

    resp = llm.with_structured_output(Plan).invoke(
        planner_prompt(state["user_prompt"])
    )

    return {
        **state,
        "plan": resp}