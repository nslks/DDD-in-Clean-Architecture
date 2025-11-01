# agent.md

## Ziel
Erstelle ein lauffähiges Python-Projekt, das **den Übergang von Clean Architecture zu Clean Architecture + Domain-Driven Design (DDD)** Schritt für Schritt zeigt.  
Das Projekt dient als **Lern- und Präsentationsbeispiel**.  
Es soll **vollständig mit Pytest testbar** sein und die **Verbesserung der Testbarkeit durch DDD** verdeutlichen.

---

## Anforderungen

### 1. Sprache & Umgebung
- Python ≥ 3.10  
- Pytest für Tests  
- Keine externen Libraries außer Standardbibliothek  
- Das Projekt muss mit `pytest` vollständig lauffähig sein  
- Stil: saubere Layer-Trennung, Typannotationen, sprechende Namen  

---

## 2. Gesamtstruktur

Das Projekt soll zwei Hauptordner enthalten, um die Entwicklung **nebeneinander sichtbar** zu machen:

```
src/
├── clean_architecture/
│   ├── domain/
│   │   └── entities.py
│   ├── application/
│   │   └── create_order.py
│   └── infrastructure/
│       └── order_repository_sql.py
├── clean_architecture_ddd/
│   ├── ordering/
│   │   ├── domain/
│   │   │   ├── entities.py
│   │   │   ├── value_objects.py
│   │   │   └── repositories.py
│   │   ├── application/
│   │   │   └── use_cases.py
│   │   └── infrastructure/
│   │       └── order_repository_inmemory.py
│   └── pricing/
│       └── domain/
│           └── discount_service.py
tests/
├── clean_architecture/
│   └── test_create_order.py
└── clean_architecture_ddd/
    ├── ordering/
    │   ├── test_order_entity.py
    │   └── test_order_usecase.py
    └── pricing/
        └── test_discount_service.py
```

Diese Struktur zeigt den Code **vorher/nachher direkt nebeneinander**  
→ Der Unterschied zwischen Clean Architecture und Clean Architecture + DDD ist **im Dateisystem erkennbar.**

---

## 3. Implementierungsdetails

### **Teil 1 – Clean Architecture (Baseline)**
- `Order` Entity: technisch einfach (id, user_id, total)
- `CreateOrderUseCase`: summiert Preise direkt im Use Case
- `SqlOrderRepository`: simuliert DB-Speicher (keine echte DB)
- Ziel: technisch klar, aber fachlich schwach und schwer testbar

**Beispiel-Test:**  
`tests/clean_architecture/test_create_order.py`
```python
def test_create_order_sums_total_correctly():
    repo = FakeRepo()  # implementiere einfaches Mockobjekt
    use_case = CreateOrderUseCase(repo)
    order = use_case.execute(1, [{"price": 10}, {"price": 5}])
    assert order.total == 15
```

**Problem:**  
- Fachlogik im Use Case  
- Kein fachliches Modell  
- Tests eher Integration als Unit  

---

### **Teil 2 – Clean Architecture + DDD**

#### Fachliche Erweiterungen:
- Einführung `Money` (Value Object)
- `OrderItem` und `Order` nutzen `Money`
- `total()`-Berechnung liegt in der Domain, nicht im Use Case
- `DiscountService` in separatem `pricing`-Kontext
- Repository als Interface + InMemory-Implementierung
- Use Case verbindet beide Kontexte

**Vorteil:**  
- Fachlich sprechender Code  
- Reine Unit-Tests möglich  
- Keine Infrastrukturabhängigkeit  

**Beispielhafte DDD-Tests:**
```python
def test_order_total():
    items = [OrderItem(1, Money(10)), OrderItem(2, Money(5))]
    order = Order(1, items)
    assert order.total() == Money(15)

def test_discount_service():
    result = DiscountService().apply_discount(Money(100), 10)
    assert result == Money(90)
```

**Integrationstest auf Application-Ebene:**
```python
def test_create_order_with_discount():
    repo = FakeOrderRepo()
    use_case = CreateOrderUseCase(repo, DiscountService())
    total = use_case.execute(1, [{"price": 10}, {"price": 20}])
    assert total.amount == 27  # 10% discount applied
```

---

## 4. Teststrategie

### **Testpyramide (explizit abbilden)**
Erstelle eine README mit dieser Pyramide und Erklärung:

| Ebene | Bereich | Anteil | Ziel |
|-------|----------|--------|------|
| Unit | Domain (Entities, Value Objects, Services) | 80 % | Schnell, stabil |
| Integration | Application Layer | 15 % | Überprüfung Zusammenspiel |
| End-to-End | API / CLI (minimal simuliert) | 5 % | Akzeptanztests |

---

## 5. README.md Inhalt (vom Agent erzeugen)
Erstelle automatisch eine **README.md**, die erklärt:

1. Was Clean Architecture ist  
2. Was die Schwächen bei Testbarkeit sind  
3. Wie DDD diese Schwächen löst  
4. Wie sich die Projektstruktur verändert  
5. Wie man `pytest` ausführt (`pytest -v`)  
6. Kurze Zusammenfassung der Testpyramide

---

## 6. Anforderungen an Code-Stil

- Verwende `dataclasses` wo sinnvoll (`Money`, DTOs)
- Keine Frameworks, kein ORM
- Saubere Imports (`from ...domain import ...`)
- Typannotationen verpflichtend
- `__init__.py`-Dateien anlegen, um Module importierbar zu machen
- Jeder Test läuft isoliert, keine globale Zustände

---

## 7. Zieldefinition
Das Projekt ist **fertig**, wenn:
- Alle Tests mit `pytest` grün sind  
- Code strukturell den zwei Phasen entspricht  
- Die README den Lernwert erklärt  
- Unterschiede zwischen Clean Architecture und Clean Architecture + DDD **im Code direkt sichtbar** sind  
- Fachlogik in Domain-Schicht testbar ist, Infrastruktur entkoppelt  

---

**Endziel:**  
Ein didaktisch sauberes, testbares Python-Projekt, das zeigt, wie DDD Clean Architecture verbessert –  
mit vollständigem Code, Tests, und klar erkennbarer Evolution innerhalb des Projekts.
