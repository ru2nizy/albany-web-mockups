# Simple Automation Outline for Local Businesses

**Purpose:** Practical, low-complexity automations that solve real time drains for independent restaurants, cafes, boutiques, and service businesses.

---

## Priority Automations (Start Here)

### 1. Review Request Flow
**Pain:** Owners forget to ask for reviews; good experiences never become public social proof.

**Simple version:**
- After a known positive interaction (or weekly batch), send a polite SMS/email with a direct Google review link.
- Tools: Google Form or Typeform → Make.com / n8n → Gmail/SMS.

### 2. Inquiry / Lead Capture → Follow-up
**Pain:** Website form submissions sit in an inbox and get answered late or not at all.

**Simple version:**
- Form submission creates a row in Google Sheets + sends an auto-reply + notifies the owner.
- Optional: 24–48 hour reminder if no response logged.

### 3. Hours / Specials Broadcast
**Pain:** Updating hours or daily specials across website, Google, and social is tedious.

**Simple version:**
- Owner updates one Google Sheet or Notion page.
- Automation pushes the change to the website (if using a CMS that supports it) and optionally creates a social post draft.

### 4. New Customer Welcome Sequence
**Pain:** First-time customers never hear from the business again.

**Simple version:**
- Capture email at point of sale or via a simple form.
- 3–5 short automated emails over 2–3 weeks (thank you, story, offer, review ask).

---

## Recommended Tool Stack for You

| Need | Tool |
|------|------|
| Visual workflows | Make.com (easiest) or n8n (more control / self-host) |
| Forms | Google Forms, Typeform, or Tally |
| Spreadsheet backbone | Google Sheets |
| Email | Gmail or a simple ESP |
| SMS (optional) | Twilio or similar |

Start with Make.com free tier for proofs of concept. Move to n8n if you want to host for clients later and keep margins high.

---

## Packaging Suggestion

- **Audit + 1 automation setup:** $500 – $900
- **3-automation starter pack:** $1,200 – $2,000
- **Monthly light monitoring:** $50 – $100

Keep scope tight. Over-promising complex AI agents is the fastest way to create support burden.
