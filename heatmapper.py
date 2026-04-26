import sys
import os
import difflib
from anthropic import Anthropic

def generate_samples(prompt, api_key, num_samples=3):
    """Fakes the Claude API to test the local comparison logic for free."""
    print(f"Generating {num_samples} mock samples... Please wait.")
    
    # We pretend Claude gave two correct answers and one hallucination
    return [
        "The first emperor of Rome was Augustus. He died in 14 AD.",
        "Augustus was the first Roman emperor. He passed away in the year 14 AD.",
        "The first emperor of Rome was Julius Caesar. He died in 44 BC." # Intentional hallucination!
    ]

def build_heatmap(samples):
    """Compares the samples and applies HTML color tags based on consistency."""
    base_text = samples[0]
    comparisons = samples[1:]
    
    # Break the base text into sentences
    sentences = base_text.split('. ')
    heatmapped_output = []

    for sentence in sentences:
        if not sentence.strip():
            continue
            
        match_scores = []
        
        # Compare this sentence against the other generated samples
        for comp_text in comparisons:
            # difflib gives a ratio of similarity between 0.0 and 1.0
            matcher = difflib.SequenceMatcher(None, sentence, comp_text)
            
            # Find the best matching block of text in the comparison sample
            match = matcher.find_longest_match(0, len(sentence), 0, len(comp_text))
            match_ratio = match.size / len(sentence) if len(sentence) > 0 else 0
            match_scores.append(match_ratio)
            
        # Calculate average consistency across all samples
        avg_score = sum(match_scores) / len(match_scores)

        # Apply coloring based on the consistency score
        if avg_score > 0.75:
            # High consistency -> Green
            heatmapped_output.append(f'<span style="color:green">{sentence}.</span>')
        elif avg_score > 0.40:
            # Medium consistency -> Yellow
            heatmapped_output.append(f'<span style="color:#D4AF37">{sentence}.</span>')
        else:
            # Low consistency (Hallucination risk) -> Red
            heatmapped_output.append(f'<span style="color:red"><b>{sentence}.</b></span>')

    return " ".join(heatmapped_output)

if __name__ == "__main__":
    # Ensure arguments are provided
    if len(sys.argv) < 3:
        print("Error: Please provide the prompt and the API key as arguments.")
        sys.exit(1)

    user_prompt = sys.argv[1]
    user_api_key = sys.argv[2]
    
    try:
        # Step 1: Get the varying answers
        generated_samples = generate_samples(user_prompt, user_api_key)
        
        # Step 2: Compare them and generate the HTML heatmap
        final_heatmap = build_heatmap(generated_samples)
        
        # Step 3: Print the result for Claude's UI to render
        print("\n### 🔍 Heatmapper Results\n")
        print("**Legend:** <span style='color:green'>Verified</span> | <span style='color:#D4AF37'>Slight Variations</span> | <span style='color:red'>High Hallucination Risk</span>\n")
        print(final_heatmap)
        
    except Exception as e:
        print(f"An error occurred while running the heatmapper: {e}")