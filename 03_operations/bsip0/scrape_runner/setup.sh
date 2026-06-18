#!/usr/bin/env bash
# setup.sh — Idempotent Ubuntu 24.04 setup for Bari scrape-runner VM
# Usage: chmod +x setup.sh && sudo ./setup.sh
# Safe to re-run; skips already-installed packages.

set -euo pipefail

echo "=== Bari scrape-runner setup: $(date) ==="

# --- Phase 1: System packages ---
apt-get update -qq
apt-get upgrade -y -qq

# Python 3.12+ (Ubuntu 24.04 ships 3.12), pip, venv
apt-get install -y -qq python3 python3-pip python3-venv

# git, rclone, curl, wget
apt-get install -y -qq git rclone curl wget

# Playwright / Chromium system deps
apt-get install -y -qq \
    libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 \
    libcups2 libdrm2 libdbus-1-3 libxkbcommon0 \
    libxcomposite1 libxdamage1 libxfixes3 libxrandr2 \
    libgbm1 libpango-1.0-0 libcairo2 libasound2t64 \
    libatspi2.0-0 libwayland-client0 libx11-xcb1 \
    libxcb-shm0 libxcb-shape0 libxcb-xfixes0

# Unattended-upgrades (security patches)
apt-get install -y -qq unattended-upgrades
dpkg-reconfigure -f noninteractive unattended-upgrades

# --- Phase 2: Python packages (PEP 668: Ubuntu 24.04 forbids system pip;
# everything lives in a dedicated venv at /opt/bari/venv) ---
python3 -m venv /opt/bari/venv
/opt/bari/venv/bin/pip install --quiet --upgrade pip
/opt/bari/venv/bin/pip install --quiet playwright requests beautifulsoup4 lxml

# Install Chromium for Playwright (via the venv's playwright)
PLAYWRIGHT_BROWSERS_PATH=/opt/bari/playwright-browsers \
    /opt/bari/venv/bin/playwright install chromium

# Convenience: `bari-python` works from anywhere.
# Must be a WRAPPER, not a symlink — a symlinked venv python resolves back to
# the system interpreter and silently loses the venv's site-packages.
printf '#!/bin/sh\nexec /opt/bari/venv/bin/python3 "$@"\n' > /usr/local/bin/bari-python
chmod +x /usr/local/bin/bari-python

# --- Phase 3: Directory structure ---
mkdir -p /opt/bari/raw_store
mkdir -p /opt/bari/playwright-browsers
mkdir -p /opt/bari/logs
chmod 755 /opt/bari

# --- Phase 4: SSH hardening ---
# Disable password auth (key-only) — safe to re-apply
if grep -q '^#\?PasswordAuthentication' /etc/ssh/sshd_config; then
    sed -i 's/^#\?PasswordAuthentication.*/PasswordAuthentication no/' /etc/ssh/sshd_config
else
    echo 'PasswordAuthentication no' >> /etc/ssh/sshd_config
fi
# Disable root login
if grep -q '^#\?PermitRootLogin' /etc/ssh/sshd_config; then
    sed -i 's/^#\?PermitRootLogin.*/PermitRootLogin prohibit-password/' /etc/ssh/sshd_config
else
    echo 'PermitRootLogin prohibit-password' >> /etc/ssh/sshd_config
fi
systemctl restart ssh   # Ubuntu 24.04 unit name is `ssh` (not `sshd`)

# --- Phase 5: Firewall ---
ufw --force reset
ufw default deny incoming
ufw default allow outgoing
ufw allow ssh
ufw --force enable

# --- Phase 6: Cron for unattended-upgrades auto-reboot ---
# Weekly reboot at 5am Sunday for kernel patches
cat > /etc/cron.d/auto-upgrade-reboot <<'CRON'
# Auto-reboot Sunday 5am after unattended-upgrades
SHELL=/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
0 5 * * 0 root [ -f /var/run/reboot-required ] && /sbin/reboot
CRON
chmod 644 /etc/cron.d/auto-upgrade-reboot

# --- Phase 7: Verify ---
echo "=== Verification ==="
python3 --version
/opt/bari/venv/bin/pip --version
git --version
rclone version | head -1
/opt/bari/venv/bin/playwright --version
ufw status verbose
echo "=== Setup complete: $(date) ==="
