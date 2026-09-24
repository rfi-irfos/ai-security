import os
import boto3
from dotenv import load_dotenv

# Load variables from .env into os.environ
load_dotenv()

def main():
    # Use explicitly set region or default to us-east-1
    region = os.environ.get('AWS_REGION') or os.environ.get('AWS_DEFAULT_REGION') or 'us-east-1'
    access_key = os.environ.get('AWS_ACCESS_KEY_ID')
    secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
    
    print(f"Connecting to AWS Bedrock in region: {region}...")
    if access_key and secret_key:
        print("Using explicitly provided AWS credentials from .env")
        client = boto3.client(
            'bedrock',
            region_name=region,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key
        )
    else:
        print("No AWS credentials found in .env. Relying on default boto3 resolution (e.g., IAM role, ~/.aws/credentials).")
        client = boto3.client('bedrock', region_name=region)

    try:
        response = client.list_foundation_models()
        models = response.get('modelSummaries', [])
        
        print("\n=== AVAILABLE ANTHROPIC MODELS ===")
        anthropic_count = 0
        for model in models:
            model_id = model.get('modelId', '')
            if 'anthropic' in model_id.lower() or 'claude' in model_id.lower():
                # Provide the formatted version you should use in litellm/config.yaml
                print(f" bedrock/{model_id}")
                anthropic_count += 1
                
        if anthropic_count == 0:
            print("No Anthropic models found. They might be disabled in your account or region.")
            
        print("\n=== OTHER AVAILABLE TEXT MODELS ===")
        for model in models:
            model_id = model.get('modelId', '')
            modalities = model.get('outputModalities', [])
            if 'TEXT' in modalities and 'anthropic' not in model_id.lower() and 'claude' not in model_id.lower():
                print(f" bedrock/{model_id}")

        print("\nNote: When using these in your config.yaml, make sure to use the 'bedrock/' prefix as formatted above!")

    except Exception as e:
        print(f"\nError retrieving models: {e}")

if __name__ == "__main__":
    main()
