# Multi-Agent AI System for Automated Content Creation

## 1. Overview

This project is a multi-agent AI system designed for automated, daily content creation. It leverages a sequence of specialized AI agents to research trending topics, strategize content, write scripts, and produce multimedia assets.

The system is built in Python and uses the LangChain framework to interact with Google's Gemini large language models for AI-powered tasks.

## 2. Project Structure

The project is organized into a modular structure, with each agent residing in its own directory.

-   `/main.py`: The main orchestration script that runs the entire pipeline from start to finish.
-   `/requirements.txt`: A list of all necessary Python dependencies.
-   `/.env`: A file to store the necessary API keys (you will need to create this).
-   `/trend_research_agent/`: **Agent 1:** Scans for trending topics. (Currently uses a mock implementation).
-   `/content_strategist_agent/`: **Agent 2:** Analyzes and selects the top topics using an LLM.
-   `/scriptwriter_agent/`: **Agent 3:** Writes a long-form YouTube script for the top topic.
-   `/short_form_repurposing_agent/`: **Agent 4:** Creates three short-form video concepts from the long-form script.
-   `/multimedia_production_agent/`: **Agent 5:** Generates `.mp3` voice-overs and `.txt` video plans (shot lists).
-   `/final_content_package/`: The output directory where the final assets are saved.

## 3. Setup and Installation

**Step 1: Create a Virtual Environment**
It is highly recommended to run this project in a Python virtual environment.

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

**Step 2: Install Dependencies**
Install all the required packages using the `requirements.txt` file.

```bash
pip install -r requirements.txt
```
*Note: The initial installation of all dependencies might take a few minutes.*

**Step 3: Set up API Keys**
This project requires API keys for Google's AI services.

1.  Create a file named `.env` in the root of the `multi_agent_content_creation` directory.
2.  Add your API key to the file in the following format:

    ```
    # Required for Agents 2, 3, and 4
    GOOGLE_API_KEY="YOUR_GEMINI_API_KEY_HERE"

    # Optional for Agent 1 (currently mocked)
    NEWS_API_KEY="YOUR_NEWS_API_KEY_HERE"
    ```

You can get a Google Gemini API key from [Google AI Studio](https://ai.google.dev/gemini-api/docs/api-key).

## 4. How to Run

To run the entire content creation pipeline, simply execute the `main.py` script from the root of the `multi_agent_content_creation` directory:

```bash
python main.py
```

The script will print status updates as it progresses through each agent. The final output files will be saved in the `final_content_package` directory.

## 5. Agent Descriptions

-   **Agent 1: Trend Research Agent:** Identifies emerging trends. *Note: The current implementation is a mock and provides a static list of topics. To enable real-time trend research, you would need to implement the API calls for services like Google Trends and NewsAPI.*
-   **Agent 2: Content Strategist Agent:** Evaluates the list of topics and selects the top 10 with the highest potential, adding a strategic angle for content creation.
-   **Agent 3: Scriptwriter Agent (Long-Form):** Takes the top-ranked topic and generates a detailed, 8-10 minute YouTube video script.
-   **Agent 4: Short-Form Repurposing Agent:** Deconstructs the long-form script to create three distinct, high-impact short-form video concepts.
-   **Agent 5: Multimedia Production Agent:** Generates `.mp3` voice-overs for all four scripts and creates text-based "shot list" files containing the visual cues for video editing.
