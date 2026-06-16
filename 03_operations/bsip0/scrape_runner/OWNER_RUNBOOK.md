# Owner Runbook — Create the Israeli VM (15 minutes)

You are not a sysadmin. These steps are written for you. Follow them in order — if something
fails or looks different, stop and ask rather than guessing.

---

## Step 1: Sign up at Kamatera

1. Go to **https://www.kamatera.com** and click **"Start Free Trial"** (top right).
2. Enter your email, name, and password. Use a credit card or PayPal.
   - The free trial gives you $100 credit — enough for ~16 months at $6/mo.
3. Verify your email.

## Step 2: Create the server

1. Log in to the Kamatera management console (my.kamatera.com).
2. Click **"Create Server"** → **"New Server"**.
3. Fill in:

   | Field | What to type/select |
   |---|---|
   | Server name | `bari-scraper` |
   | Data center | **Israel, Tel Aviv** |
   | Image | **Ubuntu Server 24.04 LTS 64-bit** |
   | CPU type | **Type A – Availability** |
   | CPU | **1 vCPU** |
   | RAM | **2 GB** |
   | Disk | **20 GB NVMe** |
   | Traffic | **5 TB** (default; fine for our use) |
   | Daily backup | **None** (optional; costs extra) |

4. Scroll down to **"Network"**. Keep defaults (1 public IP, IPv4).
5. Scroll to **"SSH Key"**. This is important:
   - If you have an SSH key already, click **"Add Key"** and paste your public key (the `.pub` file).
   - If you do NOT have an SSH key, ask whoever manages your computer to generate one for you
     (`ssh-keygen -t ed25519`) and give you the public key. Then paste it in.
6. Leave **"Password"** blank (we want key-only access).
7. Click **"Create Server"**.
8. Wait 30–60 seconds. The console will show the server's **IP address** (e.g., `5.xxx.xxx.xxx`).
   Copy this IP address.

## Step 3: SSH in and run the setup

1. Open a terminal (PowerShell on Windows, Terminal on Mac, or whatever you use).

2. Run this command (replace `5.xxx.xxx.xxx` with your server's IP):

   ```bash
   ssh ubuntu@5.xxx.xxx.xxx
   ```

   The first time, you'll see a security warning. Type **`yes`** and press Enter.

3. Now you're logged in. Run the setup:

   ```bash
   curl -sL https://raw.githubusercontent.com/.../setup.sh | sudo bash
   ```

   *(Wait — we haven't uploaded setup.sh yet. Instead, you have two options:)*

   **Option A — Upload from your computer:**
   Open a NEW terminal on your computer (keep the SSH session open) and run:
   ```bash
   scp C:\Bari\03_operations\bsip0\scrape_runner\setup.sh ubuntu@5.xxx.xxx.xxx:/tmp/setup.sh
   ```
   Then back in the SSH session:
   ```bash
   sudo bash /tmp/setup.sh
   ```

   **Option B — Copy-paste:**
   Open setup.sh on your computer in Notepad, select ALL the text, copy it.
   In the SSH session, run:
   ```bash
   cat > /tmp/setup.sh
   ```
   Paste the text (right-click in the terminal to paste), then press Enter, then press **Ctrl+D**.
   Then run:
   ```bash
   sudo bash /tmp/setup.sh
   ```

4. The script runs for 1–3 minutes. When it finishes, you'll see:
   ```
   === Setup complete: ...
   ```
   Your Python version, git version, and firewall status are printed.

## Step 4: Upload the probe scripts

On your computer (NOT the SSH session), run:

```bash
scp C:\Bari\03_operations\bsip0\scrape_runner\probe_shufersal.py ubuntu@5.xxx.xxx.xxx:/opt/bari/
scp C:\Bari\03_operations\bsip0\scrape_runner\probe_yohananof.py ubuntu@5.xxx.xxx.xxx:/opt/bari/
```

## Step 5: Test connectivity (Shufersal probe)

In the SSH session:

```bash
python3 /opt/bari/probe_shufersal.py
```

This takes ~30 seconds. It fetches 8 pages from Shufersal and reports whether the
Israeli IP is working. At the end you'll see:

- **CLEAN** — the VM can reach Shufersal. Proceed to Phase 1 live deployment.
- **DEGRADED** — some pages work, some don't. May need minor fixes.
- **BLOCKED** — Shufersal is blocking the VM's IP. You'll need residential proxies.

## What next?

If CLEAN → hand the VM IP to whoever deploys the crawl pipeline.
If BLOCKED → message the team; we'll add residential proxy support.

To stop the VM (save money when not using it): in the Kamatera console, click
**"Stop"** on the server. It will cost ~$0.008/hr only for the disk while stopped.
To start again: click **"Start"**. The IP stays the same as long as you don't delete it.
