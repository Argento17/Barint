# Bari Scrape-Runner — Windows Owner Guide (zero Linux knowledge assumed)

This replaces OWNER_RUNBOOK.md for the owner. Every command below is typed into
**PowerShell on your Windows machine** unless the line is marked **[ON THE SERVER]**.
Total time: ~20 minutes. If anything looks different from the "You should see" notes,
stop and paste what you see back into the chat — do not improvise.

---

## Step 0 — Create your SSH key (one time, on your PC, 2 minutes)

An SSH key is a pair of files that replaces passwords. Windows 11 has everything
built in.

1. Open **PowerShell** (Start menu → type `powershell` → Enter).
2. Run:
   ```powershell
   ssh-keygen -t ed25519
   ```
3. It asks three questions. **Press Enter for all three** (default location, no
   passphrase). Done — you now have a key.
4. Show your PUBLIC key (the safe-to-share half):
   ```powershell
   type $env:USERPROFILE\.ssh\id_ed25519.pub
   ```
   **You should see:** one long line starting with `ssh-ed25519 AAAA...` ending
   with your PC name.
5. Select that whole line with your mouse, press **Ctrl+C**. You'll paste it in
   Step 2. (Never share the other file, `id_ed25519` without `.pub` — that's the
   private half.)

---

## Step 1 — Sign up at Kamatera (5 minutes)

1. Go to **https://www.kamatera.com** → **Start Free Trial**.
2. Email, name, password, credit card or PayPal. The trial includes $100 credit
   (≈16 months of this server free).
3. Verify your email, log in at **https://console.kamatera.com**.

---

## Step 2 — Create the server (3 minutes)

In the console (console.kamatera.com): left menu **My Cloud → Servers** → blue
**Create New Server** button. You get ONE LONG PAGE with sections. Go top to
bottom. Only 6 things matter — leave everything else at its default:

1. **Zone** — pick any **Israel** data center (Tel Aviv if offered; Petach Tikva
   or Rosh Haayin are equally fine — all are Israeli IPs).
2. **Server Image** — under "OS Images" choose **Ubuntu**, then version
   **Server 24.04 LTS 64-bit**.
3. **Server Specs** —
   - Type: **A (Availability)**
   - vCPU: **1**
   - RAM: **2 GB** (2048 MB)
   - SSD Disk: **20 GB**
