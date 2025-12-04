### ✔ Gestión de Instrumentos
- Crear instrumentos
- Editar instrumentos
- Marcar un instrumento como descontinuado (stock = 0)
- Subir imágenes
- Listar y visualizar detalle

### ✔ Gestión de Clientes
- Crear clientes
- Editar clientes
- Eliminar clientes
- Foto de perfil opcional

### ✔ Gestión de Ventas
- Registrar una venta
- Relación cliente – instrumento
- Calculo automático del stock
- Dashboard de ventas

### ✔ API REST
Disponible con:
- /docs
- /redoc

---

## 📁 Estructura del Proyecto
```txt
musykal/
  │── main.py
  │── models.py
  │── schemas.py
  │── database.py
  │── static/
  │── templates/
  │   ├── base.html
  │   ├── index.html
  │   ├── clients/
  │   ├── instruments/
  │   └── sales/
  │── requirements.txt
  │── render.yaml
  └── README.md

```

---

### LA APLICACION YA HA SIDO DESPLEGADA:
https://musykal.onrender.com

## 💻 Instalación Local

# 1️ Clonar repositorio
git clone https://github.com/tu-repo/musykal.git
cd musykal

# 2️ Crear entorno virtual
python -m venv venv
source venv/bin/activate    # Linux/Mac
venv\Scripts\activate       # Windows

# 3️ Instalar dependencias
pip install -r requirements.txt

---

## ▶ Ejecución del Servidor
Modo desarrollo:

uvicorn main:app --reload

La app estará en:
http://127.0.0.1:8000/

---

## 🌐 Endpoints Principales

# HTML (Interfaz)
Home: /  
Instrumentos: /instruments/html  
Detalle: /instruments/{id}  
Editar: /instruments/update/{id}  
Clientes: /clients/html  
Ventas: /sales/html  

# API REST (JSON)
GET /instruments/  
POST /instruments/  
PUT /instruments/{id}  
DELETE /instruments/{id}  
GET /clients/  
POST /sales/  

---

## ☁ Ejecución en Render

### Build Command
pip install -r requirements.txt

### Start Command
uvicorn main:app --host 0.0.0.0 --port 10000

### Variables
DATABASE_URL=postgres://...

---
