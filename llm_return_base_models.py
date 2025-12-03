from pydantic import BaseModel, Field


def get_base_model(model_name: str) -> BaseModel:
    class TextFile(BaseModel):
        text: str = Field(..., description="The improved text file content.")
        suggested_additions: str = Field(..., description="suggested additions to the text that are important to the text concepts.")
        tags: list[str] = Field(..., description="A list of relevant tags for the text file.")
        relevant_commands: list[str] = Field(..., description="A list of helpful commands that are relevant to the text file topics")

    class CVText(BaseModel):
        job_experience: str = Field(..., description="The improved CV job experience text.")
        skills: str = Field(..., description="Improved CV skills section.")
        suggested_skills: str = Field(..., description="A list of suggested skills to add to the CV, if any.")
        job_application_business_name: str = Field(..., description="The business name from the job application.")
        model: str = Field(default="llama2", description="The AI model used to generate the CV content.")

    if model_name == "textfile":
        return TextFile
    elif model_name == "cvtext":
        return CVText