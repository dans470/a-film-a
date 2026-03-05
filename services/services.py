import threading
from typing import List, Dict, Optional
import uuid

class User:
    def __init__(self, userId: int, name: str, email: str):
        self.userId = userId
        self.name = name
        self.email = email

class Movie:
    def __init__(self, movieId: int, title: str, movieDuration: int):
        self.movieId = movieId
        self.title = title
        self.duracion_minutos = movieDuration

class Room:
    def __init__(self, roomId: int, name: str, totalSeats: int):
        self.roomId = roomId
        self.name = name
        self.totalSeats = totalSeats

class Seat:
    def __init__(self, seatId: str):
        self.seatId = seatId
        self.occupied = False

class Schedule:
    def __init__(self, scheduleId: int, movieId: int, roomId: int, seatsIds: List[str]):
        self.scheduleId = scheduleId
        self.movieId = movieId
        self.roomId = roomId
        self.seats: Dict[str, Seat] = {id_s: Seat(id_s) for id_s in seatsIds}
        self._lock = threading.Lock()

    def getAvailableSeats(self) -> List[str]:
        return [b.seatId for b in self.seats.values() if not b.occupied]

    def seatReservation(self, seatsRequested: List[str]) -> bool:
        with self._lock:
            for asiento in seatsRequested:
                if asiento not in self.seats or self.seats[asiento].occupied:
                    return False
                            
            for seat in seatsRequested:
                self.seats[seat].occupied = True
            return True

class Booking:
    def __init__(self, userId: int, scheduleId: int, seats: List[str]):
        self.reserve_id = str(uuid.uuid4())
        self.userId = userId
        self.scheduleId = scheduleId
        self.seats = seats
        self.status = "PENDIENTE_PAGO"