# RAYY take-home: partner discounts

Thanks for doing this. It is about two and a half hours; if you reach three
hours, stop and write in `NOTES.md` what is left.
Use any tools you like, including AI; we care about what you ship and how you
checked it, not how it was typed.

## What you have

A small FastAPI service with one MongoDB collection, `orders`, a stub
payment-gateway client, seed data, and a test suite that currently passes.
Run it with `docker compose up`, or without Docker (Python 3.11+) `make test`
uses an in-memory Mongo (note: the in-memory Mongo does not support
transactions; if you use them, say so in NOTES.md and we will run your tests
against a real replica set). All money in this codebase is integer paise.

## What to build

1. `POST /orders/{order_id}/apply-discount` with body `{ "code": "..." }`.
   Look the code up, apply it to the order, and record what was applied. Codes
   have a percentage, a cap in paise, an expiry, and a funding split between the
   partner and RAYY (for example 70/30).
2. `POST /webhooks/payment`. The gateway calls this when a payment succeeds,
   with a payment id, an order id and the amount charged. Mark the order paid
   and record the payment. Handle the gateway as documented in
   `app/gateway.py`; treat this as a production payment path.
3. Tests for both, in the existing suite.
4. A small client, in Flutter or React: pick one, you do not need both, and
   say in `NOTES.md` which one you chose. Starters are in `client/flutter/`
   and `client/web/`; each has one passing test (`npm ci && npm test` in
   `client/web/`, `flutter pub get && flutter test` in `client/flutter/`).
   Given an order
   (the shape is in the starter):
   - write `formatPaise`, which turns integer paise into rupees with Indian
     digit grouping and exactly two decimals, using integer maths only:
     199999 is `₹1,999.99`, 12345678 is `₹1,23,456.78`, 5 is `₹0.05`. It
     throws on input it cannot format (a non-integer in TypeScript, a
     negative amount in Dart);
   - show the subtotal, the discount code and amount when there is one, and
     the total, all through `formatPaise`;
   - add a button labelled "Pay" that is disabled while a payment is in
     progress (it still reads "Pay"); it reads "Paid", and stays disabled,
     only when the order's status is `paid`;
   - if the payment fails, show an error (React: an element with
     `role="alert"`; Flutter: text containing "Payment failed") and let the
     customer try again.

   Add tests for it in the starter's test setup. Keep the starter's file
   names, exports and the contract in its doc comments (Flutter: an
   `ElevatedButton`).
5. In `NOTES.md` (short bullets are fine), five lines: partners are settled
   monthly for their share of discounts, and a partner's split ratio can
   change next month. What do you store per order so this month's settlement
   is correct, and what does the settlement query read?
6. Also in `NOTES.md`: the one thing your AI tool got wrong that you caught;
   anything in your submission you would not yet trust in production; and
   roughly how long this took and where the time went.

Every item is needed. The client task (about 20 minutes) and `prompts/` are
required for a pass, so if time is short do a smaller version of each rather
than skipping one.

Two things are deliberately not specified. Decide, and say what you decided
in `NOTES.md`: how you round when a percentage produces a fraction of a
paisa, and what happens when a second discount code is applied to an order
that already has one.

## Submitting

Within 48 hours, push your work to your own GitHub (public, or private with
read access for the account named in our email) and send us the link. Include
`NOTES.md` and your AI prompt history in a `prompts/` folder (a raw export or
screenshots is fine; no need to tidy it); we expect it with every submission.
If your tool does not keep a history, copy or screenshot the conversation as
you go. A submission without `prompts/` cannot pass. Keep pricing and money
logic out of the route handlers; we read the structure as well as the
behaviour.
