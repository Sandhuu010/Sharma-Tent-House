# Sharma Tent House CLI System — Phase 1

## Overview

This is a CLI-based inventory management system for Sharma Tent House.

Phase 1 implements the Item Catalogue system where users can:

- Add items
- List items
- Search items
- Update items
- Delete items

Data is stored permanently in a JSON file.

---

# Features

## Add Item
Add new inventory items with:
- Auto-generated item ID
- Name
- Quantity
- Rate

Example:

```text
ITEM_001
Folding Chairs
200
5.00
```

---

## List Items

Displays all stored items.

---

## Search Item

Search items using:
- partial names
- uppercase/lowercase insensitive matching

Example:
- chair
- CHAIR
- folding

All work correctly.

---

## Update Item

- Search item by partial name
- Choose matching item
- Blank input keeps old value

---

## Delete Item

- Search item by partial name
- Shows matching items
- Confirmation before delete

---

# Project Structure

```text
SharmaTentHouse/
│
├── main.py
├── items.py
├── storage.py
├── README.md
├── TESTS.md
├── .gitignore
│
└── data/
    └── items.json
```

---

# Data Storage

All items are stored in:

```text
data/items.json
```

Example:

```json
[
    {
        "item_id": "ITEM_001",
        "name": "Folding Chairs",
        "total_quantity": 200,
        "rate": "5.00"
    }
]
```

---

# Validation

The program prevents:
- empty names
- invalid quantity
- negative quantity
- invalid rate
- negative rate

The program never crashes on invalid user input.

---

# Auto Item IDs

IDs are automatically generated:

```text
ITEM_001
ITEM_002
ITEM_003
```

Deleted IDs are not reused.

---

# Requirements

- Python 3.x

---

# How To Run

Open terminal in project folder:

```bash
python main.py
```

---

# Future Scope

Upcoming phases will include:
- bookings
- availability engine
- customers
- payments
- delivery & return tracking
- reports
- maintenance management

---
