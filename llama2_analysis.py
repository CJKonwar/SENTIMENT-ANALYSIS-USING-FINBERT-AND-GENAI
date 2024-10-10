from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch
from dotenv import load_dotenv
import os
import torch


load_dotenv()
device = "cuda" if torch.cuda.is_available() else "cpu"


def load_llama2_model(device):
    model_name = "meta-llama/Llama-3.2-3B-Instruct"
    hf_token = os.getenv("hf_token")  # Replace with your actual token

    # Load tokenizer and model with the token, using CUDA if available
    tokenizer = AutoTokenizer.from_pretrained(model_name, use_auth_token=hf_token)
    
    # Ensure the model uses GPU (CUDA) if available, with automatic device mapping
    model = AutoModelForCausalLM.from_pretrained(
        model_name, 
        use_auth_token=hf_token, 
        device_map="auto",  # Automatically use GPU if available
        torch_dtype=torch.float16  # Use half-precision for faster inference
    )

    return model, tokenizer

def generate_summary_and_insights(headlines_df, model, tokenizer):
    # Concatenate all the headlines into one input string
    headlines_text = ". ".join(headlines_df['Headline'].tolist())

    # Set up a pipeline for text generation using the LLaMA 2 model
    text_generation = pipeline(
        "text-generation", 
        model=model, 
        tokenizer=tokenizer
        # Removed the `device` argument, as it's automatically handled
    )

    # Create a prompt for summarizing and generating insights on investment
    prompt = (f"Please summarize the following headlines: {headlines_text}. "
              "Provide detailed investment insights, including both short-term and long-term perspectives, "
              "along with sentiment analysis for each headline. "
              "Also, suggest whether it's a good time to invest in the company based on the insights provided.")
    # Generate the summary and insights using the model
    summary_and_insights = text_generation(
        prompt,
        max_length=1024,
        do_sample=True,
        truncation=True  # Enable truncation
    )[0]['generated_text']

    return summary_and_insights
