<div align="center">

# Logistics 4 Odoo

**A batch-processing engine for shipping logistics.**

From customer orders to printable loading sheets — group orders by zone, build pallets, assign trucks, and dispatch, all driven from a lightweight Flask dashboard.

<sub>Python · Flask · SQLAlchemy · PostgreSQL</sub>

</div>

---

> [!NOTE]
> **`app.py`, the Flask interface (`templates/`) and README.md were generated with AI assistance**, due to limited familiarity with Flask and time constraints. The core logic — the data model and the three engine stages (`grouper.py`, `packer.py`, `dispatcher.py`) — is hand-written. The web layer is a thin wrapper to run and visualize that logic.

---

## Overview

The system takes validated customer orders and moves them through three sequential stages. Each stage reads the state left by the previous one in PostgreSQL and pushes it forward.

```
  Orders            Stage 1            Stage 2              Stage 3            Shipments
(validated)  ──►   Grouping    ──►   Palletizing   ──►   Dispatching   ──►   + loading
                (zone / ETA win.)    (bin-packing)       (truck choice)        sheets
```

| Stage | Module | What it does |
|------:|--------|--------------|
| **1 · Group** | `grouper.py` | Groups `validated` / `ready` orders from the same geographic zone whose ETAs fall within one window (48 h by default). A `ready` order opens a group (reference ETA pinned to 08:00 on the delivery day); a `validated` order joins its zone's group if its ETA is within the window, otherwise it opens a new one. Writes `groups` rows (`status = open`) and sets `orders.group_id`. |
| **2 · Palletize** | `packer.py` | For each open group, distributes order lines into pallets using a first-fit rule. Standard pallet 1.2 × 0.8 m, max height 2.0 m, max weight 1500 kg. An oversized product gets its own `closed` pallet. Writes `pallets` and `pallet_lines`, then marks the group `packed`. |
| **3 · Dispatch** | `dispatcher.py` | For each packed group, computes total weight / length / width and pallet count, then picks the **smallest available truck** that can carry it (a heuristic accounting for truck width classes and an estimate of the length the pallets occupy). Creates a `shipment` (`status = planned`) with a per-pallet load order, marks pallets `loaded` and the group `shipped`. |

The web app (`app.py`) runs these three stages, shows orders / groups / pallets / shipments / fleet in tabs, and opens a detailed **loading sheet** for any shipment.

## Project structure

```
logistics_odoo/
├── app.py                  # Flask app: dashboard, stage triggers, loading-sheet page
├── db.py                   # SQLAlchemy engine + scoped session
├── models.py               # ORM models mapped to the `logistics` schema
├── grouper.py              # Stage 1 — order grouping
├── packer.py               # Stage 2 — pallet building
├── dispatcher.py           # Stage 3 — truck assignment
├── tables_create.sql       # `logistics` schema + core tables
├── groups.sql              # `groups` table + `group_id` columns on orders/pallets
├── demo_data.sql           # Demo dataset
└── templates/
    ├── dashboard.html      # Dashboard (tabs, user selector, 3-stage engine)
    ├── shipment.html       # Loading sheet for one shipment
    └── zones.html          # Geographic zones view
```

### Data model

Schema `logistics`. Core tables: `geo_zone`, `products`, `users`, `vehicles`, `orders` / `order_lines`, `groups`, `pallets` / `pallet_lines`, `shipments` / `shipment_pallet`. Statuses are enforced by `CHECK` constraints:

| Entity | Lifecycle |
|--------|-----------|
| `orders` | `draft → validated → in_preparation → ready → grouped → shipped` |
| `groups` | `open → packed → shipped` |
| `pallets` | `open → closed → loaded` |
| `shipments` | `planned → loading → departed` |

## Requirements

- Python 3.10+ (the dispatcher uses `match` / `case`)
- PostgreSQL
- `flask`, `sqlalchemy`, `psycopg2` (or `psycopg2-binary`)

```bash
pip install flask sqlalchemy psycopg2-binary
```

## Setup

**1. Create the database** — run the SQL scripts in order:

```bash
psql -d postgres -f tables_create.sql
psql -d postgres -f groups.sql
psql -d postgres -f demo_data.sql   # optional: demo data
```

**2. Configure the connection** in `db.py`:

```python
engine = create_engine("postgresql://postgres:Root@localhost:5432/postgres")
```

Adjust user, password, host and database name to your environment.

**3. Run the app:**

```bash
python app.py
```

The development server starts at **http://127.0.0.1:5000**.

## Usage

From the dashboard:

**1.** Pick your name in the **"You are:"** bar — it's recorded as the author of the actions (`created_by`).

**2.** Run the three engine stages in order: **Group** (adjustable ETA window), **Palletize**, then **Dispatch**.

**3.** Open the **Shipments** tab and click **Loading sheet** to see a shipment in detail: truck, loaded weight, used length, and each pallet expandable down to its lines (order, product, quantity, weight).

The three stages can also run from the command line, independently of the UI:

```bash
python grouper.py      # grouping
python packer.py       # palletizing
python dispatcher.py   # dispatching
```

## Notes

- The server runs with `debug=True` — fine for development, not for production as-is.
- The grouping window is passed via `run_grouping(session, window_hours=...)`; the UI offers 24 / 48 / 72 / 96 h.
- `app.secret_key` in `app.py` is a development key — replace it for any real deployment.
- Database credentials are currently hard-coded in `db.py`; move them to environment variables before deploying.
