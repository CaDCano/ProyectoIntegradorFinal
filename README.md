# Music Store - Proyecto listo para ejecutar

## Requisitos
- Python 3.10+
- Instalar dependencias:
```
pip install -r requirements.txt
```

## Ejecutar
```
uvicorn main:app --reload
```
Luego abrir http://127.0.0.1:8000

## Contenido
- `main.py` - servidor FastAPI con rutas HTML y API
- `models.py`, `schemas.py`, `database.py` - modelos y DB
- `templates/` - plantillas Jinja2
- `static/` - CSS e imágenes
