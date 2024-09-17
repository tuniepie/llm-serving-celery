```bash
conda create -n <ENV-NAME> python=3.9
conda activate <ENV-NAME>
```

Terminal 1:
```bash
celery -A tasks worker --pool=eventlet --loglevel=info
```
Terminal 2: 
```bash
python main.py
```
API docs
-------------------------
- `POST: localhost/generate_code` 
```
INPUT
{
  "prompt": "promt"  
}
OUTPUT 
{
  "task_id": "cb1cc7a0-0f35-4036-9952-3bd5b615f22f"
}
```
- `GET: localhost/generate_code/<task_id>` 
```
OUTPUT
{
  "generated_code": "<OUTPUT FROM LLM>"
}
```