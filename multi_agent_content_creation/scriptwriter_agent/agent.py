import os
import json
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser

class ScriptwriterAgent:
    def __init__(self):
        load_dotenv()
        if not os.getenv("GOOGLE_API_KEY"):
            raise ValueError("GOOGLE_API_KEY not found in .env file")

        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=0.7 # Add some creativity
        )
        self.prompt_template = self._create_prompt_template()

    def _create_prompt_template(self):
        template = """
        You are a professional scriptwriter and storyteller, specializing in creating engaging and educational video scripts for a YouTube channel that covers trending topics.
        Your task is to write a detailed 8-10 minute video script based on the provided topic information. An 8-10 minute script is typically between 1200 and 1500 words.

        **Topic Information:**
        - **Topic Name:** {topic_name}
        - **Brief Summary:** {brief_summary}
        - **Strategic Angle:** {strategic_angle}

        **Script Requirements:**
        1.  **Tone:** Conversational, accessible, and highly engaging for a broad audience.
        2.  **Structure:** The script MUST be clearly divided into the following sections using the specified headings:
            - `== HOOK ==`
            - `== INTRODUCTION ==`
            - `== MAIN BODY ==`
            - `== CONCLUSION & CALL-TO-ACTION ==`
        3.  **Hook:** Start with a powerful opening hook based on the `strategic_angle` that grabs the viewer's attention within the first 15 seconds.
        4.  **Main Body:** Expand on the topic with 3-4 distinct key points. Use the summary as a starting point, but feel free to research and add more details to create a comprehensive narrative.
        5.  **Visual Cues:** Intersperse the script with visual cues for the video editor. These cues should be on their own line and formatted as `[Visual: Description of the visual element]`. Examples: `[Visual: Animated graph showing the rise of vertical farming]`, `[B-roll: Footage of a bustling city]`.
        6.  **Conclusion:** Summarize the key points and end with a compelling call-to-action (e.g., asking viewers to comment with their thoughts, subscribe to the channel, etc.).

        Produce only the script content, starting with the `== HOOK ==` section. Do not include any other explanatory text before or after the script itself.
        """
        return ChatPromptTemplate.from_template(template)

    def write_script(self, topic_json):
        """
        Takes a JSON object for a single topic and generates a video script.
        """
        topic_data = json.loads(topic_json)

        chain = self.prompt_template | self.llm | StrOutputParser()

        script = chain.invoke({
            "topic_name": topic_data["topic_name"],
            "brief_summary": topic_data["brief_summary"],
            "strategic_angle": topic_data["strategic_angle"]
        })

        return script

if __name__ == '__main__':
    # This is an example of how to run the agent.
    # It requires a single topic object from the ContentStrategistAgent.

    # Example input topic
    mock_topic_json = json.dumps({
        "topic_name": "The Rise of Vertical Farming",
        "brief_summary": "How vertical farms are changing agriculture in urban areas, offering a sustainable solution to food security.",
        "keywords": ["Vertical Farming", "Agriculture", "Sustainability"],
        "source_urls": ["https://example.com/vf-1", "https://example.com/vf-2"],
        "strategic_angle": "Vertical farming offers a sustainable solution to food security in urban areas, a compelling narrative for environmentally conscious audiences and a visually stunning glimpse into the future of agriculture.",
        "justification_score": 88
    })

    agent = ScriptwriterAgent()
    video_script = agent.write_script(mock_topic_json)

    print("--- GENERATED SCRIPT ---")
    print(video_script)
    print("\n--- END OF SCRIPT ---")

    # Verification check
    if "== HOOK ==" in video_script and "[Visual:" in video_script:
        print("\nVerification successful: Script contains required structural elements.")
    else:
        print("\nVerification failed: Script is missing required structural elements.")
