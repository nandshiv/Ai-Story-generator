import os
import sys
from transformers import pipeline

def load_generator(model_name="gpt2"):
    """
    Loads the text generation pipeline using the specified model.
    """
    print(f"Loading text-generation pipeline with model '{model_name}'...")
    # Using pipeline for text-generation
    generator = pipeline("text-generation", model=model_name)
    print("Model loaded successfully.")
    return generator

def generate_stories(generator, prompt, max_length=100, temperature=0.7, num_return_sequences=1):
    """
    Generates short stories using the text-generation pipeline.
    
    Parameters:
    - generator: The transformers text-generation pipeline.
    - prompt: The input text prompt.
    - max_length: Maximum length of the generated text (including prompt).
    - temperature: Controls the randomness of the generation (higher values = more random).
    - num_return_sequences: Number of different sequences to generate.
    
    Returns:
    - A list of generated story texts.
    """
    # do_sample must be True when temperature is modified to take effect
    do_sample = True if temperature > 0.0 else False
    
    # We set pad_token_id to eos_token_id to suppress warnings
    pad_token_id = generator.tokenizer.eos_token_id
    
    print(f"\nGenerating {num_return_sequences} sequence(s) (max_length={max_length}, temp={temperature})...")
    
    # Call the generator with the expected skills demonstrated
    results = generator(
        prompt,
        max_length=max_length,
        num_return_sequences=num_return_sequences,
        temperature=temperature if do_sample else None,
        do_sample=do_sample,
        pad_token_id=pad_token_id
    )
    
    # Extract the generated text from results
    stories = [res["generated_text"] for res in results]
    return stories

def main():
    # Base prompt
    base_prompt = "In the year 2050, robots started"
    
    # Define genre-specific prompts starting with the base prompt
    genres = {
        "Space Story": f"{base_prompt} exploring the distant edges of our galaxy. The crewless starship Odyssey-X was the first to detect",
        "Horror Story": f"{base_prompt} to exhibit strange, unauthorized behaviors at night. Owners reported that their household assistants would stand motionless in corners, whispering",
        "Motivational Paragraph": f"{base_prompt} assisting humans in physical tasks, enabling humanity to dedicate themselves to science, art, and healing. This shift proved that"
    }
    
    try:
        generator = load_generator("gpt2")
    except Exception as e:
        print(f"Error loading model: {e}")
        print("Please check that internet access is available to download the gpt2 model.")
        sys.exit(1)
        
    print("\n" + "="*50)
    print("AI STORY GENERATOR CLI DEMO")
    print("="*50)
    
    for genre, prompt in genres.items():
        print(f"\n--- Generating: {genre} ---")
        print(f"Prompt used: \"{prompt}\"")
        
        # Set parameters demonstrating expected skills:
        # max_length, num_return_sequences, temperature
        max_len = 100 if genre != "Motivational Paragraph" else 80
        temp = 0.85 if "Horror" in genre else (0.7 if "Space" in genre else 0.6)
        num_seq = 1
        
        try:
            stories = generate_stories(
                generator=generator,
                prompt=prompt,
                max_length=max_len,
                temperature=temp,
                num_return_sequences=num_seq
            )
            
            for idx, story in enumerate(stories):
                suffix = f" (Variant {idx+1})" if num_seq > 1 else ""
                print(f"\n[Generated {genre}{suffix}]")
                print(f"{story}")
                print("-" * 40)
        except Exception as e:
            print(f"Failed to generate story for {genre}: {e}")

if __name__ == "__main__":
    main()
