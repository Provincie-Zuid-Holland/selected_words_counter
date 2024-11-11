from huggingface_hub import InferenceClient

from selected_words_counter.llms import keys

client = InferenceClient(api_key=keys.api_key)


def generate_message(
    message,
    amodel="meta-llama/Llama-3.1-8B-Instruct",
    atenperature=0.1,
    amax_tokens=1024,
    atop_p=0.7,
):
    messages = [{"role": "user", "content": message}]
    response = client.chat.completions.create(
        model=amodel,
        messages=messages,
        temperature=atenperature,
        max_tokens=amax_tokens,
        top_p=atop_p,
        stream=False,
    )

    output = response["choices"][0]["message"]["content"]

    return output.replace("\\n", "\n")
