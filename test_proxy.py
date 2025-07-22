#!/usr/bin/env python3
"""
Proxy Tester: Check working proxies, rank by speed, and save in string format
to good_proxies.json as: FACEBOOK_PROXIES="ip:port" or with auth.
"""

import time
import os
import requests
from typing import List, Dict
from concurrent.futures import ThreadPoolExecutor, as_completed
import sys

TEST_URL = "http://httpbin.org/ip"
TIMEOUT = 10
MAX_THREADS = 30


def prompt_proxy_type() -> str:
    types = ["http", "https", "socks4", "socks5"]
    print("Select proxy type:")
    for idx, t in enumerate(types, 1):
        print(f"{idx}. {t}")
    while True:
        choice = input("Enter number (1-4): ").strip()
        if choice in {"1", "2", "3", "4"}:
            return types[int(choice) - 1]
        print("Invalid choice. Please enter 1, 2, 3, or 4.")


def get_proxies_from_input(filename: str = None) -> List[str]:
    """
    If filename is provided, read proxies from file. Otherwise, prompt user for input.
    """
    proxies: List[str] = []
    if filename:
        try:
            with open(filename, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        proxies.append(line)
            print(f"Loaded {len(proxies)} proxies from {filename}.")
        except Exception as e:
            print(f"Error reading {filename}: {e}")
            sys.exit(1)
    else:
        print("Paste your proxies (ip:port or ip:port:username:password, one per line). Press Enter twice to finish:\n")
        while True:
            line = input()
            if not line.strip():
                break
            proxies.append(line.strip())
    return proxies


def build_proxy_url(proxy_type: str, proxy: str) -> str:
    parts = proxy.split(":")
    if len(parts) == 2:

        return f"{proxy_type}://{proxy}"
    elif len(parts) == 4:

        ip, port, user, pwd = parts
        return f"{proxy_type}://{user}:{pwd}@{ip}:{port}"
    else:
        return proxy

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


def check_proxy(proxy_url: str, proxy_type: str) -> Dict[str, object]:
    proxies = {"http": proxy_url, "https": proxy_url}
    result = {
        "proxy": proxy_url,
        "status": "BAD",
        "anonymity": "Unknown",
        "response_time": None,
        "speed": "N/A"
    }
    test_url = "https://www.youtube.com"
    try:
        start = time.time()
        response = requests.get(test_url, proxies=proxies, timeout=TIMEOUT)
        response.raise_for_status()
        elapsed = time.time() - start
        result.update({
            "status": "GOOD",
            "anonymity": "Unknown",
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
    proxy_type = prompt_proxy_type()
    filename = sys.argv[1] if len(sys.argv) > 1 else None
    proxy_list = get_proxies_from_input(filename)
    good: List[Dict[str, object]] = []
    print(f"\n🔍 Testing {proxy_type.upper()} proxies...\n")
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        future_to_proxy = {
            executor.submit(check_proxy, build_proxy_url(proxy_type, proxy), proxy_type): proxy
            for proxy in proxy_list
        }
        for future in as_completed(future_to_proxy):
            res = future.result()
            if res["status"] == "GOOD":
                good.append(res)
    good.sort(key=lambda x: x["response_time"])
    print("\n🏆 Good Proxies (Fastest to Slowest):")
    clean_list: List[str] = []
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
