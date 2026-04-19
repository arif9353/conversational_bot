from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict, Any
from agents.input_guardrail import input_guardrail
from agents.pandas_query_generator import pandas_query_generator
from agents.pandas_query_executor import pandas_query_executor
from agents.nl_response import nl_response
import pandas as pd
from agents.visualization import visualization
from utils.generate_visualization_chart import generate_chart
from utils.visualization_data_format import format_data_for_visualization
from agents.pandas_query_validator import pandas_query_validator
# import asyncio
# from utils.print_langgraph_state import print_state

class State(TypedDict):
    # inputs:
    pandas_dataframe : pd.DataFrame
    user_query: str
    data_context: str
    conversation_history: str

    # guardrail:
    enhanced_user_query: str
    continue_conversation: bool

    # pandas query gen+validation+exec
    generated_pandas_query: str
    validated_pandas_query: str
    pandas_result: dict

    # visualization
    visualization_required: bool
    visualization_type: str
    visualization_reason: str
    visualization_data: Any

    # final output:
    answer: str
    visualization_base64: str


async def input_guardrail_agent(state: State) -> State:
    try:
        resp = await input_guardrail(state["user_query"], state["data_context"], state["conversation_history"])
        if resp["isContinue"]:
            state["continue_conversation"] = True
            state["enhanced_user_query"] = resp["contextualized_user_query"]
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


async def pandas_query_validator_agent(state: State) -> State:
    try:
        state["validated_pandas_query"] = await pandas_query_validator(state["enhanced_user_query"], state["data_context"], state["generated_pandas_query"])
        return state
    except Exception as e:
        print("Exception occured in pandas_query_validator_agent() in langgraph_workflow.py as: ",e)
        raise e    
    

async def pandas_query_executor_agent(state: State) -> State:
    try:
        state["pandas_result"] = pandas_query_executor(state["pandas_dataframe"], state["validated_pandas_query"])
        return state
    except Exception as e:
        print("Exception occured in pandas_query_executor_agent() in langgraph_workflow.py as: ",e)
        raise e    


async def nl_response_agent(state: State) -> State:
    try:
        state["answer"] = await nl_response(state["user_query"],state["enhanced_user_query"], state["pandas_result"])
        return state
    except Exception as e:
        print("Exception occured in nl_response_agent() in langgraph_workflow.py as: ",e)
        raise e    


def check_conversation_condition(state: State) -> str:
    try:
        if state["continue_conversation"]:
            return "CONTINUE"
        return "END"
    except Exception as e:
        print("Exception occured in check_conversation_condition() in langgraph_workflow.py as: ",e)
        raise e
    
def check_visualization_condition(state: State) -> str:
    try:
        if state["visualization_required"]:
            return "CONTINUE"
        return "END"
    except Exception as e:
        print("Exception occured in check_condition() in langgraph_workflow.py as: ",e)
        raise e

async def visualization_agent(state: State) -> State:
    try:
        resp = await visualization(state["enhanced_user_query"], state["validated_pandas_query"], state["pandas_result"], state["data_context"])
        state["visualization_type"] = resp["recommended_visualization"]
        state["visualization_reason"] = resp["reason"]
        state["visualization_required"] = resp["recommended_visualization"] != "none"
        return state
    except Exception as e:
        print("Exception occured in visualization_agent() in langgraph_workflow.py as: ",e)
        raise e

async def data_formatter(state: State) -> State:
    try:
        state["visualization_data"] = format_data_for_visualization(state["pandas_result"], state["visualization_type"])
        return state
    except Exception as e:
        print("Exception occured in data_formatter() in langgraph_workflow.py as: ",e)
        raise e
    
async def chart_generator(state: State) -> State:
    try:
        state["visualization_base64"] = generate_chart(state["visualization_data"], state["visualization_type"])
        return state
    except Exception as e:
        print("Exception occured in chart_generator() in langgraph_workflow.py as: ",e)
        raise e

async def build_langgraph_workflow() -> Any:
    try:
        graph = StateGraph(State)

        graph.add_node("input_guardrail_agent", input_guardrail_agent)
        graph.add_node("pandas_query_generator_agent", pandas_query_generator_agent)
        graph.add_node("pandas_query_validator_agent", pandas_query_validator_agent)
        graph.add_node("pandas_query_executor_agent", pandas_query_executor_agent)
        graph.add_node("visualization_agent", visualization_agent)
        graph.add_node("data_formatter", data_formatter)
        graph.add_node("chart_generator", chart_generator)
        graph.add_node("nl_response_agent", nl_response_agent)

        graph.add_edge(START, "input_guardrail_agent")
        graph.add_conditional_edges(
            "input_guardrail_agent",
            check_conversation_condition,
            {
                "END": END,
                "CONTINUE": "pandas_query_generator_agent"
            }                        
        )
        graph.add_edge("pandas_query_generator_agent", "pandas_query_validator_agent")
        graph.add_edge("pandas_query_validator_agent", "pandas_query_executor_agent")
        graph.add_edge("pandas_query_executor_agent", "visualization_agent")
        graph.add_conditional_edges(
            "visualization_agent",
            check_visualization_condition,
            {
                "CONTINUE": "data_formatter",
                "END": "nl_response_agent"
            }
        )
        graph.add_edge("data_formatter", "chart_generator")
        graph.add_edge("chart_generator", "nl_response_agent")
        graph.add_edge("nl_response_agent", END)

        chain = graph.compile()
        # with open ('workflow_architecture.txt', 'w', encoding="utf-8") as f:
        #     f.write(chain.get_graph().draw_ascii())
        return chain
    
    except Exception as e:
        print("Exception Occured in build_langgraph_workflow() in langgraph_workflow.py as: ",e)
        raise e

# if __name__=="__main__":
#     async def _main():
#         df = pd.read_excel("uploads/Route_Input_file (1).xlsx")
#         user_query = "What is the total count of quantity?"
#         with open("dataset_context.txt", "r", encoding="utf-8") as f:
#             dataset_context = f.read()
#         chain = await build_langgraph_workflow()
#         state = await chain.ainvoke({
#             "user_query": user_query,
#             "data_context": dataset_context,
#             "pandas_dataframe": df
#         })
#         print_state(state)
#     asyncio.run(_main())