#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HIFINI 音乐磁场自动签到脚本 (hifini.net)
精简版 - 无需提取sign参数
"""

import os
import requests
import json
from datetime import datetime


def hifini_sign(cookie_str: str) -> bool:
    """
    执行HIFINI签到
    :return: True=签到成功, False=已签到或失败
    """
    base_url = "https://hifini.net"
    sign_url = f"{base_url}/sg_sign.htm"
    
    # 解析Cookie
    cookies = {}
    for item in cookie_str.split(";"):
        item = item.strip()
        if "=" in item:
            key, value = item.split("=", 1)
            cookies[key] = value
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": f"{base_url}/sg_sign.htm",
        "Origin": base_url,
        "X-Requested-With": "XMLHttpRequest",
    }
    
    # 发送签到请求（无需额外参数）
    response = requests.post(
        sign_url,
        headers=headers,
        cookies=cookies,
        timeout=15
    )
    response.encoding = "utf-8"
    
    try:
        result = response.json()
        code = result.get("code", "")
        message = result.get("message", "")
        
        print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📝 响应: {message}")
        
        if code == "-1" and "已经" in message:
            print("ℹ️ 今日已签到")
            return False
        elif "成功" in message or code == "0":
            print("✅ 签到成功！")
            return True
        else:
            print(f"❌ 签到结果: {message}")
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
