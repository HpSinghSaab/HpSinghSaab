import os
import json
import re
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser

class ShortFormRepurposingAgent:
    def __init__(self):
        load_dotenv()
        if not os.getenv("GOOGLE_API_KEY"):
            raise ValueError("GOOGLE_API_KEY not found in .env file")

        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=0.8 # Higher temperature for more creative ideas
        )
        self.prompt_template = self._create_prompt_template()

    def _create_prompt_template(self):
        template = """
        You are a trendy, fast-paced social media manager and an expert in creating viral content for TikTok, Instagram Reels, and YouTube Shorts.
        Your task is to deconstruct the provided long-form YouTube script and create three distinct, high-impact short-form video concepts from it.

        **Long-Form Script:**
        ---
        {long_form_script}
        ---

        **Instructions:**
        1.  Identify the three most powerful moments, surprising facts, or emotional hooks from the long-form script.
        2.  For each hook, write a concise script for a vertical video that is under 60 seconds.
        3.  The scripts MUST be fast-paced and punchy.
        4.  For each script, provide clear and concise visual instructions, including suggestions for on-screen text, quick cuts, and potential trending audio styles (e.g., "upbeat, inspirational background music," "a popular science-explainer audio").

        **Output Format:**
        You MUST provide the output as a single JSON object. This object should contain a single key, "short_form_plans", which is a list of three video plan objects.
        Each video plan object in the list MUST have the following three keys:
        - `Hook`: A short, attention-grabbing sentence that will be the main point of the video.
        - `Concise_Script`: The full script for the short video, including spoken lines.
        - `Visual_Instructions`: A description of the visuals, including on-screen text, B-roll, and audio suggestions.

        **Example JSON Output Structure:**
        {{
          "short_form_plans": [
            {{
              "Hook": "Hook for the first video concept.",
              "Concise_Script": "The script for the first video...",
              "Visual_Instructions": "Visuals for the first video..."
            }},
            {{
              "Hook": "Hook for the second video concept.",
              "Concise_Script": "The script for the second video...",
              "Visual_Instructions": "Visuals for the second video..."
            }},
            {{
              "Hook": "Hook for the third video concept.",
              "Concise_Script": "The script for the third video...",
              "Visual_Instructions": "Visuals for the third video..."
            }}
          ]
        }}

        Do not include any text or explanations outside of this JSON object.
        """
        return ChatPromptTemplate.from_template(template)

    def _clean_json_response(self, response_text):
        match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if match:
            return match.group(0)
        return None

    def create_short_form_plans(self, long_form_script):
        chain = self.prompt_template | self.llm | StrOutputParser()

        response = chain.invoke({"long_form_script": long_form_script})

        cleaned_response = self._clean_json_response(response)

        if cleaned_response:
            return json.dumps(json.loads(cleaned_response), indent=4)
        else:
            raise ValueError("Could not parse JSON from the LLM response.")

if __name__ == '__main__':
    # This is an example of how to run the agent.
    # It requires the output from the ScriptwriterAgent.

    # Example long-form script (pasted from the previous agent's successful run)
    mock_long_form_script = """
== HOOK ==

[Visual: Stunning time-lapse footage of a city skyline transitioning to a vibrant, lush vertical farm nestled amongst the buildings.]

Imagine a future where fresh, locally-grown produce is readily available in the heart of even the busiest metropolis. No more long transportation routes, no more reliance on dwindling farmland.  That future is closer than you think, thanks to the incredible rise of vertical farming.

== INTRODUCTION ==

[Visual:  Title card: "The Rise of Vertical Farming: A Sustainable Solution"]

Hi everyone, and welcome back to the channel! Today, we're diving into a fascinating and increasingly important topic: vertical farming.  It's a revolutionary approach to agriculture that's transforming how we grow food, especially in our rapidly urbanizing world.  We’ll explore how these innovative farms are tackling food security challenges, minimizing environmental impact, and offering a glimpse into the future of food production.

== MAIN BODY ==

[Visual: B-roll footage of various vertical farms, showcasing different designs and technologies.]

**Key Point 1: Addressing Urban Food Security:** Our cities are booming, but arable land is becoming increasingly scarce.  Vertical farms offer a solution by maximizing space utilization.  Instead of sprawling fields, they stack crops vertically, creating a high-yield environment in a fraction of the land area. This means fresh, healthy produce can be grown closer to consumers, reducing transportation costs and emissions, and ensuring a more reliable food supply, especially in densely populated areas.

[Visual: Animated infographic showing the comparison of land usage between traditional farming and vertical farming.]

**Key Point 2: Sustainability and Environmental Benefits:**  Traditional farming often relies heavily on pesticides, herbicides, and vast amounts of water. Vertical farming offers a more sustainable alternative.  Many vertical farms utilize hydroponics or aeroponics, growing plants without soil, which drastically reduces water consumption.  Precise climate control minimizes the need for pesticides, and the controlled environment leads to higher yields with less waste.  This is a huge win for the environment and for our planet's resources.

[Visual:  Footage of a vertical farm showcasing its water recycling system and LED lighting.]

**Key Point 3: Technological Advancements:** Vertical farming isn't just about stacking plants; it's a technologically advanced system.  From sophisticated LED lighting systems that optimize plant growth to automated irrigation and monitoring systems, technology plays a crucial role.  Data analytics and AI are increasingly being used to optimize resource usage and predict potential problems, ensuring maximum efficiency and yield. This constant innovation makes vertical farming a dynamic and ever-evolving field.

[Visual:  Interview with a vertical farmer or expert in the field.]

**Key Point 4: Economic Opportunities and Job Creation:** The rise of vertical farming is also creating new economic opportunities.  From the construction and maintenance of these farms to the development of new technologies and the creation of skilled jobs in agriculture, this industry is generating employment and boosting local economies.  This is particularly important in urban areas where traditional agricultural jobs might be scarce.

[Visual:  Montage of various jobs within a vertical farm setting.]


== CONCLUSION & CALL-TO-ACTION ==

[Visual:  Time-lapse footage of plants growing in a vertical farm, transitioning to a final shot of a diverse range of fresh produce.]

So, there you have it – a glimpse into the fascinating world of vertical farming.  From addressing food security challenges to promoting sustainability and driving technological innovation, vertical farms are reshaping the future of agriculture.  They're not just a trend; they're a crucial part of building a more resilient and sustainable food system for our growing urban populations.

What are your thoughts on vertical farming? Do you think it's the future of food production? Let us know in the comments below!  And don't forget to like this video and subscribe to the channel for more insightful content on trending topics.  Thanks for watching!

[Visual: End screen with social media links and subscription button.]
    """

    agent = ShortFormRepurposingAgent()
    short_form_plans_json = agent.create_short_form_plans(mock_long_form_script)

    print("--- GENERATED SHORT-FORM PLANS ---")
    print(short_form_plans_json)
    print("\n--- END OF PLANS ---")

    # Verification check
    try:
        data = json.loads(short_form_plans_json)
        if "short_form_plans" in data and len(data["short_form_plans"]) == 3:
            print("\nVerification successful: JSON is valid and contains 3 plans.")
        else:
            print("\nVerification failed: JSON structure is incorrect.")
    except json.JSONDecodeError:
        print("\nVerification failed: Output is not valid JSON.")
