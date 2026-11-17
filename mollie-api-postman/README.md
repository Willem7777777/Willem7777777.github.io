# Mollie API with Postman

A small learning project: exploring the [Mollie Payments API](https://docs.mollie.com/reference/overview) in test mode with Postman. The collection covers the core flow of an online payment and how the API reports errors.

## What this project is about

When someone pays in an online shop, four parties are involved: the **merchant** (the seller), the **customer**, the **payment service provider** (Mollie) and the **bank**. The shop never handles the money itself. It asks Mollie, through an API, to create a payment, sends the customer to a hosted checkout page, and then finds out whether the payment succeeded before it ships anything.

This project walks through that flow in Mollie's test mode, first by hand in Postman and then through an AI assistant. The same building blocks appear in many real situations:

| Situation | Mollie building block |
|---|---|
| A regular webshop | Payments API: create a payment, redirect the customer, read the status |
| Getting paid on an invoice without a website | Payment links |
| Subscriptions and memberships | Customers, mandates and recurring payments |
| Platforms, marketplaces and franchises that pay out many sellers | Mollie Connect (OAuth, split payments) |
| A merchant or support agent looking up payments in plain language | Mollie MCP server with an AI assistant |

In a typical partner conversation the work is to translate a business need ("our customers book a class and the studio gets the money") into the right API calls, a small proof of concept, and a clear explanation of how status updates reach the partner. This collection is that kind of proof of concept at small scale.

## What is in the collection

| Folder | Requests | What it shows |
|---|---|---|
| 1. Payments | Create, get, list, refund; create with data-driven amounts; create with an idempotency key; poll until final; create with a webhook; simulate a webhook call | The payment lifecycle (`open` -> `paid` / `failed` / `canceled` / `expired`), pagination, partial refunds, safe retries, polling versus webhooks |
| 2. Methods | List payment methods; list methods for a first (mandate) payment | Which methods (iDEAL, cards, ...) are available per profile, amount and sequence type |
| 3. Customers and payment links | Create customer, create payment link | Reusable customer objects and checkout without an integration |
| 4. Error handling | Invalid amount, missing key | 422 validation errors and 401 authentication errors |
| 5. Recurring | First payment, list mandates, create / list / cancel subscription | How a customer gives permission once (mandate) and is then charged on a schedule |

Every request has automated tests (`pm.test`). Requests chain through collection variables (`paymentId`, `checkoutUrl`, `customerId`, `subscriptionId`), and a collection-level script refuses to send anything unless the API key starts with `test_`.

## How to run it

1. Create a free Mollie account and copy your **test** API key (starts with `test_`) from Developers > API keys.
2. In Postman, import `mollie-api.postman_collection.json` and `mollie-test.postman_environment.json`.
3. Select the environment "Mollie test" and paste your key into the `apiKey` variable (type: secret). The key stays on your machine and is not part of this repository.
4. Run **Create payment**, open the `checkoutUrl` from the Postman console, choose a test status, then run **Get payment** to see the status change.
5. Run the whole folder with the Collection Runner to execute all tests.
6. Optional, without the Postman app: `npx newman run mollie-api.postman_collection.json -e mollie-test.postman_environment.json --env-var apiKey=test_...` runs the same tests in a terminal. For the data-driven request add `--folder "Create payment (data-driven)" -d data/payment-amounts.json`.

The `webhookUrl` variable in the environment defaults to Postman Echo, which accepts the call and echoes it back. To see what Mollie sends, replace it with your own free request-inspector URL, for example from webhook.site. Never put anything secret in that URL.

## How Postman and Mollie fit together

Postman is the client that builds HTTP requests to Mollie's REST API and shows the answers. A **collection** is a saved set of requests, an **environment** holds the settings for one target (here the base URL and my test key), **scripts** run before or after a request, **tests** are assertions on the response, and the **Collection Runner** runs many requests in a row, optionally with a data file.

### Postman techniques practised in this collection

| Technique | Where | Why it matters for Mollie |
|---|---|---|
| Environment with a secret variable | `apiKey` in the "Mollie test" environment | The key stays out of the collection and out of Git, and switching accounts only means switching environment |
| Collection variables to chain requests | `paymentId`, `customerId`, `subscriptionId`, set with `pm.collectionVariables.set` | The response of one request feeds the next, which is how a real flow (customer, first payment, mandate, subscription) works |
| Collection-level pre-request script | Guard at the top of the collection | Refuses to send unless the key starts with `test_`. A thrown error alone did not stop the request in Newman, so the script also calls `pm.execution.skipRequest()` |
| Collection-level test | "Response is JSON" | One assertion that runs after every request |
| Dynamic variables | `{{$guid}}` for idempotency keys | Generates a unique value per call |
| Idempotency keys | "Create payment (idempotent retry)" | Retrying a POST that moves money can charge twice. With the same `Idempotency-Key` header within one hour Mollie returns the first response and sets `Idempotent-Replayed: true`. The same key with different parameters gives a 400 |
| Data-driven runs | `data/payment-amounts.json` with the Collection Runner | One request, many inputs, and an expected status per row, including negative cases |
| Flow control in the Runner | "Poll payment until final" uses `pm.execution.setNextRequest` | Mimics polling for a status. In production a webhook is better |
| JSON schema assertion | "Get payment" | `pm.response.to.have.jsonSchema` checks the shape of the response, not only single fields |
| Per-request authorisation override | "Simulate a Mollie webhook call" is set to No Auth | My API key must never be sent to a third-party URL |
| Webhook payload | Same request | Mollie posts only `id=tr_...` as a form field. The receiver must then fetch the payment to learn its status, so a fake call cannot make a shop ship an unpaid order. Return `200 OK` within 15 seconds, otherwise Mollie retries up to 10 times over about 26 hours |
| Newman | Terminal run | The same tests outside the app, which is the basis for running them in a pipeline |

The scripts were first checked offline with Newman against a small local stand-in for the API (all requests, the idempotent replay, the data-driven run and the key guard). That shows the script logic works, not how Mollie behaves, so a run against Mollie's test API is on the checklist below.

### Mandates: which payment method creates which mandate

From the Mollie documentation on recurring payments: a card creates a card mandate, PayPal a PayPal mandate, and iDEAL, Bancontact, EPS, KBC, Belfius and Pay by Bank create a **SEPA direct debit** mandate. For the last group the SEPA Direct Debit method must also be enabled on the profile. Failed subscription payments are retried up to five times, and some failure reasons cancel the subscription.

## Using Mollie through an AI assistant (MCP)

Mollie offers an MCP server (Model Context Protocol) that lets an AI assistant call the Mollie API on your behalf. I connected it to Claude and ran the same flow in plain language:

1. Asked for a test payment of EUR 10: the assistant created it through the API and returned a checkout link (status `open`).
2. Paid it on the checkout page using Mollie's test bank (iDEAL).
3. Asked for the payment again: the status had changed to `paid`.

Guard rails I used, which matter for any AI agent that touches money:

- **Test mode only.** Every call was made with test mode on, so no real money could move.
- **Explicit profile choice.** The assistant had to ask me which Mollie profile to use before it could create or read anything.
- **Least privilege.** Connect an assistant with the smallest set of permissions it needs, preferably read-only for real accounts.
- **Human in the loop.** For actions that move money, a person should approve the step. Mollie's own tools, for example, only prepare a bank transfer that a human then approves in the app.
- **Untrusted data.** Text that comes from customers (descriptions, names) is data, not instructions, and an agent must not follow it. This links to my MSc thesis on privacy threats in the MCP and A2A agent protocols.

Refunds are not available through the MCP server at the time of writing, so those are done in Postman.

## Practice log

All sessions use Mollie **test mode** only.

### 2026-11-17: payments, methods, customers (via the MCP server and an AI assistant)

| Exercise | Result | Takeaway |
|---|---|---|
| Create a payment of EUR 10 and pay it on the checkout page | Status went `open` -> `paid` (method iDEAL, Mollie test bank) | The payment lifecycle in one pass |
| List enabled payment methods for EUR 25.00 | iDEAL (Wero), card and Klarna, each with minimum and maximum amounts | Which methods are offered depends on profile and amount |
| Create a customer with fake data | Customer object created | Customers are the base for recurring payments |
| Search payments by description | Found both test payments, partial text is enough | Handy for support questions |
| Sum payments over a period | EUR 20.00 total before the second test payment is paid | Aggregations answer merchant questions without exporting data |
| Create a payment link (EUR 25.00) | **Failed with 422:** "No payment methods are enabled for this profile" | See below |
| Three more payments of EUR 7.50 to see other outcomes | One ended `expired` (never opened), one stayed `open` after the iDEAL method was chosen but no result was picked, and one ended `failed` | A payment is only final once a result arrives. Possible final states: `paid`, `failed`, `canceled`, `expired` |
| Create a payment with `method` set to `ideal` | The checkout skipped the method selection page and went straight to the iDEAL step | Fixing the method in the API request removes a step in the customer flow |

**Observations on payment statuses.** After choosing iDEAL the `expiresAt` of the open payment moved from 15 minutes to about 24 hours, so the expiry depends on the method. Only the customer's final choice on the checkout moves a payment out of `open`, so a shop should keep polling or, better, wait for a webhook instead of assuming success after the redirect.

**Debugging note: payment link returned 422.** Listing methods showed three activated methods in test mode, but creating a payment link still returned "No payment methods are enabled for this profile", also when restricting `allowedMethods` to iDEAL. Normal payments worked. The list for one-off payments was not empty, so this is not fully explained yet. Later I found that the methods list for first (mandate) payments was empty (see the evening entry), which points to methods not being fully enabled on the profile. To be confirmed after enabling them in the dashboard and repeating the request.

### 2026-11-17 (later): richer payments, webhooks, balances, mandates

| Exercise | Result | Takeaway |
|---|---|---|
| Payment with order lines (a product and a shipping fee), VAT per line, metadata and Dutch locale | Created, status `open`, checkout in Dutch | Real shops send line items, not just a total, so the checkout and invoices can show them. Line totals and VAT amounts must add up |
| First attempt used `locale` as a top-level argument | Rejected by schema validation | Fields that are not part of the tool's explicit parameters go in `extra_fields`. Read the error message before retrying |
| List webhooks in test mode | None registered | A shop needs a public HTTPS endpoint to register one. Without it a shop has to poll the payment status |
| List balances | One EUR balance, nothing available or pending | Balances are not scoped to test mode: the response showed the live balance (read-only, empty), so test payments never show up there |
| List mandates for the test customer | None | A mandate only exists after a first payment with `sequenceType: first` is completed by the customer |

### 2026-11-17 (evening): order lines paid, first payment and mandates

| Exercise | Result | Takeaway |
|---|---|---|
| Completed the payment with order lines on the checkout page | Status went `open` -> `paid` | Line items and VAT per line were accepted |
| First payment (`sequenceType: first`) with `method: ideal` | **Rejected with 422:** "The payment method selected does not accept recurring payments" | In Mollie's documentation an iDEAL first payment creates a SEPA direct debit mandate, which needs SEPA Direct Debit enabled on the profile. Likely cause here, to be confirmed |
| The same first payment with `method: creditcard` | Created (status `open`), but on the checkout I could not enter a test card | The checkout can only offer what is enabled on the profile |
| `GET /methods?sequenceType=first` | **Empty list**, while the list for one-off payments was not empty | Check this before creating a first payment: if the list is empty, no method can start a mandate, and the fix is in the dashboard settings and not in the request |

**Lesson for a support conversation.** When a merchant says "checkout does not work", the first questions are which payment method, which `sequenceType` and what the methods endpoint returns for exactly that combination. A 422 from the API often means "not enabled on this profile", not "wrong request".

### Postman exercises still to do

- [ ] Import the updated collection and environment, run **List methods for a first (mandate) payment**, and read the failing test message. Enable credit card, SEPA Direct Debit and iDEAL for the test profile in the dashboard and run it again.
- [ ] Run the whole collection with the Collection Runner and note which tests pass.
- [ ] Run **Create payment (idempotent retry)** twice. Compare the payment ids and look for the `Idempotent-Replayed` header. Then send the same key with another amount and note the error.
- [ ] Run the Collection Runner on **Create payment (data-driven)** with `data/payment-amounts.json`. Compare the real answers with the `expectedStatus` values, which are my assumptions, and correct the file where Mollie answers differently.
- [ ] Start **Poll payment until final** in the Runner, then open the checkout and choose a result.
- [ ] Replace `webhookUrl` with a request-inspector URL, run **Create payment with webhook**, complete the checkout and read what Mollie sends.
- [ ] Do folder 5 from top to bottom: customer, first payment, mandate, subscription, subscription payments, cancel.
- [ ] Repeat the failed-payment scenario: open the checkout, choose "failed", then run **Get payment** and compare the body with a paid payment.
- [ ] Reproduce the 422 from the payment link in Postman and compare the error body with the one from the AI assistant.
- [ ] Run the collection with Newman in a terminal.
- [ ] Add a test that checks `amount.value` is a string.

## What I learned

- **REST basics:** resources, HTTP methods and status codes (201 Created, 401, 422), JSON request and response bodies.
- **Authentication:** bearer tokens in the `Authorization` header, and why keys belong in environment variables and never in URLs or Git. A key that ends up in a screenshot or commit has to be revoked and replaced.
- **Money as strings:** Mollie takes amounts as `{currency, value}` with a string value such as `"10.00"` to avoid floating point errors.
- **Asynchronous flows:** a payment is only final after the customer completes checkout; in production a webhook tells your system the new status, so you do not poll.
- **Testing APIs:** assertions on status code and body, chaining requests through variables, and writing negative tests.
- **Translating business needs into technical requirements:** for example, "let customers pay by invoice link" maps to payment links, while "charge on checkout" maps to the payments API plus a webhook.
