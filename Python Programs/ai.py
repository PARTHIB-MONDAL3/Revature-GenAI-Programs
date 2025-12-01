from transformers import pipeline

# Initialize the text-generation pipeline with GPT-2
gen = pipeline("text-generation", model="gpt2")

# Get topic from user
topic = input("Enter the topic: ")

# Generate a better prompt based on the topic
better_prompt_result = gen(
    "Generate a better prompt for the topic: " + topic,
    max_new_tokens=200,
    do_sample=True,
    top_p=0.9,
    temperature=0.8
)

better_prompt = better_prompt_result[0]["generated_text"]
print("Better Prompt:\n", better_prompt)

# Generate final result using the better prompt
final_result = gen(
    better_prompt,
    max_new_tokens=400,
    do_sample=True,
    top_p=0.9,
    temperature=0.8
)

print("\nGenerated Text:\n", final_result[0]["generated_text"])
