from datetime import date
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from .database import get_connection, init_db
from .models import CustomerCreate, ServiceCreate, AppointmentCreate, StatusUpdate

app = FastAPI(title="SalonFlow MVP", version="0.1.0")
templates = Jinja2Templates(directory="app/templates")

@app.on_event("startup")
def startup():
    init_db()

@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    conn = get_connection()
    today = date.today().isoformat()

    customers = conn.execute(
        "SELECT * FROM customers ORDER BY id DESC"
    ).fetchall()

    services = conn.execute(
        "SELECT * FROM services WHERE active=1 ORDER BY name"
    ).fetchall()

    appointments = conn.execute("""
        SELECT a.*, c.name AS customer_name, c.phone,
               s.name AS service_name, s.price
        FROM appointments a
        JOIN customers c ON c.id=a.customer_id
        JOIN services s ON s.id=a.service_id
        WHERE a.appointment_date=?
        ORDER BY a.appointment_time
    """, (today,)).fetchall()

    stats = {
        "customers": conn.execute("SELECT COUNT(*) FROM customers").fetchone()[0],
        "today": len(appointments),
        "confirmed": conn.execute(
            "SELECT COUNT(*) FROM appointments WHERE appointment_date=? AND status='confirmed'",
            (today,)
        ).fetchone()[0],
        "pending": conn.execute(
            "SELECT COUNT(*) FROM appointments WHERE appointment_date=? AND status='pending'",
            (today,)
        ).fetchone()[0],
    }
    conn.close()

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "customers": customers,
            "services": services,
            "appointments": appointments,
            "stats": stats,
            "today": today,
        },
    )

@app.post("/customers")
def create_customer(
    name: str = Form(...),
    phone: str = Form(...),
    notes: str = Form(""),
):
    conn = get_connection()
    conn.execute(
        "INSERT INTO customers (name, phone, notes) VALUES (?, ?, ?)",
        (name.strip(), phone.strip(), notes.strip()),
    )
    conn.commit()
    conn.close()
    return RedirectResponse("/", status_code=303)

@app.post("/services")
def create_service(
    name: str = Form(...),
    duration: int = Form(30),
    price: float = Form(0),
):
    conn = get_connection()
    conn.execute(
        "INSERT INTO services (name, duration, price) VALUES (?, ?, ?)",
        (name.strip(), duration, price),
    )
    conn.commit()
    conn.close()
    return RedirectResponse("/", status_code=303)

@app.post("/appointments")
def create_appointment(
    customer_id: int = Form(...),
    service_id: int = Form(...),
    appointment_date: str = Form(...),
    appointment_time: str = Form(...),
    notes: str = Form(""),
):
    conn = get_connection()

    conflict = conn.execute("""
        SELECT id FROM appointments
        WHERE appointment_date=? AND appointment_time=? AND status != 'cancelled'
    """, (appointment_date, appointment_time)).fetchone()

    if conflict:
        conn.close()
        raise HTTPException(
            status_code=409,
            detail="That time slot is already booked."
        )

    conn.execute("""
        INSERT INTO appointments
        (customer_id, service_id, appointment_date, appointment_time, notes)
        VALUES (?, ?, ?, ?, ?)
    """, (
        customer_id, service_id, appointment_date,
        appointment_time, notes.strip()
    ))
    conn.commit()
    conn.close()
    return RedirectResponse("/", status_code=303)

@app.post("/appointments/{appointment_id}/status")
def update_status(
    appointment_id: int,
    status: str = Form(...),
):
    allowed = {"pending", "confirmed", "completed", "cancelled", "no_show"}
    if status not in allowed:
        raise HTTPException(status_code=400, detail="Invalid status")

    conn = get_connection()
    conn.execute(
        "UPDATE appointments SET status=? WHERE id=?",
        (status, appointment_id),
    )
    conn.commit()
    conn.close()
    return RedirectResponse("/", status_code=303)

# API endpoints for the future WhatsApp integration.

@app.post("/api/customers")
def api_create_customer(customer: CustomerCreate):
    conn = get_connection()
    cur = conn.execute(
        "INSERT INTO customers (name, phone, notes) VALUES (?, ?, ?)",
        (customer.name.strip(), customer.phone.strip(), customer.notes or ""),
    )
    conn.commit()
    row = conn.execute(
        "SELECT * FROM customers WHERE id=?", (cur.lastrowid,)
    ).fetchone()
    conn.close()
    return dict(row)

@app.post("/api/services")
def api_create_service(service: ServiceCreate):
    conn = get_connection()
    cur = conn.execute(
        "INSERT INTO services (name, duration, price) VALUES (?, ?, ?)",
        (service.name.strip(), service.duration, service.price),
    )
    conn.commit()
    row = conn.execute(
        "SELECT * FROM services WHERE id=?", (cur.lastrowid,)
    ).fetchone()
    conn.close()
    return dict(row)

@app.post("/api/appointments")
def api_create_appointment(appointment: AppointmentCreate):
    conn = get_connection()

    conflict = conn.execute("""
        SELECT id FROM appointments
        WHERE appointment_date=? AND appointment_time=? AND status != 'cancelled'
    """, (
        appointment.appointment_date,
        appointment.appointment_time,
    )).fetchone()

    if conflict:
        conn.close()
        raise HTTPException(status_code=409, detail="Time slot already booked.")

    cur = conn.execute("""
        INSERT INTO appointments
        (customer_id, service_id, appointment_date, appointment_time, notes)
        VALUES (?, ?, ?, ?, ?)
    """, (
        appointment.customer_id,
        appointment.service_id,
        appointment.appointment_date,
        appointment.appointment_time,
        appointment.notes or "",
    ))
    conn.commit()
    row = conn.execute(
        "SELECT * FROM appointments WHERE id=?", (cur.lastrowid,)
    ).fetchone()
    conn.close()
    return dict(row)

@app.get("/api/availability")
def availability(appointment_date: str, service_id: int):
    conn = get_connection()
    booked = conn.execute("""
        SELECT appointment_time FROM appointments
        WHERE appointment_date=? AND service_id=? AND status != 'cancelled'
    """, (appointment_date, service_id)).fetchall()
    conn.close()

    booked_times = {r["appointment_time"] for r in booked}
    slots = [
        "09:00", "09:30", "10:00", "10:30",
        "11:00", "11:30", "12:00", "12:30",
        "14:00", "14:30", "15:00", "15:30",
        "16:00", "16:30", "17:00", "17:30",
        "18:00", "18:30", "19:00", "19:30",
    ]
    return {
        "date": appointment_date,
        "available": [s for s in slots if s not in booked_times],
    }

@app.get("/health")
def health():
    return {"status": "ok", "service": "salonflow-mvp"}
