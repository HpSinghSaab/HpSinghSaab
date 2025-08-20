import json
import os
import shutil

# Import all agent classes
from trend_research_agent.agent import TrendResearchAgent
from content_strategist_agent.agent import ContentStrategistAgent
from scriptwriter_agent.agent import ScriptwriterAgent
from short_form_repurposing_agent.agent import ShortFormRepurposingAgent
from multimedia_production_agent.agent import MultimediaProductionAgent

def main():
    """
    Main function to orchestrate the multi-agent content creation pipeline.
    """
    print("--- STARTING MULTI-AGENT CONTENT CREATION PIPELINE ---")

    # 1. Instantiate all agents
    print("\n[1/5] Instantiating agents...")
    try:
        trend_agent = TrendResearchAgent()
        strategist_agent = ContentStrategistAgent()
        scriptwriter_agent = ScriptwriterAgent()
        repurposing_agent = ShortFormRepurposingAgent()
        production_agent = MultimediaProductionAgent(output_dir="final_content_package")
        print("  - Agents instantiated successfully.")
    except Exception as e:
        print(f"  - ERROR: Failed to instantiate agents. Have you set up the .env file correctly? Error: {e}")
        return

    # 2. Run Trend Research Agent
    print("\n[2/5] Running Trend Research Agent...")
    # NOTE: This agent uses a mock implementation as we don't have a NewsAPI key.
    trending_topics_json = trend_agent.research_trends()
    print("  - Trend Research Agent finished. Found 20 mock topics.")
    # print(trending_topics_json) # Optional: print the full list

    # 3. Run Content Strategist Agent
    print("\n[3/5] Running Content Strategist Agent...")
    try:
        top_10_topics_json = strategist_agent.select_top_topics(trending_topics_json)
        print("  - Content Strategist finished. Selected top 10 topics.")
        # print(top_10_topics_json) # Optional: print the top 10
    except Exception as e:
        print(f"  - ERROR: Content Strategist Agent failed. This is likely an API key or model issue. Error: {e}")
        return

    # 4. Select the top topic and run the scriptwriting agents
    top_topics = json.loads(top_10_topics_json)
    if not top_topics:
        print("  - No topics were selected by the strategist. Exiting.")
        return

    top_topic = top_topics[0]
    top_topic_name = top_topic.get("topic_name", "Untitled_Topic")
    print(f"\n--- Processing top topic: '{top_topic_name}' ---")

    # 5. Run Scriptwriter Agent
    print("\n[4/5] Running Scriptwriter and Repurposing Agents...")
    try:
        long_form_script = scriptwriter_agent.write_script(json.dumps(top_topic))
        print("  - Scriptwriter Agent finished. Generated long-form script.")

        # 6. Run Short-Form Repurposing Agent
        # Note: We wrap this in a try-except because it can fail on long inputs
        try:
            short_form_plans_json = repurposing_agent.create_short_form_plans(long_form_script)
            print("  - Short-Form Repurposing Agent finished. Generated 3 short-form plans.")
        except Exception as e:
            print(f"  - WARNING: Short-Form Repurposing Agent failed. This might be due to a long input script. Error: {e}")
            print("  - Proceeding with an empty list of short-form plans.")
            short_form_plans_json = json.dumps({"short_form_plans": []})

    except Exception as e:
        print(f"  - ERROR: A scriptwriting agent failed. Error: {e}")
        return

    # 7. Run Multimedia Production Agent
    print("\n[5/5] Running Multimedia Production Agent...")
    try:
        final_files = production_agent.produce_multimedia_package(
            top_topic_name,
            long_form_script,
            short_form_plans_json
        )
        print("  - Multimedia Production Agent finished.")
        print(f"  - Final assets are located in the '{production_agent.output_dir}' directory.")
        print(f"  - Files created: {final_files}")
    except Exception as e:
        print(f"  - ERROR: Multimedia Production Agent failed. Error: {e}")
        return

    print("\n--- MULTI-AGENT CONTENT CREATION PIPELINE FINISHED SUCCESSFULLY ---")


if __name__ == '__main__':
    # Clean up previous output directory if it exists
    if os.path.exists("final_content_package"):
        print("Removing previous output directory...")
        shutil.rmtree("final_content_package")

    main()
