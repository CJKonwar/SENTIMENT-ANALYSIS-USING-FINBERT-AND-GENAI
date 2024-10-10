from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch
from dotenv import load_dotenv
import os

load_dotenv()
device = "cuda" if torch.cuda.is_available() else "cpu"

def load_llama2_model(device):
    model_name = "meta-llama/Llama-3.2-3B-Instruct"
    hf_token = os.getenv("hf_token")  # Replace with your actual token

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
        f"Analyze the following headlines by summarizing key points, identifying overall sentiment, and offering investment insights for the company: {headlines_text}. "
        "Provide actionable recommendations on whether current market conditions make it a suitable time to invest in this company.")

    # Generate summary and insights
    summary_and_insights = text_generation(
        prompt,
        max_length=1024,
        do_sample=True,
        truncation=True
    )[0]['generated_text']

    return summary_and_insights
