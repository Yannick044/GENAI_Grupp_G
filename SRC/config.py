import os
from dotenv import load_dotenv
load_dotenv()

# Toggle: "cerebras" ODER "hf"
BACKEND = os.getenv("BACKEND", "cerebras").lower()

if BACKEND == "hf":
    BASE_URL = "https://router.huggingface.co/v1"
    API_KEY  = os.environ["HF_READ_TOKEN"]
    MODEL    = "openai/gpt-oss-120b:cerebras"   # wie im Unterrichtsbeispiel
else:
    BASE_URL = "https://api.cerebras.ai/v1"
    API_KEY  = os.environ["CEREBRAS_API_KEY"]
    MODEL    = "gpt-oss-120b"

TEMPERATURE = 0.2
