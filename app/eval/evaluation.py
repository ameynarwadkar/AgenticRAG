"""
Automated RAG Evaluation - Continuous Quality Monitoring

This script utilizes Ragas (Retrieval Augmented Generation Assessment) to
programmatically evaluate the quality of the agent's responses.
It measures three core RAG metrics:
1. Faithfulness: Is the answer grounded purely in the retrieved context? (No hallucinations)
2. Answer Relevancy: Did the agent actually answer the user's question?
3. Context Precision: Was the retrieved context highly relevant and useful?

Run this script periodically (e.g., in a nightly CI/CD pipeline) against
recent production logs to ensure the agent's quality doesn't degrade over time.
"""
import os
from dotenv import load_dotenv
load_dotenv()
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
)

def run_evaluation(query: str, answer: str, contexts: list[str], ground_truth: str = None):
    """
    Run Ragas evaluation on a single interaction.
    In production, you'd pull batches of (query, answer, contexts) from Langfuse or Supabase.
    """
    
    # Ragas expects a HuggingFace Dataset format
    data_samples = {
        'question': [query],
        'answer': [answer],
        'contexts': [contexts], # Note: contexts is a list of strings for each row
        'ground_truth': [ground_truth] if ground_truth else [""]
    }
    
    dataset = Dataset.from_dict(data_samples)
    
    # Run evaluation using Azure OpenAI models
    metrics = [faithfulness, answer_relevancy, context_precision]
    
    # Initialize Azure OpenAI clients for Ragas
    azure_llm = AzureChatOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4o")
    )
    
    azure_embeddings = AzureOpenAIEmbeddings(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        azure_deployment=os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME", "text-embedding-3-small")
    )
    
    score = evaluate(
        dataset, 
        metrics=metrics, 
        llm=azure_llm, 
        embeddings=azure_embeddings
    )
    
    print("\n--- RAGAS Evaluation Results ---")
    print(score.to_pandas())
    return score

if __name__ == "__main__":
    # Example test
    sample_q = "What is your return policy?"
    sample_a = "Exchanges for different sizes are free within 30 days."
    sample_ctx = ["We accept returns within 30 days. Size exchanges are completely free."]
    
    run_evaluation(sample_q, sample_a, sample_ctx)
