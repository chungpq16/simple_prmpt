"""
GenAI Prompt Generator Application
A Streamlit interface for generating custom prompts based on user interests.
"""
import streamlit as st
import time
from typing import Dict, List
import os
from llm_client import LLMFarmClient
from prompt_generator import PromptGenerator
from logger import get_logger

# Configure page
st.set_page_config(
    page_title="GenAI Prompt Generator",
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


def display_sidebar():
    """Display the sidebar with app information and configuration."""
    with st.sidebar:
        st.title("🤖 GenAI Prompt Generator")
        st.markdown("---")
        
        st.subheader("About")
        st.info(
            "This application generates custom prompts based on your task description. "
            "Simply describe what you want to accomplish, and get a professional prompt template!"
        )
        
        st.subheader("Example Tasks")
        st.markdown("""
        - Draft an email responding to a customer complaint
        - Choose an item from a menu based on preferences
        - Rate a resume according to a rubric
        - Explain a complex concept in simple terms
        - Design a marketing strategy for a new product
        """)
        
        st.markdown("---")
        st.caption("Powered by Corporate LLM Farm")


def main():
    """Main application interface."""
    
    # Initialize app components
    llm_client, prompt_gen = initialize_app()
    
    if not llm_client or not prompt_gen:
        st.stop()
    
    # Display sidebar
    display_sidebar()
    
    # Main interface
    st.title("GenAI Prompt Generator")
    st.markdown("Transform your task descriptions into professional prompt templates")
    
    # Health check
    if st.button("🔍 Check LLM Farm Connection", key="health_check"):
        with st.spinner("Checking connection..."):
            if llm_client.health_check():
                st.success("✅ LLM Farm connection is healthy!")
            else:
                st.error("❌ LLM Farm connection failed")
                st.stop()
    
    st.markdown("---")
    
    # Task input section
    st.subheader("1. Describe Your Task")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        task_description = st.text_area(
            "What task would you like to create a prompt for?",
            placeholder="Example: Draft an email responding to a customer complaint",
            height=100,
            help="Describe the task you want to create a prompt template for. Be specific about what you want the AI to accomplish."
        )
    
    with col2:
        st.markdown("### Quick Examples")
        if st.button("Email Response", key="example1"):
            st.session_state.task_input = "Draft an email responding to a customer complaint"
        if st.button("Menu Selection", key="example2"):
            st.session_state.task_input = "Choose an item from a menu based on user preferences"
        if st.button("Resume Rating", key="example3"):
            st.session_state.task_input = "Rate a resume according to a rubric"
    
    # Handle example selection
    if "task_input" in st.session_state:
        task_description = st.session_state.task_input
        del st.session_state.task_input
        st.rerun()
    
    # Variables section (optional)
    st.subheader("2. Specify Variables (Optional)")
    
    with st.expander("Advanced: Custom Variables"):
        st.info("Leave empty to let the AI choose appropriate variables automatically.")
        custom_variables = st.text_input(
            "Variable names (comma-separated)",
            placeholder="CUSTOMER_COMPLAINT, COMPANY_NAME",
            help="Specify custom variable names if you have specific requirements. Use ALL_CAPS format."
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
        
        # Parse custom variables
        variables = None
        if custom_variables.strip():
            variables = [var.strip().upper() for var in custom_variables.split(",") if var.strip()]
        
        try:
            with st.spinner("Generating your custom prompt template..."):
                result = prompt_gen.generate_prompt_template(task_description, variables)
            
            generation_time = time.time() - start_time
            
            # Display results
            st.success(f"✅ Prompt template generated successfully! ({generation_time:.2f}s)")
            
            # Store in session state for testing
            st.session_state.generated_result = result
            
            # Display the generated prompt
            st.subheader("3. Generated Prompt Template")
            
            # Variables information
            if result.get("variables"):
                st.markdown("**Variables detected:**")
                cols = st.columns(len(result["variables"]))
                for i, var in enumerate(result["variables"]):
                    with cols[i]:
                        st.code(f"{{{var}}}", language="text")
            
            # The actual prompt template
            st.markdown("**Prompt Template:**")
            st.text_area(
                "Generated Prompt",
                value=result["prompt_template"],
                height=400,
                help="This is your generated prompt template. Copy and use it in your AI applications!"
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
            
        except Exception as e:
            st.error(f"❌ Error generating prompt template: {str(e)}")
            logger.error(f"Generation error: {str(e)}")
    
    # Testing section
    if "generated_result" in st.session_state:
        st.markdown("---")
        st.subheader("4. Test Your Prompt Template")
        
        result = st.session_state.generated_result
        
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
                    try:
                        with st.spinner("Testing prompt template..."):
                            test_result = prompt_gen.test_prompt_template(
                                result["prompt_template"], 
                                test_values
                            )
                        
                        st.success("✅ Test completed!")
                        st.markdown("**AI Response:**")
                        st.markdown(test_result)
                        
                    except Exception as e:
                        st.error(f"❌ Error testing prompt: {str(e)}")
                else:
                    st.warning("⚠️ Please provide values for all variables before testing.")
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666;'>"
        "GenAI Prompt Generator v1.0 | Built with Streamlit & LLM Farm"
        "</div>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()