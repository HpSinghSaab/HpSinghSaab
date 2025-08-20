import os
import json
import re
from gtts import gTTS

class MultimediaProductionAgent:
    def __init__(self, output_dir="output_package"):
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def _clean_text_for_tts(self, text):
        """Removes visual cues and other script annotations for cleaner audio."""
        # Remove visual cues like [Visual: ...] or [B-roll: ...]
        text = re.sub(r'\[.*?\]', '', text)
        # Remove section headings like == HOOK ==
        text = re.sub(r'==.*?==', '', text)
        # Replace newlines and multiple spaces for better flow
        return ' '.join(text.split())

    def _extract_visual_cues(self, text):
        """Extracts all visual cues from a script."""
        cues = re.findall(r'(\[.*?\])', text)
        return '\n'.join(cues) if cues else "No visual cues found in script."

    def produce_multimedia_package(self, topic_name, long_form_script, short_form_plans_json):
        """
        Generates a package of multimedia assets: 4 audio files and 4 video plan files.
        """
        print(f"Starting multimedia production for topic: {topic_name}")

        # Sanitize topic_name for use in filenames
        safe_topic_name = re.sub(r'\W+', '_', topic_name).lower()

        # 1. Process Long-Form Script
        print("Processing long-form script...")
        # Generate audio
        long_form_text = self._clean_text_for_tts(long_form_script)
        long_form_audio_path = os.path.join(self.output_dir, f"{safe_topic_name}_longform.mp3")
        tts = gTTS(text=long_form_text, lang='en', slow=False)
        tts.save(long_form_audio_path)
        print(f"  - Saved long-form audio to: {long_form_audio_path}")

        # Generate video plan
        long_form_visuals = self._extract_visual_cues(long_form_script)
        long_form_plan_path = os.path.join(self.output_dir, f"{safe_topic_name}_longform_video_plan.txt")
        with open(long_form_plan_path, 'w') as f:
            f.write(long_form_visuals)
        print(f"  - Saved long-form video plan to: {long_form_plan_path}")

        # 2. Process Short-Form Scripts
        print("Processing short-form scripts...")
        short_form_plans = json.loads(short_form_plans_json)["short_form_plans"]

        for i, plan in enumerate(short_form_plans):
            hook_name = re.sub(r'\W+', '_', plan['Hook']).lower()[:30] # Short, safe name from the hook
            print(f"  - Processing short-form plan {i+1} ('{hook_name}')...")

            # Generate audio
            short_form_text = self._clean_text_for_tts(plan['Concise_Script'])
            short_form_audio_path = os.path.join(self.output_dir, f"{safe_topic_name}_short_{i+1}_{hook_name}.mp3")
            tts = gTTS(text=short_form_text, lang='en')
            tts.save(short_form_audio_path)
            print(f"    - Saved short-form audio to: {short_form_audio_path}")

            # Generate video plan (using the pre-made visual instructions)
            short_form_plan_path = os.path.join(self.output_dir, f"{safe_topic_name}_short_{i+1}_{hook_name}_video_plan.txt")
            with open(short_form_plan_path, 'w') as f:
                f.write(plan['Visual_Instructions'])
            print(f"    - Saved short-form video plan to: {short_form_plan_path}")

        print("\nMultimedia package production complete.")
        return os.listdir(self.output_dir)


if __name__ == '__main__':
    # This is an example of how to run the agent.
    # It requires outputs from the previous agents.

    # Mock inputs
    mock_topic_name = "The Rise of Vertical Farming"

    mock_long_form_script = """
== HOOK ==
[Visual: Stunning time-lapse footage of a city skyline transitioning to a vibrant, lush vertical farm nestled amongst the buildings.]
Imagine a future where fresh, locally-grown produce is readily available...
    """ # Abridged for brevity

    mock_short_form_plans_json = """
{
    "short_form_plans": [
        {
            "Hook": "Forget farms, the future of food is VERTICAL!",
            "Concise_Script": "Imagine fresh produce, grown right in your city! Vertical farms are revolutionizing food production.",
            "Visual_Instructions": "Open on a stunning time-lapse of a city skyline. Quick cuts of vegetables growing. Text overlay: 'Vertical Farming: The Future of Food'."
        },
        {
            "Hook": "Solving Food Security? Vertical Farms are crushing it!",
            "Concise_Script": "Food security is a HUGE issue, but vertical farms are providing a solution!",
            "Visual_Instructions": "Start with a statistic about food insecurity. Show quick cuts of people harvesting produce."
        },
        {
            "Hook": "This is how we'll feed 9 billion people!",
            "Concise_Script": "Our planet's population is booming! How do we feed everyone sustainably? Vertical farming!",
            "Visual_Instructions": "Open with a graphic showing projected population growth. Show diverse shots of various vertical farms."
        }
    ]
}
    """

    agent = MultimediaProductionAgent()
    final_files = agent.produce_multimedia_package(
        mock_topic_name,
        mock_long_form_script,
        mock_short_form_plans_json
    )

    print("\n--- FINAL FILES GENERATED ---")
    for filename in final_files:
        print(filename)

    # Verification check
    if len(final_files) == 8: # 4 audio, 4 text
        print("\nVerification successful: Correct number of files (8) generated.")
    else:
        print(f"\nVerification failed: Incorrect number of files generated ({len(final_files)}).")
