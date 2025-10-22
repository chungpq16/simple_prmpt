"""
GenAI Prompt Generator Application
A Streamlit interface for generating custom prompts based on user interests.
"""
import streamlit as st
import time
from typing import Dict, List
import os
from datetime import datetime
from llm_client import LLMFarmClient
from prompt_generator import PromptGenerator
from logger import get_logger

# Configure page
st.set_page_config(
    page_title="Prompt Generator",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

logger = get_logger()


@st.cache_resource
def initialize_app():
    """Initialize the application components."""
    try:
        llm_client = LLMFarmClient()
        prompt_gen = PromptGenerator(llm_client)
        return llm_client, prompt_gen
    except Exception as e:
        st.error(f"Failed to initialize application: {str(e)}")
        st.info("Please check your environment configuration (.env file)")
        return None, None


def display_info_section():
    """Display information section inline."""
    with st.expander("ℹ️ About & Examples", expanded=False):
        st.markdown("""
        **About this app:**
        This application generates custom prompts based on your task description. 
        Simply describe what you want to accomplish, and get a professional prompt template!
        
        **Example Tasks:**
        - Draft an email responding to a customer complaint
        - Choose an item from a menu based on preferences  
        - Rate a resume according to a rubric
        - Explain a complex concept in simple terms
        - Design a marketing strategy for a new product
        
        """)


def main():
    """Main application interface."""
    
    # Initialize app components
    llm_client, prompt_gen = initialize_app()
    
    if not llm_client or not prompt_gen:
        st.stop()
    
    # Main interface
    st.title("🤖 GenAI Prompt Generator")
    st.markdown("Transform your task descriptions into professional prompt templates")
    
    # Display info section inline
    display_info_section()
    
    st.markdown("---")
    
    # Task input section
    st.subheader("Describe Your Task")
    
    task_description = st.text_area(
        "What task would you like to create a prompt for?",
        placeholder="Example: Draft an email responding to a customer complaint",
        height=120,
        help="Describe the task you want to create a prompt template for. Be specific about what you want the AI to accomplish."
    )
    
    # Generate button
    st.markdown("---")
    generate_button = st.button(
        "🚀 Generate Prompt Template",
        type="primary",
        disabled=not task_description.strip(),
        use_container_width=True
    )
    
    # Generation logic
    if generate_button and task_description.strip():
        start_time = time.time()
        
        # Simple console logging
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] USER QUERY: {task_description}")
        
        try:
            with st.spinner("Generating your custom prompt template..."):
                # Add debug info in development
                if os.getenv('DEBUG', 'false').lower() == 'true':
                    st.info(f"Debug: Task = {task_description[:100]}...")
                
                # Let LLM automatically determine variables
                result = prompt_gen.generate_prompt_template(task_description, variables=None)
            
            generation_time = time.time() - start_time
            
            # Log generation result
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] GENERATION SUCCESS: {generation_time:.2f}s, Variables: {len(result.get('variables', []))}")
            
            # Display results
            st.success(f"✅ Prompt template generated successfully! ({generation_time:.2f}s)")
            
            # Store in session state for persistent display
            st.session_state.generated_result = result
            
        except Exception as e:
            generation_time = time.time() - start_time
            
            # Log generation error
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] GENERATION ERROR: {str(e)} ({generation_time:.2f}s)")
            
            st.error(f"❌ Error generating prompt template: {str(e)}")
            
            # Show additional debug info if available
            with st.expander("🔍 Debug Information", expanded=False):
                st.code(f"""
Error Details:
- Error Type: {type(e).__name__}
- Error Message: {str(e)}
- Task: {task_description}
- Generation Time: {generation_time:.2f}s

If this error persists:
1. Check your LLM Farm connection
2. Try a simpler task description
3. Check the application logs
""", language="text")
            
            logger.error(f"Generation error: {str(e)}")
    
    # Display generated prompt template if available
    if "generated_result" in st.session_state:
        result = st.session_state.generated_result
        
        st.markdown("---")
        st.subheader("Generated Prompt Template")
        
        # Variables information
        if result.get("variables"):
            st.markdown("**Variables detected:**")
            cols = st.columns(min(len(result["variables"]), 4))
            for i, var in enumerate(result["variables"]):
                with cols[i % 4]:
                    st.code(f"{{{var}}}", language="text")
        
        # The actual prompt template - always visible
        st.markdown("**Prompt Template:**")
        st.text_area(
            "Generated Prompt",
            value=result["prompt_template"],
            height=400,
            help="This is your generated prompt template. Copy and use it in your AI applications!",
            key="persistent_prompt_display"
        )
        
        # Warning for floating variables
        if result.get("floating_variables"):
            st.warning(f"⚠️ Detected floating variables: {result['floating_variables']}")
            st.info("These variables might need manual adjustment for optimal results.")
        
        # Download option
        st.download_button(
            label="📥 Download Prompt Template",
            data=result["prompt_template"],
            file_name=f"prompt_template_{int(time.time())}.txt",
            mime="text/plain"
        )
        
        # Testing section
        st.markdown("---")
        st.subheader("Test Your Prompt Template")
        
        with st.expander("🧪 Test the Generated Prompt", expanded=False):
            st.info("Provide values for the variables to test how the prompt works.")
            
            # Create input fields for each variable
            test_values = {}
            if result.get("variables"):
                for variable in result["variables"]:
                    test_values[variable] = st.text_area(
                        f"Value for {variable}:",
                        placeholder=f"Enter value for {variable}...",
                        key=f"test_{variable}",
                        height=100
                    )
            
            # Test button
            if st.button("🎯 Test Prompt", key="test_prompt"):
                if all(value.strip() for value in test_values.values()):
                    # Log test attempt
                    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] PROMPT TEST: Variables={len(test_values)}")
                    
                    try:
                        with st.spinner("Testing prompt template..."):
                            test_result = prompt_gen.test_prompt_template(
                                result["prompt_template"], 
                                test_values
                            )
                        
                        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] TEST SUCCESS")
                        
                        # Store test result in session state to persist it
                        st.session_state.test_result = test_result
                        st.success("✅ Test completed!")
                        
                    except Exception as e:
                        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] TEST ERROR: {str(e)}")
                        
                        st.error(f"❌ Error testing prompt: {str(e)}")
                        if "test_result" in st.session_state:
                            del st.session_state.test_result
                else:
                    st.warning("⚠️ Please provide values for all variables before testing.")
            
            # Display test result if available
            if "test_result" in st.session_state:
                st.markdown("**AI Response:**")
                st.markdown(st.session_state.test_result)


if __name__ == "__main__":
    main()