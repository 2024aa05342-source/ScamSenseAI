from transformers import pipeline
import torch

print("Loading LLM...")

generator = pipeline(
    "text-generation",
    model="Qwen/Qwen2.5-3B-Instruct",
    torch_dtype=torch.float16,
    device_map="auto"
)

print("LLM Loaded")

def generate_response(prompt):

    response = generator(
        prompt,
        max_new_tokens=400,
        do_sample=False
    )

    generated = response[0]["generated_text"]

    if generated.startswith(prompt):
        generated = generated[len(prompt):]

    generated = generated.replace("```json", "")
    generated = generated.replace("```", "")
    generated = generated.strip()

    return generated
