1) Поднимаем TEI на серваке:

```bash
sudo docker run --gpus all \
  -p 8080:80 \
  -v ~/.cache/huggingface:/root/.cache/huggingface \
  -e MODEL_ID=deepvk/USER-bge-m3 \
  ghcr.io/huggingface/text-embeddings-inference:latest

```
- `ssh -L 8080:localhost:8080 workgpu` - проброс
- `curl -v http://localhost:8080/health` - проверка

2) Поднимаем qdrant:

```bash
docker run -p 6333:6333 -p 6334:6334 \
    -v "$(pwd)/qdrant_storage:/qdrant/storage:z" \
    qdrant/qdrant
```
- `ssh -L 6333:localhost:6333 workgpu` - проброс
- `http://localhost:6333/dashboard` - дашборд

