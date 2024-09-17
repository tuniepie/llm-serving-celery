# from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline, GenerationConfig
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
# import torch
# from celery_config import celery
from celery.result import AsyncResult
from celery_config import celery

class CodeGenerationRequest(BaseModel):
    prompt: str


app = FastAPI()

@app.post("/generate_code")
async def generate_code(promt: CodeGenerationRequest):
    task = celery.send_task('tasks.execute_llm', args=[promt.prompt])
    return {"task_id": task.id}


@app.get("/generate_code/<task_id>")
async def status(task_id: str):
    result = AsyncResult(task_id, app=celery)
    if result.ready():
        return result.result
    else:
        return {"status": "pending"}

@app.get("/")
async def read_root():
    return {"message": "Welcome to the API"}

@app.get("/test")
async def test_():
    task = celery.send_task('tasks.test')
    return {"task_id": task.id}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9220)
# uvicorn main:app --reload --host 0.0.0.0 --port 9220
#celery -A tasks worker --pool=eventlet --loglevel=info
