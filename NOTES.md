## React choice

I used React for the client.

---

## Money and rounding

Money stays in integer paise. Fractional paise are rounded down.

---

## Second discount

A second discount is rejected with `409`; it does not replace the first one.

---

## Monthly partner settlement

Select paid orders for the month and sum their stored `partner_amount_paise` by partner, without reading current discount configuration.

---

## Stored on each order

The order keeps an immutable snapshot of the discount code, percentage, cap, funding ratios, discount amount, and each party's funded amount.

---

## AI mistake

The AI briefly rendered `OrderSummary` twice in one test. I caught the duplicate-region problem and removed the extra render.

---

## Serious production concerns

I would add `paid_at` and settlement tracking, enforce unique payment IDs, and prevent discount changes once payment starts or finishes. Without these, payments, totals, or settlements could become inconsistent.

---

## Approximate time

About 40 minutes: 20 on the backend, 10 on React and tests, and 10 on review, prompt history, and notes.
