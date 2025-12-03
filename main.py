# from langchain_community.chat_models import ChatOllama
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from pprint import pprint
import file_handler



class TextFile(BaseModel):
    text: str = Field(..., description="The improved text file content.")
    suggested_additions: str = Field(..., description="suggested additions to the text that are important to the text concepts.")
    tags: list[str] = Field(..., description="A list of relevant tags for the text file.")
    relevant_commands: list[str] = Field(..., description="A list of helpful commands that are relevant to the text file topics")

def rewrite_text_file(job_desc: str, cv_data:dict, model: str) -> dict[str]:
    """
    Takes text file content and rewrites it to improve readability, style, and adding useful data.
    Returns parsed TextFile object.
    """
    
    llm = ChatOllama(model=model, temperature=0.3)
    parser = PydanticOutputParser(pydantic_object=TextFile)
    prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are a senior CV optimization expert specializing in cybersecurity and software development. "
     "Your job is to rewrite the applicant's CV *strictly based on the provided CV text*, and tailor "
     "it to the provided job description **without inventing or fabricating any information**.\n\n"

     "⚠️ STRICT RULES (NO EXCEPTIONS):\n"
     "1. You may ONLY use information explicitly found in the provided CV job experience text or skills text.\n"
     "- model\n\n"
     "{format_instructions}"
    ),

    ("human",
     "JOB APPLICATION DESCRIPTION:\n{job_desc}\n\n"
     "CURRENT CV JOB EXPERIENCE TEXT:\n{cv_job_experience_text}\n\n"
     "CURRENT CV SKILLS SECTION TEXT:\n{cv_skills_text}\n\n"
     "TASK:\n"
     "Rewrite the job experience and skills sections so they better reflect the job description, "
     "while strictly following the rules above. Again: do NOT add new skills or experience not present in the CV.")
])

    formatted = prompt.format(
        job_desc=job_desc,
        cv_job_experience_text=cv_data_dict["cv_job_experience_text"],
        cv_skills_text=cv_data_dict["cv_skills_text"],
        format_instructions=parser.get_format_instructions(),
    )

    response = llm.invoke(formatted)
    updated_cv = parser.parse(response.content)
    return updated_cv.model_dump()

if __name__ == "__main__":
    input_fp = "./input_files"
    # model = "qwen3:30b"
    model = "gpt-oss:20b"
    cv_data_dict = file_handler.read_yaml_file(f"{input_fp}/CV_data.yaml")
    job_application_text = file_handler.read_txt_file(f"{input_fp}/job_application_text.txt")
    updated_cv = tailor_cv_text(job_application_text, cv_data_dict, model)
    file_handler.write_to_text_file(updated_cv)
    pprint(updated_cv)