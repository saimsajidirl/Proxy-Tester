#!/usr/bin/env python3
"""
Proxy Tester: Check working proxies, rank by speed, and save in string format
to good_proxies.json as: FACEBOOK_PROXIES="ip:port" or with auth.
"""

import json
import time
import os
import requests
from typing import List, Dict
from concurrent.futures import ThreadPoolExecutor, as_completed

TEST_URL = "http://httpbin.org/ip"
TIMEOUT = 10
MAX_THREADS = 30


def get_proxies_from_input() -> List[str]:
    print("Paste your proxies (one per line). Press Enter twice to finish:\n")
    proxies = []
    while True:
        line = input()
        if not line.strip():
            break
        proxies.append(line.strip())
    return proxies


def categorize_speed(seconds: float) -> str:
    if seconds < 0.1:
        return "Excellent"
    elif seconds < 0.3:
        return "Good"
    elif seconds < 0.7:
        return "Acceptable"
    elif seconds < 1.5:
        return "Slow"
    else:
        return "Poor"


def check_proxy(proxy_url: str) -> Dict:
    proxies = {"http": proxy_url, "https": proxy_url}
    result = {
        "proxy": proxy_url,
        "status": "BAD",
        "anonymity": "Unknown",
        "response_time": None,
        "speed": "N/A"
    }

    try:
        start = time.time()
        response = requests.get(TEST_URL, proxies=proxies, timeout=TIMEOUT)
        response.raise_for_status()
        proxy_ip = response.json().get("origin", "")
        elapsed = time.time() - start

        anonymity = (
            "Transparent" if "," in proxy_ip and "unknown" in proxy_ip.lower() else
            "Anonymous" if "," in proxy_ip else
            "Elite"
        )

        result.update({
            "status": "GOOD",
            "anonymity": anonymity,
            "response_time": round(elapsed, 3),
            "speed": categorize_speed(elapsed)
        })

    except requests.exceptions.RequestException:
        pass

    return result


def extract_clean_proxy(proxy: str) -> str:
    """
    Extracts only the ip:port or ip:port:username:password from a proxy string.
    Assumes proxy is already formatted.
    """
    return proxy.strip()


def test_proxies():
    proxy_list = get_proxies_from_input()
    good = []

    print("\n🔍 Testing proxies...\n")

    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        future_to_proxy = {executor.submit(check_proxy, proxy): proxy for proxy in proxy_list}
        for future in as_completed(future_to_proxy):
            res = future.result()
            if res["status"] == "GOOD":
                good.append(res)

    good.sort(key=lambda x: x["response_time"])

    print("\n🏆 Good Proxies (Fastest to Slowest):")
    clean_list = []
    for i, p in enumerate(good, start=1):
        cleaned = extract_clean_proxy(p["proxy"])
        clean_list.append(cleaned)
        print(f"{i}. {cleaned} | {p['anonymity']} | {p['speed']} | {p['response_time']}s")

    joined_proxies = ",".join(clean_list)
    env_line = f'FACEBOOK_PROXIES="{joined_proxies}"'

    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, "good_proxies.json")
    with open(output_path, "w") as f:
        f.write(env_line + "\n")

    print(f"\n✅ Saved good proxies to {output_path} in ENV format.")


if __name__ == "__main__":
    test_proxies()
