# Bug Report
**What:** A complete record of a defect — how to reproduce it, what went wrong, severity, root cause, fix applied, and the regression test that prevents recurrence.  
**Who fills it in:** Reporter fills sections 1–5 on discovery. Assignee fills sections 6–8 on resolution.  
**Cross-references:** `.claude/templates/feature-spec.md`, `.claude/checklists/security.md` (for security bugs)

---

## Bug Metadata

| Field | Value |
|-------|-------|
| Bug ID | `<BUG-0314>` |
| Title | `<Checkout total rounds down to $0.00 when coupon covers >99 % of price>` |
| Reported by | `<@reporter-name>` |
| Reported date | `<YYYY-MM-DD>` |
| Assigned to | `<@engineer-name>` |
| Component / service | `<checkout-service / PricingCalculator>` |
| Severity | `<P0 — data loss | P1 — major | P2 — minor | P3 — cosmetic>` |
| Priority | `<Critical | High | Medium | Low>` |
| Status | `<New | In Progress | In Review | Fixed | Closed | Won't Fix>` |
| Target fix release | `<v2.4.1>` |
| Security-related? | `<Yes / No>` — if Yes, treat as confidential and follow `.claude/checklists/security.md` |

---

## 1. Summary

> One or two sentences: what fails, in what context, and what the visible impact is.

`<When a coupon code reduces the order subtotal to less than $0.01, the pricing calculator truncates the result to $0.00 instead of rounding to $0.01 or applying a floor. This allows users to complete orders without being charged.>`

---

## 2. Environment

> Provide exact versions, platform, and configuration details so the bug can be reproduced reliably.

| Field | Value |
|-------|-------|
| App version / commit | `<v2.4.0 / git sha abc123>` |
| Environment | `<Production | Staging | Local>` |
| OS / runtime | `<Node 20.11 on Ubuntu 22.04 / iOS 17 / Android 14 / macOS 14>` |
| Browser (if web) | `<Chrome 125 / Safari 17>` |
| Device (if mobile) | `<iPhone 15 Pro / Pixel 8>` |
| Region / locale | `<us-east-1 / en-US>` |
| Feature flags active | `<checkout_v2=true, new_pricing=false>` |
| User account type | `<Free tier / Pro / Admin>` |

---

## 3. Steps to Reproduce

> Number every step. Include exact inputs, URLs, and button labels. Someone who has never seen this bug must be able to reproduce it from these steps alone.

1. Log in as any user with a free account.
2. Add item `<SKU: WIDGET-001, price: $0.50>` to cart.
3. At checkout, apply coupon code `<SAVE99>` (99 % discount).
4. Observe the order total displayed.
5. Click **"Place Order"**.

**Reproducible:** `<100 % | intermittent ~X %>` with the steps above.

---

## 4. Expected vs. Actual Behavior

> Be precise — "it doesn't work" is not enough. State the exact output you expected and the exact output you got.

**Expected:**
`<Order total should display $0.01 (minimum billable amount). The payment processor should charge $0.01 and the order should be marked paid.>`

**Actual:**
`<Order total displays $0.00. Stripe receives a charge for $0 which it accepts, and the order is marked paid without any payment being collected.>`

**Screenshot / log snippet:**
```
[2026-06-25T14:32:01Z] INFO  PricingCalculator: subtotal=0.50 discount=0.4950 final=0.005
[2026-06-25T14:32:01Z] INFO  PricingCalculator: rounded_final=0.00 (Math.floor applied)
[2026-06-25T14:32:01Z] INFO  StripeCharge: amount=0 currency=usd status=succeeded
```
`<Attach screenshot or link to Sentry event: https://sentry.io/...>`

---

## 5. Impact Assessment

> Who is affected, how many users, and what is the business or data impact?

- **Users affected:** `<Any user applying a coupon ≥ 99 % discount — estimated X orders in past 30 days>`
- **Data impact:** `<X orders processed at $0; revenue loss estimated at $Y>`
- **Security impact:** `<Users can obtain paid products for free — financial exploit>`
- **Workaround available:** `<Yes — temporarily disable SAVE99 coupon code in admin panel>`
- **Workaround applied:** `<Yes, YYYY-MM-DD HH:MM UTC by @devops>`

---

## 6. Root Cause Analysis

> Filled in by the assignee after investigation. Identify the exact line(s) of code, configuration, or system interaction that caused the bug.

**Root cause:**
`<In src/pricing/calculator.ts line 87, Math.floor() is applied to the final price instead of Math.round(), and there is no minimum-price floor guard. When discount * subtotal results in a value < $0.005, floor() truncates to $0.00.>`

**Contributing factors:**
- `<No unit test covering discount > 99 % case>`
- `<Code review missed the floor vs. round distinction>`
- `<Stripe silently accepts $0 charges rather than returning an error>`

**Code location:** `<src/pricing/calculator.ts:87>`, `<src/pricing/calculator.test.ts — missing test case>`

---

## 7. Fix

> Describe the fix applied. Link to the PR/commit. Explain why this fix is correct and does not introduce new issues.

**Fix description:**
`<Replace Math.floor() with Math.round() on line 87. Add a minimum-price guard: if (finalPrice < MINIMUM_CHARGE) finalPrice = MINIMUM_CHARGE where MINIMUM_CHARGE = 0.01. Update the Stripe charge assertion to reject amount = 0.>`

**Fix PR / commit:** `<https://github.com/org/repo/pull/456 — merged YYYY-MM-DD>`

**Why this fix is safe:**
- `<Math.round() is correct for currency rounding to 2 decimal places>`
- `<Minimum charge guard is consistent with Stripe's minimum charge policy>`
- `<Change is additive — no existing passing test is broken>`

**Side effects / follow-up:** `<Finance team to issue refunds / credits for affected orders — tracked in BUG-0314-followup>`

---

## 8. Regression Test

> Describe the test(s) added to prevent this bug from recurring. Include file path and test name.

**Test file:** `<src/pricing/calculator.test.ts>`

**Test cases added:**

| Test name | Input | Expected output |
|-----------|-------|----------------|
| `<coupon reduces total below minimum charge>` | `<subtotal=$0.50, discount=99%>` | `<finalPrice=$0.01>` |
| `<coupon reduces total to exactly zero>` | `<subtotal=$1.00, discount=100%>` | `<finalPrice=$0.01>` |
| `<coupon reduces total by 50%>` | `<subtotal=$10.00, discount=50%>` | `<finalPrice=$5.00 (unchanged behavior)>` |
| `<Stripe charge rejects amount=0>` | `<amount=0>` | `<throws MinimumChargeError>` |

**CI run confirming tests pass:** `<https://ci.example.com/run/789>`

---

## 9. Verification

> Confirm the fix works in each environment before closing the bug.

| Environment | Verified by | Date | Result |
|-------------|-------------|------|--------|
| Local | `<@assignee>` | `<YYYY-MM-DD>` | ☐ Pass |
| Staging | `<@qa-lead>` | `<YYYY-MM-DD>` | ☐ Pass |
| Production | `<@qa-lead>` | `<YYYY-MM-DD>` | ☐ Pass |

**Bug closed by:** `<@name>` on `<YYYY-MM-DD>`
