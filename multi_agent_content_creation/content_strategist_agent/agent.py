import os
import json
import re
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser

class ContentStrategistAgent:
    def __init__(self):
        load_dotenv()
        # Check if the API key is available
        if not os.getenv("GOOGLE_API_KEY"):
            raise ValueError("GOOGLE_API_KEY not found in .env file")

        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )
        self.prompt_template = self._create_prompt_template()

    def _create_prompt_template(self):
        template = """
        You are an expert content strategist and viral marketing consultant.
        Your task is to analyze a trending topic and evaluate its potential for creating compelling, multi-platform content.

        Topic Information:
        - Topic Name: {topic_name}
        - Brief Summary: {brief_summary}
        - Keywords: {keywords}

        Please evaluate this topic based on the following criteria and provide a score from 1 to 100 for each:
        1.  **Virality Potential**: How likely is this to get shared? (Emotional hook, controversy, novelty)
        2.  **Narrative Depth**: Can a compelling story be told around this?
        3.  **Visual Potential**: Can this be easily translated into engaging video content?

        Based on your analysis, provide the following in a JSON format:
        1.  A `strategic_angle`: A one-sentence hook for why this topic is compelling.
        2.  A `justification_score`: An overall score (average of the three criteria) from 1 to 100, representing its content potential.

        Your output MUST be a JSON object with the keys "strategic_angle" and "justification_score".
        Example:
        {{
            "strategic_angle": "This topic has a strong emotional hook and is perfect for a short, impactful video.",
            "justification_score": 85
        }}

        Do not include any other text or explanation outside of the JSON object.
        """
        return ChatPromptTemplate.from_template(template)

    def _clean_json_response(self, response_text):
        """
        Cleans the LLM response to extract a valid JSON object.
        """
        # Use a regex to find the JSON object within the response
        match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if match:
            return match.group(0)
        return None

    def select_top_topics(self, trending_topics_json):
        topics = json.loads(trending_topics_json)

        analyzed_topics = []
        chain = self.prompt_template | self.llm | StrOutputParser()

        for topic in topics:
            try:
                response = chain.invoke({
                    "topic_name": topic["topic_name"],
                    "brief_summary": topic["brief_summary"],
                    "keywords": ", ".join(topic["keywords"])
                })

                # Clean the response to get a valid JSON
                cleaned_response = self._clean_json_response(response)

                if cleaned_response:
                    analysis = json.loads(cleaned_response)
                    topic['strategic_angle'] = analysis.get('strategic_angle', 'N/A')
                    topic['justification_score'] = analysis.get('justification_score', 0)
                else:
                    topic['strategic_angle'] = 'Error in analysis'
                    topic['justification_score'] = 0

            except Exception as e:
                print(f"An error occurred while analyzing topic '{topic['topic_name']}': {e}")
                topic['strategic_angle'] = 'Error in analysis'
                topic['justification_score'] = 0

            analyzed_topics.append(topic)

        # Sort by the justification_score and take the top 10
        ranked_topics = sorted(analyzed_topics, key=lambda x: x.get('justification_score', 0), reverse=True)
        top_10_topics = ranked_topics[:10]

        return json.dumps(top_10_topics, indent=4)

if __name__ == '__main__':
    # This is an example of how to run the agent.
    # It requires the output from the TrendResearchAgent.

    # Example input from TrendResearchAgent (using the mock data structure)
    mock_input_json = json.dumps([
        {
            "topic_name": "The Future of Quantum Computing",
            "brief_summary": "Recent breakthroughs in quantum computing are promising a new era of technology.",
            "keywords": ["Quantum Computing", "Technology", "Science"],
            "source_urls": ["https://example.com/qc-1", "https://example.com/qc-2"]
        },
        {
            "topic_name": "The Rise of Vertical Farming",
            "brief_summary": "How vertical farms are changing agriculture in urban areas.",
            "keywords": ["Vertical Farming", "Agriculture", "Sustainability"],
            "source_urls": ["https://example.com/vf-1", "https://example.com/vf-2"]
        }
    ] * 10) # Simulating 20 topics

    agent = ContentStrategistAgent()
    top_10_topics_json = agent.select_top_topics(mock_input_json)
    print(top_10_topics_json)
