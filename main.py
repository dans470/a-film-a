#Servicio de cartelera, se encarga de mostrar las peliculas disponibles en el cine
#Genera el yml de los endpoints de cartelera
#La información de las películas se obtiene de una API externa (TMDB)
from fastapi import FastAPI, HTTPException # type: ignore
from pydantic import BaseModel # type: ignore
from typing import Dict, List, Optional
from payment.payment import PaymentFactory, PaymentProcesser
from services.services import Schedule, Booking
from fastapi.middleware.cors import CORSMiddleware # type: ignore
from fastapi.responses import FileResponse # type: ignore
import random

app = FastAPI(
    title="Servicio de Cartelera",
    description="Servicio encargado de mostrar las películas disponibles en el cine",
    version="1.0.0",
    contact={
        "name": "Equipo A-FILM-A",
        "email": "afilmacines@example.com",
        "url": "https://afilmacines.com",
        }
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db = {
    "schedules": {}, 
    "bookings": {},  
}

availableSeats = []
for row in ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]:
    for num in range(1, 21):
        availableSeats.append(f"{row}{num}")

class MovieResponse(BaseModel):
    movieId: int
    title: str
    urlPoster: Optional[str] = None

class ScheduleResponse(BaseModel):
    scheduleId: int
    movieId: int
    roomId: int
    schedule: str
    avalibleSeats: List[str]

class BookingRequest(BaseModel):
    scheduleId: int
    usuarioId: int
    seats: List[str]

class BookingResponse(BaseModel):
    reserveId: str
    status: str
    message: str

class PayRequest(BaseModel):
    reserveId: str
    payMethod: str

@app.get("/movies", response_model=List[MovieResponse])
def GetMovies():
    # Aquí se haría la lógica para obtener las películas de la cartelera desde una API externa (TMDB)
    pass

@app.get("/showtimes/{movieId}")
def GetSchedule(movieId: int):
    movieSchedule = [s for s in db["schedules"].values() if s.movieId == movieId]

    if not movieSchedule:
        time = ["14:00", "16:30", "19:00", "21:30"]
        for time in time:
            newId = len(db["schedules"]) + 1 
            
            newSchedule = Schedule(
                scheduleId=newId, 
                movieId=movieId, 
                roomId=1, 
                seatsIds=availableSeats 
            )
            newSchedule.hora = time
            
            occupied = random.sample(availableSeats, k=random.randint(15, 60))
            for seat in occupied:
                newSchedule.seats[seat].occupied = True
                
            db["schedules"][newId] = newSchedule
            movieSchedule.append(newSchedule)

    return [
        {
            "scheduleId": s.scheduleId,
            "hora": getattr(s, 'hora', "12:00"),
            "estado_asientos": {
                "disponibles": [id_a for id_a, seat in s.seats.items() if not seat.occupied],
                "ocupados": [id_a for id_a, seat in s.seats.items() if seat.occupied]
            }
        } for s in movieSchedule
    ]

@app.post("/bookings/reserve")
def BuyTickets(request: BookingRequest):
    schedule = db["schedules"].get(request.scheduleId)
    if not schedule:
        raise HTTPException(status_code=404, detail="Horario no encontrado")
        
    success = schedule.seatReservation(request.seats)
    
    if not success:
        raise HTTPException(status_code=409, detail="Una o más butacas ya están ocupadas o son inválidas.")
    
    newReservation = Booking(request.usuarioId, request.scheduleId, request.seats)
    db["bookings"][newReservation.reserve_id] = newReservation
    
    return {
        "reserveId": newReservation.reserve_id, 
        "status": newReservation.status, 
        "message": "Butacas bloqueadas con éxito"
    }    


@app.post("/bookings/pay")
def PayBooking(request: PayRequest):
    reserve = db["bookings"].get(request.reserveId)
    if not reserve:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    if reserve.status == "PAGADO":
        raise HTTPException(status_code=400, detail="Reserva ya pagada")
    
    try:
        strategy = PaymentFactory.GetStrategy(request.payMethod)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    processor = PaymentProcesser(strategy)

    totalAmount = len(reserve.seats) * 50
    success = processor.pay(totalAmount)

    if success:
        reserve.status = "PAGADO"
        return BookingResponse(reserveId=reserve.reserve_id, status=reserve.status, message="Pago exitoso")
    else:
        return BookingResponse(reserveId=reserve.reserve_id, status=reserve.status, message="Pago fallido")
    pass

@app.get("/")
def leer_index():
    return FileResponse("../public/index.html")