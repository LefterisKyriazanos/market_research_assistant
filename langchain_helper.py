
from dotenv import load_dotenv
from langchain import PromptTemplate
from langchain.chains import LLMChain
from langchain_community.chat_models import ChatOpenAI
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
    print(prompt)
    chain = LLMChain(llm=llm, prompt=prompt)
    response = chain.invoke(input={'goal': goal,'industry': industry, 'product': product})
    return response

if __name__ == "__main__":
    print(generate_survey_statements("car manufacturing", "electric cars"))