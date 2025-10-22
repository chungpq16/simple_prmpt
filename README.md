# GenAI Prompt Generator

A powerful Streamlit application that generates custom prompt templates based on user task descriptions. Built with the Metaprompt system and integrated with corporate LLM Farm.

## 🚀 Features

- **AI-Powered Prompt Generation**: Uses advanced metaprompt techniques to create professional prompt templates
- **Corporate LLM Farm Integration**: Seamlessly connects to your corporate LLM infrastructure
- **Interactive Testing**: Test generated prompts with sample inputs before deployment
- **User-Friendly Interface**: Clean, intuitive Streamlit-based UI
- **Variable Detection**: Automatically identifies and extracts necessary variables from prompts
- **Performance Optimized**: Sub-2 second response times for optimal user experience

## 📋 Prerequisites

- Python 3.8 or higher
- Access to Corporate LLM Farm (API key and endpoint URL)
- pip3 package manager

## 🛠️ Installation & Setup

### 1. Clone or Download the Project

```bash
git clone <repository-url>
cd prompt-generator
```

### 2. Automated Setup (Recommended)

The easiest way to get started is using the automated setup script:

```bash
chmod +x run.sh
./run.sh
```

This script will:
- Create a virtual environment
- Install all dependencies
- Set up configuration files
- Launch the application

### 3. Manual Setup

If you prefer manual setup:

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment configuration
cp .env.template .env
```

### 4. Configure Environment Variables

Edit the `.env` file with your LLM Farm credentials:

```env
API_KEY=your_llm_farm_api_key_here
LLM_FARM_URL=your_llm_farm_base_url_here
MODEL_NAME=gpt-4o-mini
LOG_LEVEL=INFO
```

**Required Variables:**
- `API_KEY`: Your LLM Farm API key
- `LLM_FARM_URL`: Base URL for your LLM Farm endpoint (e.g., `https://your-llm-farm.example.com/v1`)

**Optional Variables:**
- `MODEL_NAME`: LLM model to use (default: `gpt-4o-mini`)
- `LOG_LEVEL`: Logging level (default: `INFO`)

## 🎯 Usage Guide

### Starting the Application

```bash
# If using automated script
./run.sh

# Or manually
source venv/bin/activate
streamlit run app.py
```

The application will be available at: `http://localhost:8501`

### Using the Prompt Generator

1. **Describe Your Task**
   - Enter a clear description of what you want the AI to accomplish
   - Examples: "Draft an email responding to a customer complaint", "Rate a resume according to a rubric"

2. **Specify Variables (Optional)**
   - Let the AI automatically detect variables, or
   - Specify custom variables in ALL_CAPS format (e.g., `CUSTOMER_COMPLAINT, COMPANY_NAME`)

3. **Generate Prompt Template**
   - Click "Generate Prompt Template"
   - Wait for the AI to create your custom prompt (typically 1-2 seconds)

4. **Review Generated Prompt**
   - Examine the generated prompt template
   - Note the detected variables
   - Download the prompt for use in your applications

5. **Test Your Prompt (Optional)**
   - Expand the testing section
   - Provide sample values for each variable
   - See how the prompt performs with real inputs

### Example Use Cases

- **Customer Support**: Generate prompts for handling various customer inquiries
- **Content Creation**: Create prompts for writing emails, articles, or marketing copy
- **Data Analysis**: Generate prompts for analyzing and summarizing information
- **Educational**: Create tutoring or explanation prompts
- **Code Review**: Generate prompts for code analysis and feedback

## 🏗️ Architecture

The application consists of several key components:

- **`app.py`**: Main Streamlit application interface
- **`prompt_generator.py`**: Core metaprompt system implementation
- **`llm_client.py`**: LLM Farm integration client
- **`config.py`**: Configuration management
- **`logger.py`**: Logging utilities

### Metaprompt System

The application uses a sophisticated metaprompt system based on multiple example patterns:

1. Customer success agent workflows
2. Binary classification tasks
3. Document analysis with citations
4. Socratic tutoring methodology
5. Function calling patterns

This diverse set of examples enables the generation of high-quality prompts for various use cases.

## ⚡ Performance Requirements

- **Response Time**: < 2 seconds for prompt generation
- **Availability**: Depends on LLM Farm uptime
- **Throughput**: Single-user application designed for interactive use

## 🔧 Configuration Options

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `API_KEY` | LLM Farm API key | - | Yes |
| `LLM_FARM_URL` | LLM Farm endpoint URL | - | Yes |
| `MODEL_NAME` | Model to use | `gpt-4o-mini` | No |
| `LOG_LEVEL` | Logging level | `INFO` | No |
| `MAX_TOKENS` | Max response tokens | `4096` | No |
| `TEMPERATURE` | Model temperature | `0` | No |
| `TIMEOUT_SECONDS` | Request timeout | `30` | No |
| `MAX_RETRIES` | Max retry attempts | `3` | No |

## 🐛 Troubleshooting

### Common Issues

**Connection Errors**
```
Error: LLM Farm connection failed
```
- Verify your `API_KEY` and `LLM_FARM_URL` in `.env`
- Check network connectivity to LLM Farm
- Ensure API key has proper permissions

**Missing Dependencies**
```
ModuleNotFoundError: No module named 'streamlit'
```
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt`

**Configuration Issues**
```
ValueError: API_KEY not found in environment variables
```
- Copy `.env.template` to `.env`
- Fill in required configuration values

### Health Check

Use the built-in health check feature:
1. Open the application
2. Click "Check LLM Farm Connection"
3. Verify the connection status

### Logs

Check application logs for detailed error information:
```bash
# Logs are output to console when running the application
# Adjust LOG_LEVEL in .env for more/less verbose logging
```

## 📝 API Reference

### LLMFarmClient

```python
from llm_client import LLMFarmClient

client = LLMFarmClient(model="gpt-4o-mini")
response = client.completion("Hello", "You are a helpful assistant")
```

### PromptGenerator

```python
from prompt_generator import PromptGenerator

generator = PromptGenerator(llm_client)
result = generator.generate_prompt_template("Draft an email")
```

## 🔒 Security Considerations

- **API Keys**: Store securely in `.env` file, never commit to version control
- **Network**: Ensure secure HTTPS connections to LLM Farm
- **Access Control**: Application runs locally, implement additional auth if needed
- **Data**: Prompts and inputs are sent to LLM Farm - follow your organization's data policies

## 📚 Dependencies

- **streamlit**: Web application framework
- **openai**: LLM Farm API client
- **python-dotenv**: Environment variable management
- **pandas**: Data manipulation utilities
- **requests**: HTTP client library

## 🤝 Contributing

1. Follow the existing code structure and naming conventions
2. Add appropriate error handling and logging
3. Update documentation for any new features
4. Test thoroughly with various prompt types

## 📄 License

This project is designed for internal corporate use with the LLM Farm infrastructure.

## 📞 Support

For technical support or questions:
- Check the troubleshooting section above
- Review application logs for error details
- Contact your LLM Farm administrator for API-related issues

## 🎉 Acknowledgments

Based on the Metaprompt system and concepts from the AI research community. Integrates with corporate LLM Farm infrastructure for enterprise-grade AI capabilities.# simple_prmpt
