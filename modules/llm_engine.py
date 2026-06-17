from transformers import pipeline
import torch
import time

print("Loading LLM...")

generator = pipeline(
    "text-generation",
    model="Qwen/Qwen2.5-3B-Instruct",
    torch_dtype=torch.float16,
    device_map="auto"
)

print("LLM Loaded")

def generate_response(prompt):

    print("PROMPT CHARS:", len(prompt))

    start = time.time()

    response = generator(
        prompt,
        max_new_tokens=250,
        do_sample=False,
        return_full_text=False
    )

    end = time.time()

    print("GENERATION TIME:", round(end - start, 2))

    generated = response[0]["generated_text"]

    generated = generated.replace("```json", "")
    generated = generated.replace("```", "")
    generated = generated.strip()

    return generated