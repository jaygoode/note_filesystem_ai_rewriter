# from langchain_community.chat_models import ChatOllama
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from pprint import pprint
import file_handler
from llm_return_base_models import get_base_model





def rewrite_text_file(text_fp: str, model: str, basemodel_name:str) -> dict[str]:
    """
    Takes text file content and rewrites it to improve readability, style, and adding useful data.
    Returns parsed TextFile object.
    """
    text = file_handler.read_txt_file(text_fp)
    llm = ChatOllama(model=model, temperature=0.3)
    parser = PydanticOutputParser(pydantic_object=get_base_model(basemodel_name))
    prompt = ChatPromptTemplate.from_messages([
    ("system",
    
     "{format_instructions}"
    ),

    ("human",
      file_handler.read_yaml_file(human_prompt_file)
      )
])

    formatted = prompt.format(
        text=text,
        cv_job_experience_text=cv_data_dict["cv_job_experience_text"],
        cv_skills_text=cv_data_dict["cv_skills_text"],
        format_instructions=parser.get_format_instructions(),
    )

    response = llm.invoke(formatted)
    updated_cv = parser.parse(response.content)
    return updated_cv.model_dump()

if __name__ == "__main__":
    config = file_handler.read_yaml_file("config.yaml")
    job_application_text = file_handler.read_txt_file(f"{input_fp}/job_application_text.txt")
    updated_cv = rewrite_text_file(job_application_text, cv_data_dict, model)
    file_handler.write_to_text_file(updated_cv)
    pprint(updated_cv)