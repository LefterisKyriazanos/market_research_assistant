
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
import prompt_templates

# load env variables
load_dotenv()


def generate_survey_statements(goal: str, industry: str, product: str):
    """
    Generate survey statements based on the specified goal, industry, and product.

    Parameters:
    - goal (str): The goal of the survey.
    - industry (str): The industry for which the survey is targeted.
    - product (str): The product or service related to the survey.

    Returns:
    - str: The generated survey statements.

    This function generates survey statements using a language model (LLM) and prompts
    tailored to the specified goal, industry, and product. It combines the LLM and prompts
    in multi-step workflows to generate the survey statements.

    Example:
    ```python
    statements = generate_survey_statements(goal="Gather customer feedback",
                                            industry="Retail",
                                            product="Online shopping platform")
    print(statements)
    ```

    """

    # choose model
    llm = ChatOpenAI(model_name="gpt-3.5-turbo-0125", temperature=0.7)

    # define prompt
    prompt = PromptTemplate(
        input_variables=["goal","industry","product"],
        template=prompt_templates.prompt_msg,
    )
    
    # define and run chain
    chain = LLMChain(llm=llm, prompt=prompt)
    response = chain.invoke(input={'goal': goal,'industry': industry, 'product': product})
    
    return response

if __name__ == "__main__":
    # print(generate_survey_statements("car manufacturing", "electric cars"))
    # langchain_agent("Ford Mustang Mach‑E® electric SUV")
    print('ok')