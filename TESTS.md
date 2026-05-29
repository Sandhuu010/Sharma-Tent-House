# Phase 1 Tests — Sharma Tent House

This file contains manual test cases for Phase 1.

---

# Test 1 — Fresh Start

## Steps

1. Delete `items.json`
2. Run program
3. Choose "List Items"

## Expected Result

```text
No items yet.
```

## Result

PASS

---

# Test 2 — Add Item

## Steps

1. Add item:
   - Name: Folding Chairs
   - Quantity: 200
   - Rate: 5

2. Exit program
3. Run again
4. List items

## Expected Result

Item should still exist after restart.

## Result

PASS

---

# Test 3 — Invalid Quantity

## Steps

At quantity prompt enter:

```text
abc
```

## Expected Result

Program should reject input without crashing.

## Result

PASS

---

# Test 4 — Negative Quantity

## Steps

Enter:

```text
-5
```

## Expected Result

Program should reject negative value.

## Result

PASS

---

# Test 5 — Invalid Rate

## Steps

Enter:

```text
abc
```

at rate prompt.

## Expected Result

Program rejects invalid rate without crashing.

## Result

PASS

---

# Test 6 — Search Item

## Steps

Search:

```text
chair
```

## Expected Result

Matching chair items displayed.

## Result

PASS

---

# Test 7 — Case Insensitive Search

## Steps

Search:
- CHAIR
- chair
- Chair

## Expected Result

All return same matching items.

## Result

PASS

---

# Test 8 — Update Item

## Steps

1. Search item
2. Update quantity/rate
3. Exit
4. Run again
5. List items

## Expected Result

Updated values persist after restart.

## Result

PASS

---

# Test 9 — Delete Item

## Steps

1. Delete item
2. Confirm yes
3. List items

## Expected Result

Item removed successfully.

## Result

PASS

---

# Test 10 — Invalid Search

## Steps

Search:

```text
xyz
```

## Expected Result

Program should:
- show no match found
- show available items list

## Result

PASS

---

# Test 11 — Invalid JSON

## Steps

Manually corrupt `items.json`

## Expected Result

Program should:
- show JSON error
- not crash

## Result

PASS