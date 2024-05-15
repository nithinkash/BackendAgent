<h1>BackendAgent</h1>

An Experiment to Replace backend code with Large Language Model and Agents for dynamic backend functionality with automatic infrastructure maintenance.

## About
BackendAgent is an advanced AI tool to Replace your backend Code with the Large Language Model. It can Design backend infrasturtcures like Database, Message Queues, etc. BackendAgent can orchestrate and interact with these infractures in real time raplacing the need of backend code.

> [!IMPORTANT]  
> This project is currently in a very early development/experimental stage. There are a lot of unimplemented/broken features at the moment. Contributions are welcome to help out with the progress!

## Demo

https://github.com/nithinkash/BackendAgent/assets/32903192/0b735385-1369-469a-bf94-0347c6587c6a

## Features

BackendAgent Now supports 
> 1. Groq 
> 2. OpenAI GPT Models
> 3. Ollama Models
> 4. Claud Models

## System Architecture

In the Big Picture, Backend agent has a very simple Architecture. Request from the Frontend is sent to the common API route which is then handed to an Agent. Request is sent to the LLM to Analyze and give the codes that needs to be run on database (or any other backend infra). Agent runs the code and again sends the response back to LLM so that it can format and reafractor the output to send it back to Frontend.

<img width="600" alt="Screenshot 2024-04-19 at 11 28 30 PM" src="https://github.com/nithinkash/BackendAgent/assets/32903192/6c251412-9d8a-4544-8927-7dde873acf1d">

Initially while starting, admin can design the backend infrastructure like database tables, Schema, etc using LLM interface whics is then implemented automatically by agent.  

## Getting Started

```
Version's requirements
  - Python >= 3.9 and < 3.12
  - sqlite3
```
### Installation

To install BackendAgent, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/nithinkash/BackendAgent.git
   ```
2. Navigate to the project directory:
   ```bash
   cd BackendAgent
   ```
3. Create a virtual environment and install the required dependencies (you can use any virtual environment manager):
   ```bash
   uv venv
   
   # On macOS and Linux.
   source .venv/bin/activate

   # On Windows.
   .venv\Scripts\activate

   uv pip install -r requirements.txt
   ```

- For ollama [ollama setup guide](https://ollama.com/) (optinal: if you don't want to use the local models then you can skip this step)
- For API models, configure the API keys via **config.toml**
- Don't forget to set any of these following Base Models
>1. gpt-3.5-turbo
>2. gpt-4-0125-preview
>3. claude-3-haiku-20240307
>4. claude-3-sonnet-20240229
>5. claude-3-opus-20240229

```
> #For Oolama Models please specify installed models in your system, to check the list of installed models use command
> ollama list
```
4. Start the server:
   ```bash
   python BackendAgent.py
   ```
   
### how to use

To start using BackendAgent, follow these steps:
1. First Time starting a server LLM interface Automatically opens up.
2. User can chat with LLM to design Backend Infra (Database for now) and API's.
3. As of now this only supports sqlite3 Database.
4. After Designing the DB, Agent automatically implements them and create required database and tables.
5. Server is started after this inital setup which will be ready for receiving requests.

## Configuration

when you first time run BackendAgent, it will create a `config.toml` file for you in the root directory:

- API KEYS
   - `OPENAI`: Your OpenAI API key for accessing GPT models.
   - `GEMINI`: Your Gemini API key for accessing Gemini models.
   - `CLAUDE`: Your Anthropic API key for accessing Claude models.
   - `MISTRAL`: Your Mistral API key for accessing Mistral models.
   - `GROQ`: Your Groq API key for accessing Groq models.
     
- API ENDPOINTS
   - `OLLAMA`: The Ollama API endpoint for accessing Local LLMs.
   - `OPENAI`: The OpenAI API endpoint for accessing OpenAI models.

Make sure to keep your API keys secure and do not share them publicly
