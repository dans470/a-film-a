Instrucciones para ejecutar el servicio de cartelera (FastAPI)

1) Crear y activar el entorno virtual (desde la carpeta `peliculas`):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2) Instalar dependencias:

```bash
pip install -r requirements.txt
```

3) Ejecutar con uvicorn (desde la carpeta `peliculas`):

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Notas:
- Si quieres ejecutar el script automático, usa `./run.sh` (asegúrate de darle permiso de ejecución).
- El archivo principal es `main.py` y expone la app FastAPI como `app`.
