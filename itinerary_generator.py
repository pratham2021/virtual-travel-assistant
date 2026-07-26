# new: the actual Claude API call
import os
from anthropic import Anthropic
from dotenv import load_dotenv
from input_schema import Preference, solo_backpacker, family_of_four, couple_luxury 
from output_schema import Itinerary
from prompts import SYSTEM_PROMPT

load_dotenv() # Load variables from the .env file into the environment

secret = os.getenv("ANTHROPIC_API_KEY")

client = Anthropic(api_key=secret)

def generate_itinerary(preference: Preference) -> Itinerary:
    preference_json_string = preference.model_dump_json()
    
    # passing our json string off to the model and returns the accumulated message object returned from the stream after it has been read to completion
    with client.messages.stream(model="claude-sonnet-5", max_tokens=24000, system=SYSTEM_PROMPT, messages=[{"role": "user", "content": preference_json_string}]) as stream:
        response = stream.get_final_message()
    
    # Clean raw output string 
    text_block = next((block.text for block in response.content if block.type == 'text'), "")
    text_block = text_block.strip()
    if text_block.startswith("```"):
        position = text_block.find("\n")
        text_block = text_block[position+1:]
    if text_block.endswith("```"):
        text_block = text_block[:-3]
    text_block = text_block.strip()
    return Itinerary.model_validate_json(text_block) # the validated Itinerary object

if __name__ == "__main__":
  # solo_backpacker_itinerary = generate_itinerary(solo_backpacker)
  # print(solo_backpacker_itinerary)

  # family_itinerary = generate_itinerary(family_of_four)
  # print(family_itinerary)
  
  # couple_itinerary = generate_itinerary(couple_luxury)
  # print(couple_itinerary)
  pass