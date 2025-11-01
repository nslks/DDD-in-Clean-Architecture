# Clean Architecture zu DDD

Dieses Projekt demonstriert schrittweise, wie eine klassische Clean-Architecture-Implementierung durch Domain-Driven Design (DDD) fachlich belastbarer und besser testbar wird. Beide Varianten liegen nebeneinander im Ordner `src`, sodass Unterschiede unmittelbar sichtbar sind.

## Clean Architecture – Ausgangspunkt
- Klare Layer (Application, Domain, Infrastructure) trennen Technik und Fachlogik.
- Use Cases orchestrieren Abläufe und greifen direkt auf Repositories zu.
- Im Baseline-Beispiel (`src/clean_architecture/`) steckt die Kernlogik – etwa das Aufsummieren von Preisen – im Use Case. Die Domain kennt kaum Fachmodellierung.

### Schwächen bei der Testbarkeit
- Tests müssen Use Case + Repository gemeinsam ausführen → Integration statt Unit.
- Preislogik ist schwer isolierbar, weil sie im Application Layer steckt.
- Primitive Datentypen (`dict`, `float`) als Träger fachlicher Werte machen Fehler (z. B. Rundung) wahrscheinlicher.

## DDD als Ergänzung
- Value Objects (`Money`) kapseln fachliche Invarianten wie Währungsrundung.
- Domain Entities (`Order`, `OrderItem`) tragen die Fachlogik (`total()`).
- Domain Services (`DiscountService`) modellieren Regeln außerhalb einzelner Aggregate.
- Repositories werden über stabile Interfaces entkoppelt; der Use Case arbeitet nur noch mit Domainobjekten.

Das Ergebnis (`src/clean_architecture_ddd/`) erlaubt echte Unit-Tests innerhalb der Domain und hält den Application Layer schlank. Infrastrukturdetails (hier: In-Memory-Repository) lassen sich leicht austauschen.

## Projektstruktur
```
src/
├── clean_architecture/               # Baseline
│   ├── domain/entities.py
│   ├── application/create_order.py
│   └── infrastructure/order_repository_sql.py
└── clean_architecture_ddd/           # DDD-Weiterentwicklung
    ├── ordering/
    │   ├── domain/{entities,value_objects,repositories}.py
    │   ├── application/use_cases.py
    │   └── infrastructure/order_repository_inmemory.py
    └── pricing/domain/discount_service.py
tests/
├── clean_architecture/test_create_order.py
└── clean_architecture_ddd/
    ├── ordering/{test_order_entity,test_order_usecase}.py
    └── pricing/test_discount_service.py
```

## Virtuelle Umgebung
```bash
python3 -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install pytest
```

## Tests ausführen
```bash
pytest -v
```

## Testpyramide

| Ebene        | Bereich                                      | Anteil | Ziel                        |
|--------------|----------------------------------------------|--------|-----------------------------|
| Unit         | Domain (Entities, Value Objects, Services)   | 80 %   | Schnell, stabil             |
| Integration  | Application Layer                            | 15 %   | Zusammenspiel absichern     |
| End-to-End   | API / CLI (minimal simuliert)                | 5 %    | Fachliche Akzeptanz prüfen  |

## Optionale CLI
`main.py` zeigt exemplarisch, wie der DDD-Use-Case aus einer einfachen CLI aufgerufen werden kann:

```bash
python main.py --user 1 --items '[{"product_id": 1, "price": 10}, {"product_id": 2, "price": 20}]' --discount 10
```
