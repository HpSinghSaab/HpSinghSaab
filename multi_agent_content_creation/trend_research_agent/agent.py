import os
import json
from dotenv import load_dotenv
from pytrends.request import TrendReq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser

class TrendResearchAgent:
    def __init__(self):
        load_dotenv()
        if not os.getenv("GOOGLE_API_KEY"):
            raise ValueError("GOOGLE_API_KEY not found in .env file")

        self.pytrends = TrendReq(hl='en-US', tz=360)
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )
        self.summary_prompt = ChatPromptTemplate.from_template(
            "You are a helpful research assistant. Write a very brief, one-sentence summary for the following trending topic: '{topic}'. This summary should be neutral and descriptive."
        )
        self.summary_chain = self.summary_prompt | self.llm | StrOutputParser()

    def research_trends(self):
        """
        Fetches trending topics from Google Trends and enriches them with an AI-generated summary.
        """
        print("Fetching trending searches from Google Trends...")
        try:
            # Get daily trending searches for the US
            df = self.pytrends.trending_searches(pn='united_states')
            topics = df[0].tolist()
            print(f"Found {len(topics)} trending topics.")
        except Exception as e:
            print(f"Error fetching trends from pytrends: {e}")
            # Fallback to a few generic topics if the API fails
            topics = ["Artificial Intelligence", "Climate Change", "Electric Vehicles", "Global Economy"]

        # Limit to the top 20 topics as required by the pipeline
        top_20_topics = topics[:20]

        enriched_topics = []
        print(f"Enriching top {len(top_20_topics)} topics with AI summaries...")

        for topic_name in top_20_topics:
            print(f"  - Processing: {topic_name}")
            try:
                # Generate a brief summary using the LLM
                brief_summary = self.summary_chain.invoke({"topic": topic_name})

                # Create the topic object
                topic_object = {
                    "topic_name": topic_name,
                    "brief_summary": brief_summary.strip(),
                    "keywords": [kw.strip() for kw in topic_name.split()],
                    "source_urls": [f"https://www.google.com/search?q={topic_name.replace(' ', '+')}"]
                }
                enriched_topics.append(topic_object)
            except Exception as e:
                print(f"    - Error generating summary for '{topic_name}': {e}")
                # If summary fails, we can skip or add a placeholder
                continue

        return json.dumps(enriched_topics, indent=4)

if __name__ == '__main__':
    agent = TrendResearchAgent()
    trending_topics_json = agent.research_trends()

    print("\n--- GENERATED TRENDING TOPICS ---")
    print(trending_topics_json)

    # Verification check
    try:
        data = json.loads(trending_topics_json)
        if isinstance(data, list) and len(data) > 0 and "topic_name" in data[0]:
            print(f"\nVerification successful: JSON is valid and contains {len(data)} topics.")
        else:
            print("\nVerification failed: JSON structure is incorrect.")
    except (json.JSONDecodeError, IndexError):
        print("\nVerification failed: Output is not valid JSON or is empty.")
