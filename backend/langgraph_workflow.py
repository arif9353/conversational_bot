from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict, Any
from agents.input_guardrail import input_guardrail
from agents.pandas_query_generator import pandas_query_generator
from agents.pandas_query_executor import pandas_query_executor
from agents.nl_response import nl_response
import pandas as pd


class State(TypedDict):
    pandas_dataframe : pd.DataFrame
    user_query: str
    enhanced_user_query: str
    pandas_result: dict
    generated_pandas_query: str
    answer: str
    data_context: str
    continue_conversation: bool


async def input_guardrail_agent(state: State) -> State:
    try:
        resp = await input_guardrail(state["user_query"], state["data_context"])
        if resp["isContinue"]:
            state["continue_conversation"] = True
            state["enhanced_user_query"] = resp["query"]
        else:
            state["continue_conversation"] = False
            state["answer"] = resp["query"]
        return state
    except Exception as e:
        print("Exception occured in input_guardrail_agent() in langgraph_workflow.py as: ",e)
        raise e


async def pandas_query_generator_agent(state: State) -> State:
    try:
        state["generated_pandas_query"] = await pandas_query_generator(state["enhanced_user_query"], state["data_context"])
        return state
    except Exception as e:
        print("Exception occured in pandas_query_generator_agent() in langgraph_workflow.py as: ",e)
        raise e    
    

async def pandas_query_executor_agent(state: State) -> State:
    try:
        state["pandas_result"] = await pandas_query_executor(state["generated_pandas_query"], state["pandas_dataframe"])
        return state
    except Exception as e:
        print("Exception occured in pandas_query_executor_agent() in langgraph_workflow.py as: ",e)
        raise e    


async def nl_response_agent(state: State) -> State:
    try:
        state["answer"] = await nl_response(state["enhanced_user_query"], state["pandas_result"])
        return state
    except Exception as e:
        print("Exception occured in nl_response_agent() in langgraph_workflow.py as: ",e)
        raise e    


def check_condition(state: State) -> str:
    try:
        if state["continue_conversation"]:
            return "CONTINUE"
        return "END"
    except Exception as e:
        print("Exception occured in check_condition() in langgraph_workflow.py as: ",e)
        raise e


async def build_langgraph_workflow() -> Any:
    try:
        graph = StateGraph(State)

        graph.add_node("input_guardrail_agent", input_guardrail_agent)
        graph.add_node("pandas_query_generator_agent", pandas_query_generator_agent)
        graph.add_node("pandas_query_executor_agent", pandas_query_executor_agent)
        graph.add_node("nl_response_agent", nl_response_agent)

        graph.add_edge(START, "input_guardrail_agent")
        graph.add_conditional_edges(
            "input_guardrail_agent",
            check_condition,
            {
                "END": "END",
                "CONTINUE": "pandas_query_generator_agent"
            }                        
        )
        graph.add_edge("pandas_query_generator_agent", "pandas_query_executor_agent")
        graph.add_edge("pandas_query_executor_agent", "nl_response_agent")
        graph.add_edge("nl_response_agent", END)

        chain = graph.compile()
        return chain
    
    except Exception as e:
        print("Exception Occured in build_langgraph_workflow() in langgraph_workflow.py as: ",e)
        raise e