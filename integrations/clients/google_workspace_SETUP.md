# Linking CC to your Gmail + Calendar (one-time, ~15 min)

This connects CC — your Chief of Staff — to your Google account so it can **see** your
inbox and calendar and surface only what needs you. It is **read-only**: CC can read and
draft, but it can **never** send mail or change your calendar. The key it uses lives
**only on this laptop** (`~/.bari/google_token.json`), is git-ignored, and never leaves
your machine — no third party is involved.

You do this once. After that, CC just reads.

---

## What you'll do
Create your own Google "app" credential, approve read-only access once, and let CC store
the resulting key locally. Google requires *you* to do the approval — nobody else can
reach your mail on your behalf.

### Step 1 — Create a Google Cloud project (2 min)
1. Go to **https://console.cloud.google.com/** (sign in as tbarhaim@gmail.com).
2. Top bar → project dropdown → **New Project**. Name it `bari-cc` → **Create**.
3. Make sure the new `bari-cc` project is selected.

### Step 2 — Turn on the two APIs (2 min)
1. Search bar → **"Gmail API"** → **Enable**.
2. Search bar → **"Google Calendar API"** → **Enable**.

### Step 3 — Configure consent (4 min)
> NOTE: Google renamed this area to **"Google Auth Platform"**. The old "OAuth consent
> screen" is now split into **Branding** + **Audience**, and "Credentials" is now **Clients**.
> The steps below use the new names.
1. Left menu → **Branding**. App name: `Bari CC`. User support email + developer contact
   email: your address. **Save**.
2. Left menu → **Audience**. User type: **External**. Under **Test users** → **+ Add users**
   → add **tbarhaim@gmail.com** → **Save**. (Publishing status **Testing** with you as a test
   user is exactly right — it stays private to you, no Google review needed.)
3. (Optional) Left menu → **Data access** → just leave it; CC requests the read-only scopes
   itself, you don't need to add them here.

### Step 4 — Create the credential (2 min)
1. Left menu → **Clients** → **Create client** (or the **Create OAuth client** button on the
   Overview page).
2. Application type: **Desktop app**. Name: `bari-cc-desktop` → **Create**.
3. In the popup → **Download JSON**. Save it somewhere handy, e.g. your Downloads folder.
   (It'll be named like `client_secret_xxxx.json`.)

### Step 5 — Link it (1 min)
In a terminal at `C:\Bari`, run (point `--client-secret` at the file you just downloaded):

```powershell
python -m integrations.clients.google_workspace --auth --client-secret "$env:USERPROFILE\Downloads\client_secret_xxxx.json"
```

Your browser opens → Google asks you to allow **read-only** Gmail + Calendar → approve.
- You may see a "Google hasn't verified this app" screen — that's expected for your own
  private app. Click **Advanced → Go to Bari CC (unsafe)**. It's your own app; it's safe.
- The tab will say "CC is linked." Close it.

The terminal prints:
```
✓ Linked. Credential saved (local only) at: C:\Users\HP\.bari\google_token.json
```

### Step 6 — Confirm
```powershell
python -m integrations.clients.google_workspace
```
You should see a small JSON status — unread count, today's events, any conflicts. That's CC
reading your world. Done.

---

## What CC can and can't do (the guarantees)
- **Can:** read mail (headers + snippets), search the inbox, read calendar events, draft
  reply *text* to show you.
- **Cannot:** send email, reply, archive, delete, label, create/move/cancel events — there
  is **no write code path** in the connector. Widening this needs new permissions *and* a
  new decision from you.
- **Key safety:** the credential is in `~/.bari/` (outside the repo) and is git-ignored.
  It is never committed and never pushed.

## Undo / revoke at any time
- Revoke CC's access entirely: **https://myaccount.google.com/permissions** → remove **Bari CC**.
- Or just delete `C:\Users\HP\.bari\google_token.json`. CC instantly goes back to
  "not linked" and the board degrades gracefully — nothing breaks.
