import os
from fastapi import FastAPI, Depends, HTTPException, Request, UploadFile, File, Form
from fastapi.responses import FileResponse, RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import models, schemas
from database import SessionLocal, engine
import aiofiles

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Music Store API with UI")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
IMAGES_DIR = os.path.join(STATIC_DIR, "images")
CLIENTS_IMG_DIR = os.path.join(IMAGES_DIR, "clients")
INSTR_IMG_DIR = os.path.join(IMAGES_DIR, "instruments")
os.makedirs(CLIENTS_IMG_DIR, exist_ok=True)
os.makedirs(INSTR_IMG_DIR, exist_ok=True)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
def read_root_html(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

async def save_upload_image(uploaded_file: UploadFile, dest_folder: str):
    if not uploaded_file:
        return None
    filename = uploaded_file.filename
    if filename == "":
        return None
    import uuid
    ext = os.path.splitext(filename)[1]
    unique_name = f"{uuid.uuid4().hex}{ext}"
    dest_path = os.path.join(dest_folder, unique_name)
    async with aiofiles.open(dest_path, "wb") as out_file:
        content = await uploaded_file.read()
        await out_file.write(content)
    rel_path = os.path.relpath(dest_path, STATIC_DIR)
    return f"/static/{rel_path.replace(os.path.sep, '/')}"

# CLIENTS API + HTML
@app.post("/clients/", response_model=schemas.Client)
async def create_client_api(client: schemas.ClientCreate, db: Session = Depends(get_db)):
    db_client = models.Client(**client.model_dump())
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

@app.get("/clients/", response_model=list[schemas.Client])
def get_clients_api(db: Session = Depends(get_db)):
    return db.query(models.Client).all()

@app.get("/clients/html", response_class=HTMLResponse)
def clients_list_html(request: Request, db: Session = Depends(get_db)):
    clients = db.query(models.Client).all()
    return templates.TemplateResponse("clients/list.html", {"request": request, "clients": clients})

@app.get("/clients/create", response_class=HTMLResponse)
def client_form_create(request: Request):
    return templates.TemplateResponse("clients/create.html", {"request": request})

@app.post("/clients/create", response_class=HTMLResponse)
async def client_create_post(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    image: UploadFile | None = File(None),
    db: Session = Depends(get_db),
):
    image_url = await save_upload_image(image, CLIENTS_IMG_DIR) if image else None
    db_client = models.Client(name=name, email=email, phone=phone, image=image_url)
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return RedirectResponse(url="/clients/html", status_code=303)

@app.get("/clients/{client_id}", response_class=HTMLResponse)
def client_detail_html(request: Request, client_id: int, db: Session = Depends(get_db)):
    client = db.query(models.Client).filter(models.Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return templates.TemplateResponse("clients/detail.html", {"request": request, "client": client})

@app.post("/clients/delete/{client_id}")
def client_delete_html(client_id: int, db: Session = Depends(get_db)):
    client = db.query(models.Client).filter(models.Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    if client.image:
        try:
            local_path = client.image.replace("/static/", "")
            full = os.path.join(STATIC_DIR, local_path)
            if os.path.exists(full):
                os.remove(full)
        except Exception:
            pass
    db.delete(client)
    db.commit()
    return RedirectResponse(url="/clients/html", status_code=303)

# INSTRUMENTS API + HTML
@app.post("/instruments/", response_model=schemas.Instrument)
async def create_instrument_api(instrument: schemas.InstrumentCreate, db: Session = Depends(get_db)):
    db_instrument = models.Instrument(**instrument.model_dump())
    db.add(db_instrument)
    db.commit()
    db.refresh(db_instrument)
    return db_instrument

@app.get("/instruments/", response_model=list[schemas.Instrument])
def get_instruments_api(db: Session = Depends(get_db)):
    return db.query(models.Instrument).all()

@app.get("/instruments/html", response_class=HTMLResponse)
def instruments_list_html(request: Request, db: Session = Depends(get_db)):
    instruments = db.query(models.Instrument).all()
    return templates.TemplateResponse("instruments/list.html", {"request": request, "instruments": instruments})

@app.get("/instruments/create", response_class=HTMLResponse)
def instrument_form_create(request: Request):
    return templates.TemplateResponse("instruments/create.html", {"request": request})

@app.post("/instruments/create", response_class=HTMLResponse)
async def instrument_create_post(
    request: Request,
    name: str = Form(...),
    brand: str = Form(...),
    price: float = Form(...),
    stock: int = Form(...),
    image: UploadFile | None = File(None),
    db: Session = Depends(get_db),
):
    image_url = await save_upload_image(image, INSTR_IMG_DIR) if image else None
    db_instrument = models.Instrument(name=name, brand=brand, price=price, stock=stock, image=image_url)
    db.add(db_instrument)
    db.commit()
    db.refresh(db_instrument)
    return RedirectResponse(url="/instruments/html", status_code=303)

@app.get("/instruments/{instrument_id}", response_class=HTMLResponse)
def instrument_detail_html(request: Request, instrument_id: int, db: Session = Depends(get_db)):
    instrument = db.query(models.Instrument).filter(models.Instrument.id == instrument_id).first()
    if not instrument:
        raise HTTPException(status_code=404, detail="Instrumento no encontrado")
    return templates.TemplateResponse("instruments/detail.html", {"request": request, "instrument": instrument})

@app.post("/instruments/delete/{instrument_id}")
def instrument_delete_html(instrument_id: int, db: Session = Depends(get_db)):
    instrument = db.query(models.Instrument).filter(models.Instrument.id == instrument_id).first()
    if not instrument:
        raise HTTPException(status_code=404, detail="Instrumento no encontrado")
    if instrument.image:
        try:
            local_path = instrument.image.replace("/static/", "")
            full = os.path.join(STATIC_DIR, local_path)
            if os.path.exists(full):
                os.remove(full)
        except Exception:
            pass
    db.delete(instrument)
    db.commit()
    return RedirectResponse(url="/instruments/html", status_code=303)

# ORDERS
@app.post("/orders/", response_model=schemas.Order)
def create_order_api(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    instrument = db.query(models.Instrument).filter(models.Instrument.id == order.instrument_id).first()
    if not instrument:
        raise HTTPException(status_code=404, detail="Instrumento no encontrado")
    total = instrument.price * order.quantity
    db_order = models.Order(client_id=order.client_id, instrument_id=order.instrument_id, quantity=order.quantity, total=total)
    instrument.stock = max(0, instrument.stock - order.quantity)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

@app.get("/orders/html", response_class=HTMLResponse)
def orders_list_html(request: Request, db: Session = Depends(get_db)):
    orders = db.query(models.Order).order_by(models.Order.created_at.desc()).all()
    clients = {c.id: c for c in db.query(models.Client).all()}
    instruments = {i.id: i for i in db.query(models.Instrument).all()}
    return templates.TemplateResponse("orders/list.html", {"request": request, "orders": orders, "clients": clients, "instruments": instruments})

@app.get("/orders/create", response_class=HTMLResponse)
def order_create_form(request: Request, db: Session = Depends(get_db)):
    clients = db.query(models.Client).all()
    instruments = db.query(models.Instrument).all()
    return templates.TemplateResponse("orders/create.html", {"request": request, "clients": clients, "instruments": instruments})

@app.post("/orders/create", response_class=HTMLResponse)
def order_create_post(request: Request, client_id: int = Form(...), instrument_id: int = Form(...), quantity: int = Form(...), db: Session = Depends(get_db)):
    instrument = db.query(models.Instrument).filter(models.Instrument.id == instrument_id).first()
    if not instrument:
        raise HTTPException(status_code=404, detail="Instrumento no encontrado")
    total = instrument.price * quantity
    db_order = models.Order(client_id=client_id, instrument_id=instrument_id, quantity=quantity, total=total)
    instrument.stock = max(0, instrument.stock - quantity)
    db.add(db_order)
    db.commit()
    return RedirectResponse(url="/orders/html", status_code=303)

# DASHBOARD
@app.get("/dashboard", response_class=HTMLResponse)
def dashboard_html(request: Request, db: Session = Depends(get_db)):
    from sqlalchemy import func
    sales_data = (
        db.query(models.Instrument.name, func.sum(models.Order.total).label("sales"))
        .join(models.Order, models.Instrument.id == models.Order.instrument_id)
        .group_by(models.Instrument.id)
        .all()
    )
    sales_by_day = (
        db.query(func.date(models.Order.created_at).label("day"), func.sum(models.Order.total).label("sales"))
        .group_by(func.date(models.Order.created_at))
        .order_by(func.date(models.Order.created_at).desc())
        .limit(30)
        .all()
    )
    sales_data = [{"name": s[0], "sales": float(s[1] or 0)} for s in sales_data]
    sales_by_day = [{"day": str(s[0]), "sales": float(s[1] or 0)} for s in sales_by_day[::-1]]
    return templates.TemplateResponse("dashboard.html", {"request": request, "sales_data": sales_data, "sales_by_day": sales_by_day})

# EXPORTS
@app.get("/export/clients")
def export_clients(db: Session = Depends(get_db)):
    clients = db.query(models.Client).all()
    file_path = "clients.txt"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("=== LISTA DE CLIENTES ===\n\n")
        for c in clients:
            f.write(f"ID: {c.id}\nNombre: {c.name}\nEmail: {c.email}\nTeléfono: {c.phone}\nImagen: {c.image or 'N/A'}\n\n")
    return FileResponse(path=file_path, filename="clients.txt", media_type="text/plain")

@app.get("/export/instruments")
def export_instruments(db: Session = Depends(get_db)):
    instruments = db.query(models.Instrument).all()
    file_path = "instruments.txt"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("=== LISTA DE INSTRUMENTOS ===\n\n")
        for i in instruments:
            f.write(
                f"ID: {i.id}\n"
                f"Nombre: {i.name}\n"
                f"Marca: {i.brand}\n"
                f"Precio: {i.price}\n"
                f"Stock: {i.stock}\n"
                f"Imagen: {i.image or 'N/A'}\n\n"
            )
    return FileResponse(path=file_path, filename="instruments.txt", media_type="text/plain")

# DOCUMENTATION
@app.get("/documentation", response_class=HTMLResponse)
def documentation_html(request: Request):
    return templates.TemplateResponse("documentation.html", {"request": request})
