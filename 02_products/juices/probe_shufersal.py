"""Probe Shufersal and Victory for barcode 7290001247891 nutrition panel."""
import sys, os
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

import requests
import json

UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36'}
barcode = '7290001247891'

RESULTS = {}

# --- Shufersal ---
print('=== SHUFERSAL PROBE ===')
try:
    # Try Shufersal barcode search API
    url = f'https://www.shufersal.co.il/online/he/search/results?q={barcode}%3Arelevance&limit=5'
    r = requests.get(url, timeout=20, headers=UA)
    print(f'Status: {r.status_code}, len={len(r.content)}')
    RESULTS['shufersal_status'] = r.status_code
    if r.status_code == 200:
        print('Shufersal REACHABLE')
        text = r.text
        print('Body snippet (first 800):', text[:800])
        # Try to find the product entry — look for the barcode in the response
        if barcode in text:
            print(f'BARCODE {barcode} FOUND in Shufersal response')
            # Find context around it
            idx = text.find(barcode)
            print('Context:', text[max(0,idx-200):idx+500])
        else:
            print(f'BARCODE {barcode} NOT found in Shufersal response')
        RESULTS['shufersal'] = 'REACHABLE'
    else:
        RESULTS['shufersal'] = f'HTTP_{r.status_code}'
except Exception as e:
    print(f'Shufersal BLOCKED: {e}')
    RESULTS['shufersal'] = f'BLOCKED: {e}'

print()

# --- Victory storefront ---
print('=== VICTORY PROBE ===')
try:
    url_v = 'https://www.victoryonline.co.il/'
    r2 = requests.get(url_v, timeout=15, headers=UA)
    print(f'Victory home: {r2.status_code}, len={len(r2.content)}')
    RESULTS['victory_home'] = r2.status_code
    if r2.status_code == 200:
        RESULTS['victory'] = 'REACHABLE'
        # Try Victory product search
        search_url = f'https://www.victoryonline.co.il/search?q={barcode}'
        r3 = requests.get(search_url, timeout=15, headers=UA)
        print(f'Victory search: {r3.status_code}, len={len(r3.content)}')
        if r3.status_code == 200 and barcode in r3.text:
            print(f'BARCODE {barcode} FOUND in Victory search response')
            idx = r3.text.find(barcode)
            print('Context:', r3.text[max(0,idx-100):idx+300])
            RESULTS['victory_product_found'] = True
        else:
            print(f'Victory search returned {r3.status_code}, barcode in response: {barcode in r3.text}')
            RESULTS['victory_product_found'] = False
    else:
        RESULTS['victory'] = f'HTTP_{r2.status_code}'
except Exception as e:
    print(f'Victory BLOCKED: {e}')
    RESULTS['victory'] = f'BLOCKED: {e}'

print()

# --- Yochananof (known blocked from sandbox) ---
print('=== YOCHANANOF PROBE ===')
try:
    r4 = requests.get('https://www.yochananof.co.il', timeout=10, headers=UA)
    print(f'Yochananof home: {r4.status_code}')
    RESULTS['yochananof'] = f'HTTP_{r4.status_code}'
except Exception as e:
    print(f'Yochananof: {e}')
    RESULTS['yochananof'] = f'BLOCKED: {e}'

print()
print('=== SUMMARY ===')
print(json.dumps(RESULTS, ensure_ascii=False, indent=2))
