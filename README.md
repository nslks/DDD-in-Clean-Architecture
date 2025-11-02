# Clean Architecture und Domain-Driven Design

_Ein praktischer Vergleich mit FastAPI

---

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
- **Application** – Use Cases / Ablaufsteuerung  
- **Domain** – Geschäftslogik  
- **Infrastructure** – technische Details (z. B. DB)

Aber: Clean Architecture sagt **nicht**, wie die Geschäftslogik **fachlich** aufgebaut sein sollte.

---

## Problem ohne Clean Architecture

In vielen Projekten sieht der Code so aus:

```python
# app/interface/api.py
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
# app/application/create_order.py
def create_order(order_data, repo):
    items = [OrderItem(**item) for item in order_data["items"]]
    total = sum(i.price * i.quantity for i in items)
    if total <= 0:
        raise ValueError("Total must be positive")

    order = Order(id=None, items=items, total=total)
    return repo.save(order)
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

### Ein Beispiel für einen guten Anwendungsfall

- Eine Verischerungsplattform
  - Es gibt viele Fachbegriffe: Police, Tarif, Schadenfall, Risikoklasse, Selbstbeteiligung, Leistungsfall usw.
  - Fachabteilungen sprechen täglich in diesen Begriffen.
  - Benutzen Entwikckler dafür ihre eigenen Begriffe (customer_contract statt Police) verschlechtert das die Kommunikation.
- DDD hilft hier
  - Sprache = Modell. Die Domäne innerhalb der Anwendung spiegelt die reale Fachwelt.
  - Fachabteilungen und Entwickler können nicht anders als die selben Begriffe zu benutzen.

### Integration von DDD in Clean Architecture im Repo-Quellcode

---

### DDD-Kernelemente

- **Entities** – Objekte mit Identität  
- **Aggregates** – konsistente Gruppen von Entities  
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

## Codefluss im DDD-Beispiel

```API → Application (Use Case) → Domain (Order, OrderItem) → Repository```

- API löst Use Case aus  
- Application orchestriert nur  
- Domain enthält alle Regeln  
- Repository speichert Ergebnis

---

## Fazit

- Clean Architecture trennt und strukturiert den Code **technisch**.  
- DDD bringt **fachliche** Tiefe in die Anwendung.