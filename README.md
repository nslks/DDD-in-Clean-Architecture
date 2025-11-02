# Clean Architecture und Domain-Driven Design

## Ziel

Wir wollen verstehen:

- Was Clean Architecture leistet
- Wo ihre Schwächen liegen  
- Wie Domain-Driven Design (DDD) diese Lücken füllt  
- Wie das Ganze im Code aussieht

---

## Ausgangspunkt

**Clean Architecture** trennt Schichten:

- **Interface (API)** – Kommunikation nach außen  
- **Controller/Application/etc. u name it** – Use Cases / Ablaufsteuerung  
- **Domain** – Datenobjekte  
- **Repository** – DB zugriff

Aber: Clean Architecture sagt **nicht**, wie die Geschäftslogik **fachlich** aufgebaut sein sollte.

---

## Problem ohne Clean Architecture

In vielen Projekten sieht der Code so aus:

```python
# src/interface/api.py
@app.post("/orders")
def create_order(order_data: dict):
    total = sum(item["price"] * item["quantity"] for item in order_data["items"])
    if total < 0:
        raise ValueError("Total must be positive")
    order_id = save_to_db(order_data, total)
    return {"order_id": order_id}
```

### Schwächen

- Fachlogik liegt im API-Endpoint
- Keine klaren Domänenregeln  
- Schwer testbar  
- Kein „Fachmodell“, nur Datenstrukturen

---

## Schritt 1: Clean Architecture anwenden

Wir trennen Schichten technisch.

```python
# src/controller/bookingcontroller.py
    def create_booking(self, room_id, customer_name, start_date, end_date):
        
        # erste fachliche Regel
        if self._booking_lasts_longer_than_max_days(start_date, end_date):
            raise ValueError(f"Booking too long")
        
        # zweite fachliche Regel: Überschneidungen prüfen (innerhalb Use Case)
        for existing in self.repo.all():
            if self._room_not_available(existing, room_id, start_date, end_date):
                raise ValueError("Room not available for given dates")
            
        booking = Booking(
            id=0,
            room_id=room_id,
            customer_name=customer_name,
            start_date=start_date,
            end_date=end_date
        )

        return self.repo.save(booking)
    
    def _booking_lasts_longer_than_max_days(self, start_date, end_date):
        max_allowed_day = 10

        days = (end_date - start_date).days
        return days > max_allowed_day
    
    def _room_not_available(self, existing, room_id, start_date, end_date):
        same_room = existing.room_id == room_id
        overlapping = not (end_date <= existing.start_date or start_date >= existing.end_date)
        return same_room and overlapping

```

### Ergebnis

- **Vorteil:** Struktur sauber  
- **Schwäche:** Fachlogik bleibt im Use Case, Domain ist passiv  

---

## Schritt 2: DDD ergänzt die Clean Architecture

### Wann DDD sinnvoll ist

Nur, wenn:

- Die Domäne **komplex** ist.
- Eine gemeinsame, eindeutige Sprache zwischen Entwicklern und Fachexperten notwendig ist.

### Integration von DDD in Clean Architecture

```python
# src/controller/bookingcontroller.py
    def create_booking(self, room_id, customer_name, start_date, end_date):
        new_booking = Booking(
            room_id=room_id,
            customer_name=customer_name,
            start_date=start_date,
            end_date=end_date
        )

        for existing in self.repo.all():
            if new_booking.overlaps(existing):
                raise ValueError("Room not available for given dates")

        return self.repo.save(new_booking)

# src/domain/booking.py
  class Booking:
    def __init__(self, booking_id, room_id, customer_name, start_date, end_date):
        if start_date >= end_date:
            raise ValueError("end_date must be after start_date")

        duration = (end_date - start_date).days
        if duration > MAX_BOOKING_DAYS:
            raise ValueError(f"Booking cannot exceed {MAX_BOOKING_DAYS} days")

        self.id = booking_id
        self.room_id = room_id
        self.customer_name = customer_name
        self.start_date = start_date
        self.end_date = end_date
    
    
    def overlaps(self, other):
        return self.room_id == other.room_id and not (
            self.end_date <= other.start_date or self.start_date >= other.end_date
        )
```

### Ein echtes Beispiel für einen guten Anwendungsfall

- Eine Verischerungsplattform
  - Es gibt viele Fachbegriffe: Police, Tarif, Schadenfall, Risikoklasse, Selbstbeteiligung, Leistungsfall usw.
  - Fachabteilungen sprechen täglich in diesen Begriffen.
  - Benutzen Entwikckler dafür ihre eigenen Begriffe (customer_contract statt Police) verschlechtert das die Kommunikation.
- DDD hilft hier
  - Sprache = Modell. Die Domäne innerhalb der Anwendung spiegelt die reale Fachwelt.
  - Fachabteilungen und Entwickler können nicht anders als die selben Begriffe zu benutzen.

---

### DDD-Kernelemente

- **Entities** – Objekte mit Identität
- **Value Objects**, **Aggregates** etc.
- **Repositories** – Schnittstellen zur Datenhaltung  

---

## Vergleich

| Aspekt | Nur Clean Architecture | Mit DDD |
|--------|------------------------|----------|
| **Struktur** | Technisch klar | Fachlich & technisch klar |
| **Domain Layer** | Datencontainer | Intelligente Objekte |
| **Businesslogik** | In Use Cases | In Domain |
| **Testbarkeit** | Mittel | Hoch |
| **Fachsprache** | Fehlend | Klar definiert |
| **Wartbarkeit** | Gut bei kleiner Domäne | Besser bei wachsender Komplexität |

---

## Fazit

- Clean Architecture trennt und strukturiert den Code **technisch**.  
- DDD bringt **fachliche** Tiefe in die Anwendung.
