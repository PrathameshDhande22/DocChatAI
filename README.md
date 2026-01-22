# DocChatAI - Intelligent Document Question Answering System

**DocChatAI** is a privacy-focused, AI-powered document chat application that allows users to upload documents and interact with their content using advanced **Retrieval-Augmented Generation (RAG)** workflows built with **LangGraph**.

All documents, embeddings, and vector data are stored locally on the filesystem, giving users full control over their data.

![LangChain](https://img.shields.io/badge/langchain-%231C3C3C.svg?style=for-the-badge&logo=langchain&logoColor=white)
![HuggingFace](https://img.shields.io/badge/huggingface-%23FFD21E.svg?style=for-the-badge&logo=huggingface&logoColor=black)
![LangGraph](https://img.shields.io/badge/langgraph-%231C3C3C.svg?style=for-the-badge&logo=langgraph&logoColor=white)
![Google Gemini](https://img.shields.io/badge/google%20gemini-8E75B2?style=for-the-badge&logo=google%20gemini&logoColor=white)
![Mistral AI](https://img.shields.io/badge/mistral%20ai-FF6F00?style=for-the-badge&logo=mistralai&logoColor=white)
![OpenAI](https://img.shields.io/badge/openai-000000?style=for-the-badge&logo=openai&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![uv](https://img.shields.io/badge/uv-%23DE5FE9.svg?style=for-the-badge&logo=uv&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-%23FE4B4B.svg?style=for-the-badge&logo=streamlit&logoColor=white)
![ChromaDB](https://img.shields.io/badge/chromadb-5A3EE6?style=for-the-badge&logo=chromadb&logoColor=white)

> [!NOTE]
> This project represents my first hands-on implementation using *LangGraph* and *LangChain* integrated with Hugging Face models.

### Objective: 
In this project, you need to:

- Enable users to upload PDF documents through a web interface
- Process and store document content in a searchable vector database
- Allow users to ask natural language questions about the PDFs
- Retrieve the most relevant document chunks for each query
- Generate accurate, context-aware answers using a language model
- Maintain conversational context across multiple user queries

### Workflow:

1. User uploads one or more PDF files
2. User clicks a process button
3. Documents are loaded, split, and embedded
4. Embeddings are stored in a vector database
5. User asks a question
6. Relevant document chunks are retrieved
7. The language model generates a context-based answer
8. Conversation history is updated and displayed

## Technology Stack:
1. Python 3.12
2. Langchain 
3. Langgraph
4. Chromadb
5. Embeddings
6. Google Gemini
7. StreamLit
8. Mistral
9. HuggingFace


### Multi-LLM Provider Support

**DocChatAI** supports chatting with multiple LLM providers, giving users flexibility in performance, cost, and deployment:
- ChatGPT OSS 120B
- Gemini 2.5 Flash
- Mistral 3 Large
- Qwen 3 (1B) – running locally for fully offline usage

Users can switch between models seamlessly while keeping the same document knowledge base.

## Architecture:
![arhitecture](./Images/docchatai_architecture.png)

#### Langgraph Contains the Follwing Nodes:
- **START** – Entry point of the graph where the user query is received.
- **QUERY_OR_RESPOND** – Decides whether the user query can be answered directly or requires document retrieval.
- **TOOLS** – Executes retrieval and utility tools to fetch relevant document context and metadata.
- **GRADE_DOCUMENTS** – Evaluates the relevance and quality of retrieved documents for the given query.
- **REWRITE_QUESTION** – Refines the user query to improve retrieval when documents are insufficient.
- **GENERATE_ANSWER** – Generates the final answer grounded in the validated document context.
- **END** – Terminates the graph and returns the final response to the user.

## Setup 

Follow the steps below to set up **DocChatAI** on your local machine.

1. Install [Python](https://www.python.org/downloads/release/python-3120/) and [UV](https://docs.astral.sh/uv/getting-started/installation/). 
2. CUDA Requirement (Recommended)
    - Ensure CUDA is installed if you plan to run models on the GPU
    - CUDA is required for GPU-accelerated PyTorch operations
    ```bash
    nvidia-smi
    ```
3. CPU-Only Setup (No CUDA)
    If CUDA is not installed or you want to run on CPU only:
    - Open `pyproject.toml`
    - Remove or comment out the CUDA-specific torch sources
4. GPU Setup (Optional but Recommended)
    If your system has a supported NVIDIA GPU:
    - Install the [CUDA Toolkit](https://developer.nvidia.com/cuda-13-0-0-download-archive) compatible with your GPU
    - Ensure CUDA and drivers are properly configured before installing dependencies
5. Install Project Dependencies:
    ```bash
    uv pip install -r pyproject.toml
    ```
    If you face error while installing dependency make sure you have installed the correct python version and CUDA Toolkit Driver.
6. Environment Variables Setup
    - Create a .env file in the project root
    - Copy all contents from .env.example
    - Add your own API keys
    ```.env
    GOOGLE_API_KEY=<your-gemini-api-key>
    LANGSMITH_API_KEY=<langsmith-api-key>
    LANGSMITH_TRACING=True
    LANGSMITH_PROJECT=<projectname>
    LANGSMITH_ENDPOINT=https://api.smith.langchain.com
    MISTRAL_API_KEY=<your-mistral-api-key>
    GROQ_API_KEY=<your-groq-api-key>
    ```
7. Run the Application
   ```bash
   streamlit run src/app.py
   ```

### Langgraph Development Server
If you plan to run the LangGraph development server directly:
- Ensure all imports inside your graph and node files use absolute and compatible paths
- Relative imports may cause issues when running langgraph dev
- Start the LangGraph dev server with:
    ```bash
    langgraph dev
    ```



## License
This project is licensed under the MIT License.