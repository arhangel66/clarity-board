# FT-001 Decision Log

## Round 1 (2026-03-07)

### Topic: Landing messaging about pricing and limits

- **Observed contradiction:**
  - Product docs describe a freemium model with credits/limits and later monetization.
  - Current landing copy still implies the product is free without meaningful limits.
- **Current misleading copy in code:**
  - `Начать мыслить ясно (бесплатно)`
  - `Навсегда бесплатный тариф`
  - `Это бесплатно? Да, начните с бесплатных сессий. Банковская карта не требуется.`

### User direction
- The landing should no longer imply the app is free forever.
- The homepage should explain that some amount of usage is free, but the product is not permanently unlimited/free.
- Visual/product inspiration: pricing presentation similar to IdeaKiller-style section:
  - recurring free allowance
  - paid tiers or packs for additional usage
  - pricing explained directly on the landing page

## Round 2 (2026-03-07)

### Answers received

- **Free tier:** 1 session is free.
- **Reset logic:** free usage refreshes every month.
- **Pricing UI:** yes, add a dedicated pricing section on the homepage.
- **Public prices (candidate):**
  - `$10/month` for unlimited usage
  - `$100` lifetime
- **Unit language preference:** talk about `sessions`, not `credits`, to avoid mental overhead.

### Remaining ambiguity

- There is still a product-model conflict:
  - one answer suggests selling additional sessions
  - another answer suggests selling unlimited monthly access and lifetime access
- These are different monetization models and lead to different landing structures/copy.

## Round 3 (2026-03-07)

### Answers received

- `Credits` should be removed from user-facing positioning.
- Public packaging should be expressed in `sessions`.
- The monetization task/docs around credits likely need to be rewritten later.

### Updated working model

- Free allowance exists and refreshes monthly.
- Paid offer should be presented as:
  - monthly unlimited plan
  - lifetime plan
- The landing should explain pricing directly instead of implying permanent free use.

## Round 4 (2026-03-07)

### Final clarification

- Free allowance is **3 sessions total**, not monthly.
- Public pricing direction:
  - `3 free sessions`
  - `$10/month` unlimited
  - `$100` lifetime
- User-facing wording should use `sessions`, not `credits`.

### Resulting decision

- Landing/pricing communication must move from a `credits` framing to a `sessions + plans` framing.
- The public homepage should include a visible pricing section.
- Existing monetization docs/tasks built around `credits` are now stale and must be updated before implementation.

### Remaining implementation questions

- What exactly counts as a consumed session in product logic: board creation, first AI interaction, or completed board?
- Does the initial launch show real checkout or still start with intent-tracking UI before billing is implemented?

### Working interpretation
- Preferred positioning is moving toward:
  - free usage allowance
  - explicit limits
  - paid expansion beyond the free allowance
- This likely requires not only copy fixes in hero/trust/FAQ, but also a dedicated pricing/limits section on the landing.

### Open questions
- Is the free allowance monthly, one-time starter balance, or both?
- Is monetization based on subscriptions, one-time credit packs, or a hybrid?
- Are exact public prices already decided, or should the landing stay qualitative for now?
- Do paid credits expire?
- Should pricing be published in both Russian and English immediately?
