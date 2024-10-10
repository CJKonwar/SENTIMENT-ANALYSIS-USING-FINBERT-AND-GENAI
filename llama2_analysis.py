from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch

def load_llama2_model():
    # Change the model to LLaMA-2-3B for a lighter version
    model_name = "meta-llama/Llama-3.2-3B-Instruct"
    hf_token = "hf_token"  # Replace with your actual token

    # Load tokenizer and model with the token
    tokenizer = AutoTokenizer.from_pretrained(model_name, use_auth_token=hf_token)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        use_auth_token=hf_token,
        device_map="auto",  # Use automatic device mapping (GPU if available)
        torch_dtype=torch.float16  # Use half-precision for faster inference and lower memory usage
    )

    return model, tokenizer


def generate_summary_and_insights(headlines_df, model, tokenizer):
    # Concatenate all the headlines into one input string
    headlines_text = ". ".join(headlines_df['Headline'].tolist())

    # Set up a pipeline for text generation using the LLaMA 2 model
    text_generation = pipeline("text-generation", model=model, tokenizer=tokenizer)

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
