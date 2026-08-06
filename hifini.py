#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HIFINI 音乐磁场自动签到脚本 (hifini.net)
精简版 - 无需提取sign参数
"""

import os
import requests
import json
import time
from datetime import datetime

def hifini_sign(cookie_str: str) -> bool:
    base_url = "https://hifini.net"
    sign_url = f"{base_url}/sg_sign.htm"
    
    cookies = {}
    for item in cookie_str.split(";"):
        item = item.strip()
        if "=" in item:
            key, value = item.split("=", 1)
            cookies[key] = value
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": base_url + "/",
        "Origin": base_url,
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "X-Requested-With": "XMLHttpRequest",
    }
    
    session = requests.Session()
    session.headers.update(headers)
    
    # 先访问首页，获取必要的cookie和会话
    try:
        session.get(base_url, timeout=10)
    except:
        pass  # 即使失败也不影响后续
    
    for attempt in range(3):
        try:
            response = session.post(sign_url, cookies=cookies, timeout=15)
            response.encoding = "utf-8"
            result = response.json()
            # ... 后续处理同上 ...
            return True/False
        except (requests.ConnectionError, requests.Timeout) as e:
            print(f"⚠️ 请求失败 (尝试 {attempt+1}/3): {e}")
            if attempt < 2:
                time.sleep(2 ** attempt)
            else:
                print("❌ 所有重试均失败")
                return False
        except Exception as e:
            print(f"❌ 未知错误: {e}")
            return False
    except:
        print(f"❌ 响应解析失败: {response.text}")
        return False


def main():
    COOKIE = os.environ.get("HIFINI_COOKIE")
    
    print(f"\n{'='*40}")
    print("🎵 HIFINI 音乐磁场签到")
    print(f"{'='*40}")
    
    hifini_sign(COOKIE)
    
    print(f"{'='*40}\n")


if __name__ == "__main__":
    main()
