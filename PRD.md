# Instructions to Read Folder `ai-docs`

## Files and Their Purpose

1. **llm-farm-integrate**  
    - Description: Guide on how to use the corporate LLM farm.

2. **prompt_generator.ipynb**  
    - Description: Explains the concept of the prompt generator application.

## Steps to Access the Folder
1. Navigate to the `ai-docs` directory using the terminal or file explorer.
2. Open the relevant file based on your requirement:
    - For LLM farm integration, refer to `llm-farm-integrate`.
    - For understanding the prompt generator, open `prompt_generator.ipynb`.
3. Use a text editor or Jupyter Notebook to view and edit the files as needed.



## Product Requirements Document (PRD) for GenAI Prompt Generator Application

### Objective
Develop a Generative AI (GenAI) application that generates prompts based on user interests.

### Key Features
1. **LLM Integration**  
    - Utilize the corporate LLM farm to access and integrate large language models for generating prompts.

2. **Concept Implementation**  
    - Implement the core concept outlined in the `prompt_generator.ipynb` file to ensure consistency and reusability.

3. **User Interface**  
    - Create a minimal Streamlit-based UI to allow end users to interact with the GenAI application seamlessly.

### Functional Requirements
1. **Prompt Generation**  
    - Accept user input to determine their area of interest.
    - Generate contextually relevant prompts using the LLM models.

2. **UI Features**  
    - Input field for user interests.
    - Display area for generated prompts.
    - Button to trigger prompt generation.

3. **Backend Integration**  
    - Connect the Streamlit UI with the LLM farm backend for processing user requests.

### Non-Functional Requirements
1. **Performance**  
    - Ensure prompt generation is completed within 2 seconds for a smooth user experience.
    x
3. **Usability**  
    - Keep the UI intuitive and minimalistic for non-technical users.

### Deliverables
1. Fully functional GenAI application with integrated LLM models.
2. Streamlit-based UI for end-user interaction.
3. Documentation for setup, usage, and maintenance.
