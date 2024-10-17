from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch


import streamlit as st
import os
from dotenv import load_dotenv
load_dotenv(dotenv_path='../../.env')
device = "cuda" if torch.cuda.is_available() else "cpu"

def load_llama2_model(device):
    model_name = "meta-llama/Llama-3.2-3B-Instruct"
    hf_token = os.getenv("HF_TOKEN")  # Replace with your actual token

    # Load tokenizer and model with the token, using CUDA if available
    tokenizer = AutoTokenizer.from_pretrained(model_name, token=hf_token)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        token=hf_token,
        device_map="auto",  # Automatically map to GPU if available
        torch_dtype=torch.float16  # Faster inference with half precision
    )
    return model, tokenizer

def generate_summary_and_insights(headlines_df, model, tokenizer):
    # Concatenate headlines into a single string
    headlines_text = ". ".join(headlines_df['Headline'].tolist())

    # Set up a text-generation pipeline
    text_generation = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer
    )

    # Formulate a prompt for the model
    prompt = (
        "Analyze the following news headlines and provide a structured summary along with investment insights:\n\n"
        f"Use the information from the following headlines:\n{headlines_text}\n\n"  # Keep this line to inform the model
        "Please include the following sections in your response:\n"
        "1. Summary: A brief summary of the news headlines.\n"
        "2. Short-Term View: An assessment of the stock's potential performance in the short term.\n"
        "3. Long-Term View: An assessment of the stock's potential performance in the long term.\n"
        "4. Investment Recommendation: Suggestions on whether it’s a good time to invest in this company based on the analysis.\n"
        "\nProvide your insights in a clear and concise manner without reiterating the headlines."
    )
    input_length = len(tokenizer.encode(prompt))
    max_length = 4096 - input_length  # Ensure total tokens don't exceed model limit

    # Generate summary and insights
    summary_and_insights = text_generation(
        prompt,
        max_length=max_length,
        do_sample=True,
        truncation=True
    )[0]['generated_text']

    start_phrase = "Please include the following sections in your response:"
    output_start = summary_and_insights.find(start_phrase)
    final_output = summary_and_insights[output_start:] if output_start != -1 else summary_and_insights

    return final_output