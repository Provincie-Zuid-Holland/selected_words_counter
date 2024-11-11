from flask import Flask, jsonify, request
from transformers import AutoModelForCausalLM, AutoTokenizer

# Load the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("GroNLP/gpt2-small-dutch")
model = AutoModelForCausalLM.from_pretrained("GroNLP/gpt2-small-dutch")


# Function to generate Dutch text
def generate_dutch_text(prompt, max_length=200, temperature=0.7, top_k=50, top_p=0.9):
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(
        inputs.input_ids,
        max_length=max_length,
        num_return_sequences=1,
        temperature=temperature,
        top_k=top_k,
        top_p=top_p,
        no_repeat_ngram_size=2,
        repetition_penalty=1.2,
    )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)
