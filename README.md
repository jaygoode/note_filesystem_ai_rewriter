a program that recursively goes through a filesystem and has ai rewrite the text files to improve their readability and style.

CONFIG
    -contains changing variables and filepaths, settings

GET/ADD AI PROMPT
    -ai prompts folder
        -contains folder for each type of prompting
            -contains human and system prompt

recursive traversion of root folder
    -goes through each folder and each file, and runs the LLM with selected prompt on file.
    -adds new file to a identical file/folder structure, named new_FOLDERNAME

logging
    - to be created.