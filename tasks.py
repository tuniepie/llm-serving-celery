from celery import Celery
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline, GenerationConfig
from pydantic import BaseModel
import os


model_name = "codellama/CodeLlama-7b-Instruct-hf"  
cache_dir = "/space/hotel/tungl/work/llm-dev-assistant/host-llm/cache"

redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")

llmapp = Celery("tasks", broker=redis_url, backend=redis_url)


# Load the tokenizer and model
model_name = "Qwen/CodeQwen1.5-7B"  # Replace with the correct model path if needed
model = AutoModelForCausalLM.from_pretrained("Qwen/CodeQwen1.5-7B", cache_dir=cache_dir)
tokenizer = AutoTokenizer.from_pretrained("Qwen/CodeQwen1.5-7B", cache_dir=cache_dir)

pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, device="cuda:0")

generation_config = GenerationConfig.from_pretrained(model_name)
generation_config.max_new_tokens = 512
generation_config.temperature = 0.0001
generation_config.do_sample = True

@llmapp.task
def execute_llm(message):
    code = pipe(message,
            return_full_text=True,
            generation_config=generation_config,
            num_return_sequences=1,
            eos_token_id=tokenizer.eos_token_id,
            pad_token_id=tokenizer.eos_token_id)[0]["generated_text"]

    return {"generated_code": code}
@llmapp.task
def test():

        return {"message": "Done"}