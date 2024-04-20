
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
# from langchain import PromptTemplate
from langchain.chains import LLMChain
# from langchain_community.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
import prompt_templates

load_dotenv()

def generate_survey_statements(goal, industry, product):

    # --------------------------------------------------------------
    # LLMs: Get predictions from a language model
    # --------------------------------------------------------------

    llm = ChatOpenAI(model_name="gpt-3.5-turbo-0125", temperature=0.7)

    # --------------------------------------------------------------
    # Chains: Combine LLMs and prompts in multi-step workflows
    # --------------------------------------------------------------

    prompt = PromptTemplate(
        input_variables=["goal","industry","product"],
        template=prompt_templates.prompt_msg,
    )
    # print(prompt)
    chain = LLMChain(llm=llm, prompt=prompt)
    response = chain.invoke(input={'goal': goal,'industry': industry, 'product': product})
    return response


# def langchain_agent(product):
#     llm = ChatOpenAI(model_name="gpt-3.5-turbo-0125", temperature=0.7)
#     tools = load_tools(['wikipedia'], llm=llm)

#     # verbose = True returns the reasoning behind the answer
#     agent = initialize_agent(tools, llm, agent= AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=False)

#     result = agent.invoke(f"What products are similar to {product}")
#     print(result)


if __name__ == "__main__":
    # print(generate_survey_statements("car manufacturing", "electric cars"))
    # langchain_agent("Ford Mustang Mach‑E® electric SUV")
    print('ok')