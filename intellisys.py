"""
Provides intelligence/AI services for the Lifsys Enterprise
"""
__version__ = "0.1.0"
import os
import json
from time import sleep
from typing import Optional
from openai import OpenAI
from litellm import completion
from jinja2 import Template
from onepasswordconnectsdk import new_client_from_environment

def get_api(item, key_name, vault="API"):
    try:
        client = new_client_from_environment()
        item = client.get_item(item, vault)
        for field in item.fields:
            if field.label == key_name:
                return field.value
    except Exception as e:
        raise Exception(f"Connect Error: {e}")

def fix_json(json_string):
    prompt = f"You are a JSON formatter, fixing any issues with JSON formats. Review the following JSON: {json_string}. Return a fixed JSON formatted string but do not lead with ```json\n, without making changes to the content."
    return get_completion_api(prompt, "gemini-flash", "system", prompt)

def template_api_json(model, render_data, system_message, persona):
    """
    Get the completion response from the API using the specified model.
    render_data: The data to render the template, e.g. {"name": "John"} - dict
    """
    xtemplate = Template(system_message)
    prompt = xtemplate.render(render_data)
    response = get_completion_api(prompt, model, "system", persona)
    response = response.strip("```json\n").strip("```").strip()
    response = json.loads(response)
    return response

def template_api(model, render_data, system_message, persona):
    """
    Get the completion response from the API using the specified model.
    render_data: The data to render the template, e.g. {"name": "John"} - dict
    """
    xtemplate = Template(system_message)
    prompt = xtemplate.render(render_data)
    response = get_completion_api(prompt, model, "system", persona)
    return response

def initialize_client():
    """
    Initialize the OpenAI client with the provided API key.
    """
    api_key = get_api("OPEN-AI", "Mamba")
    return OpenAI(api_key=api_key)

def create_thread(client):
    """
    Create a new thread using the OpenAI client.
    """
    return client.beta.threads.create()

def send_message(client, thread_id, reference):
    """
    Send a message to the specified thread.
    """
    return client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=reference,
    )

def run_assistant(client, thread_id, assistant_id):
    """
    Run the assistant for the specified thread.
    """
    return client.beta.threads.runs.create(
        thread_id=thread_id, assistant_id=assistant_id
    )

def wait_for_run_completion(client, thread_id, run_id):
    """
    Wait for the assistant run to complete.
    """
    run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
    while run.status in ["queued", "in_progress"]:
        sleep(0.5)  # Add a delay to avoid rapid polling
        run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
    return run

def get_assistant_responses(client, thread_id):
    """
    Retrieve and clean the assistant's responses from the thread.
    """
    message_list = client.beta.threads.messages.list(thread_id=thread_id)
    assistant_responses = [
        message.content[0].text.value
        for message in message_list.data
        if message.role == "assistant"
    ]
    return assistant_responses

def get_assistant(reference, assistant_id):
    """
    Get the assistant's response for the given reference and assistant ID.
    """
    client = initialize_client()
    thread = create_thread(client)
    send_message(client, thread.id, reference)
    run = run_assistant(client, thread.id, assistant_id)
    wait_for_run_completion(client, thread.id, run.id)
    responses = get_assistant_responses(client, thread.id)
    return responses

def get_completion_api(
    prompt: str,
    model_name: str,
    mode: str = "simple",
    system_message: Optional[str] = None,
) -> Optional[str]:
    """
    Get the completion response from the API using the specified model.

    :param prompt: The prompt to send to the API.
    :param model_name: The name of the model to use for completion.
    :param mode: The mode of message sending (simple or system).
    :param system_message: The system message to send if in system mode.
    :return: The completion response content.
    """
    try:
        # Select the model and set the appropriate API key
        match model_name:
            case "gpt-3.5-turbo" | "gpt-4" | "gpt-4o":
                os.environ["OPENAI_API_KEY"] = get_api("OPEN-AI", "Mamba")
                selected_model = model_name
            case "claude-3.5-sonnet":
                os.environ["ANTHROPIC_API_KEY"] = get_api("Anthropic", "CLI-Maya")
                selected_model = "claude-3-5-sonnet-20240620"
            case "gemini-flash":
                os.environ["GEMINI_API_KEY"] = get_api("Gemini", "CLI-Maya")
                selected_model = "gemini/gemini-1.5-flash"
            case "llama-3-70b":
                os.environ["TOGETHERAI_API_KEY"] = get_api("TogetherAI", "API")
                selected_model = "together_ai/meta-llama/Llama-3-70b-chat-hf"
            case "groq-llama":
                os.environ["GROQ_API_KEY"] = get_api("Groq", "Promptsys")
                selected_model = "groq/llama3-70b-8192"
            case "groq-fast":
                os.environ["GROQ_API_KEY"] = get_api("Groq", "Promptsys")
                selected_model = "groq/llama3-8b-8192"
            case _:
                raise ValueError(f"Unsupported model: {model_name}")

        # Select message type
        match mode:
            case "simple":
                print("Message Simple")
                messages = [{"content": prompt, "role": "user"}]
            case "system":
                if system_message is None:
                    raise ValueError("system_message must be provided in system mode")
                messages = [
                    {"content": system_message, "role": "system"},
                    {"content": prompt, "role": "user"},
                ]
            case _:
                raise ValueError(f"Unsupported mode: {mode}")

        # Make the API call
        response = completion(
            model=selected_model,
            messages=messages,
            temperature=0.1,
        )

        # Extract and return the response content
        return response["choices"][0]["message"]["content"]

    except KeyError as ke:
        print(f"Key error occurred: {ke}")
    except ValueError as ve:
        print(f"Value error occurred: {ve}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return None

def fix_json(json_string):
    prompt = f"You are a JSON formatter, fixing any issues with JSON formats. Review the following JSON: {json_string}. Return a fixed JSON formatted string but do not lead with ```json\n, without making changes to the content."
    return get_completion_api(prompt, "gemini-flash", "system", prompt)
