# Clean Architecture → Domain-Driven Design

Dieses Projekt stellt zwei Implementierungen eines Bestell-Workflows nebeneinander: eine klassische Clean Architecture als Ausgangspunkt und eine erweiterte Variante, in der Domain-Driven Design (DDD) die Fachlichkeit in den Mittelpunkt rückt.

## Clean Architecture in Kürze
- **Stärken**: Saubere Layer (Application, Domain, Infrastructure), klare Abhängigkeitsrichtung, austauschbare Infrastruktur.
- **Wofür sie gut ist**: Trennung von Anwendungslogik und Technik, bessere Wartbarkeit, klare Use-Case-orientierte Abläufe.
- **Was fehlt**: Die Domain bleibt dünn. Fachregeln landen im Application Layer, primitive Typen repräsentieren Fachwerte, Tests prüfen eher Flüsse als Sprache und Regeln.

## Tests vs. Fachliche Tiefe
- In der Baseline-Version (`src/clean_architecture/`) addiert der Use Case Preise direkt und speichert Orders über ein Repository.
- Tests müssen Use Case und Repository gemeinsam ausführen – der Fokus liegt auf Integration statt auf fachlicher Präzision.
- Ohne explizite Domain-Modelle lassen sich Invarianten, Rundungen oder komplexere Regeln schwer isoliert prüfen.

## Was ist Domain-Driven Design?
- **Ubiquitous Language**: Gemeinsame Fachsprache zwischen Domänenexperten und Entwicklern.
- **Modelle im Code**: Value Objects, Entities und Aggregate transportieren Regeln und Zusammenhänge.
- **Bounded Contexts**: Fachlich kohärente Bereiche werden getrennt gedacht und implementiert.
- **Services & Repositories**: Domänenlogik bleibt unabhängig von Infrastruktur.

## Übergang zur DDD-Variante
- Das DDD-Beispiel (`src/clean_architecture_ddd/`) verschiebt Logik aus dem Application Layer in die Domain:
  - `Money` kümmert sich um Währungsrundung und Vergleichbarkeit.
  - `OrderItem` validiert Mengen und kann bestehende Posten zusammenführen.
  - `Order` berechnet Summen, verwaltet Items und bleibt Herr über seine Invarianten.
  - `DiscountService` kapselt fachliche Rabatte im Pricing-Kontext.
  - Der Use Case orchestriert nur noch Domainobjekte und verbindet Ordering und Pricing.
- Die Tests fokussieren sich jetzt auf die Domain selbst – Infrastruktur wird substituierbar.

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

## Virtuelle Umgebung & Abhängigkeit
```bash
python3 -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install pytest
```
Die vorbereitete Umgebung `.venv/` liegt bereits im Projekt – einfach aktivieren und Pytest installieren.

## Tests ausführen
```bash
pytest -v
```

## Optionale CLI
`main.py` ruft den DDD-Use-Case aus einer einfachen CLI heraus auf:
```bash
python main.py --user 1 --items '[{"product_id": 1, "price": 10}, {"product_id": 2, "price": 20}]' --discount 10
```