4. **Networking** — keep the default (one public WAN IP). Don't add anything.
5. **Password** — Kamatera requires a root password: set a strong one and SAVE
   IT in your password manager. This is your emergency back door via Kamatera's
   own web console (our setup script later disables password login over the
   network — that's intentional and safe).
   *If* you see a "Public SSH Key" / "SSH Keys" option, paste your
   `ssh-ed25519 AAAA...` line; if you don't see one, **don't hunt for it** —
   Step 3b installs the key in 30 seconds anyway.
6. **Billing cycle** — choose **Monthly** (always-on box; monthly includes the
   traffic bundle and is the ~$6/mo price). Name the server `bari-scraper`.

Click **Create Server**. Provisioning takes ~1–2 minutes. When it's up, the
server page shows its **IP address** (e.g. `185.x.x.x`) — copy it. Everywhere
below, replace `45.93.95.32` with that number.

> Looks slightly different on your screen? Section names shift; the substance
> doesn't. As long as you hit: Israel zone · Ubuntu 24.04 · 1 vCPU Type A ·
> 2 GB · 20 GB · saved root password · monthly — you're correct. When unsure,
> screenshot and ask before clicking Create.

---

## Step 3 — Connect from PowerShell (2 minutes)

1. In PowerShell:
   ```powershell
   ssh root@45.93.95.32
   ```
   ⚠️ Note: **root**, not ubuntu — Kamatera images log in as root.
2. First time only, you'll get a security question ending in
   `Are you sure you want to continue connecting?` → type **yes** → Enter.
3. If it asks for a password, use the password from Step 2.3.
   **You should see:** a greeting ending with a prompt like `root@bari-scraper:~#`
   — you are now typing ON THE SERVER.

### Step 3b — Install your key on the server (ONLY if you skipped Step 2.4)

**[ON THE SERVER]** run (paste your `ssh-ed25519 AAAA...` line between the quotes):
```bash
mkdir -p ~/.ssh && echo "PASTE_YOUR_PUBLIC_KEY_LINE_HERE" >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys
```
Then **verify before continuing** — open a SECOND PowerShell window and run
`ssh root@45.93.95.32`. **You should see:** it logs in WITHOUT asking for a
password. Only when that works, continue.

> 🛑 **Do not run Step 5 (setup.sh) until key login works.** The setup script
> turns off password login over the network on purpose. Your Kamatera web
> console password remains as the emergency back door regardless.

---

## Step 4 — Upload the files (1 minute)

In PowerShell **on your PC** (not the server window):
```powershell
scp C:\Bari\03_operations\bsip0\scrape_runner\setup.sh root@45.93.95.32:/tmp/
```
**You should see:** a progress line ending in `100%`.

---

## Step 5 — Run the setup script (3 minutes)

**[ON THE SERVER]** (the window from Step 3):
```bash
bash /tmp/setup.sh
```
It prints package installs for 2–3 minutes.
**You should see at the end:** `=== Setup complete: <date> ===` plus version
numbers for Python, git, rclone and a firewall status block saying `Status: active`.

---

## Step 6 — Upload and run the probes (5 minutes)

1. On your PC:
   ```powershell
   scp C:\Bari\03_operations\bsip0\scrape_runner\probe_all.py C:\Bari\03_operations\bsip0\scrape_runner\probe_shufersal.py C:\Bari\03_operations\bsip0\scrape_runner\probe_yohananof.py root@45.93.95.32:/opt/bari/
   ```
2. **[ON THE SERVER]** run the full retailer map (~2 minutes):
   ```bash
   /opt/bari/venv/bin/python3 /opt/bari/probe_all.py | tee /opt/bari/logs/probe_all.txt
   ```
3. **[ON THE SERVER]** run the Yohananof Playwright probe:
   ```bash
   PLAYWRIGHT_BROWSERS_PATH=/opt/bari/playwright-browsers /opt/bari/venv/bin/python3 /opt/bari/probe_yohananof.py | tee /opt/bari/logs/probe_yohananof.txt
   ```
   (Always use the full path `/opt/bari/venv/bin/python3` on this box — plain
   `python3` is the OS's own Python and doesn't have the scraping libraries.)

---

## Step 7 — Send the results back (1 minute)

On your PC:
```powershell
scp root@45.93.95.32:/opt/bari/logs/probe_all.txt $env:USERPROFILE\Desktop\
scp root@45.93.95.32:/opt/bari/logs/probe_yohananof.txt $env:USERPROFILE\Desktop\
```
Both files land on your Desktop. Open them in Notepad, paste contents into the
orchestrator chat. The verdict table decides everything downstream
(CLEAN / JS_ONLY / DEGRADED / BLOCKED per retailer).

---

## Money & housekeeping

- Cost: ~$6/month running. The server is meant to stay ON (it's the scheduled
  scrape runner). If you ever want to pause it: Kamatera console → server →
  **Stop** (disk-only cost while stopped; IP is kept).
- To disconnect from the server window: type `exit`.
- You never need to update it manually — security patches install themselves
  (it may auto-reboot Sunday 5am Israel time when needed).

## Troubleshooting

| You see | It means | Do |
|---|---|---|
| `Permission denied (publickey)` | Key not installed / wrong user | Make sure you used `root@`, not `ubuntu@`; redo Step 3b |
| `Connection timed out` | Server still booting or wrong IP | Wait 2 min, re-check IP in Kamatera console |
| `REMOTE HOST IDENTIFICATION HAS CHANGED` | You rebuilt the server | Run `ssh-keygen -R 45.93.95.32` on your PC, retry |
| `scp: No such file or directory` | `/opt/bari` doesn't exist yet | Run Step 5 before Step 6 |
| Stuck inside the server window | — | Type `exit` to get back to your PC |
| Locked out entirely | — | Kamatera console → server → **Console** (web terminal, uses the Step 2.3 password) |
