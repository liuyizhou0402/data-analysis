# -*- coding: utf-8 -*-
"""国内大厂「线上 / 远程」实习数据源（仅用于第二封邮件）。

硬规则：只返回 **大厂** 且 **线上/远程** 的实习；坐班岗位一律不返回。
来源：
  1) 腾讯招聘官方 JSON API（最稳定，腾讯专用）
  2) 实习僧（实习聚合站，覆盖各大厂，浏览器渲染 + 客户端过滤远程标记）

任何一路失败都只打印日志、返回空，绝不拖垮整条 pipeline。
"""
from __future__ import annotations

import time
from urllib.parse import quote_plus

from . import browser
from .base import JobPosting, http_get

# ============ 国内大厂别名表（用于判定是否「大厂」）============
CHINA_BIGTECH = {
    "字节跳动": ["字节", "bytedance", "tiktok", "抖音", "飞书", "lark", "火山引擎"],
    "腾讯": ["腾讯", "tencent", "wechat", "微信", "wxg", "天美", "光子"],
    "阿里巴巴": ["阿里", "alibaba", "蚂蚁", "ant group", "淘宝", "天猫", "钉钉",
              "alipay", "支付宝", "阿里云", "aliyun", "菜鸟", "高德", "盒马"],
    "百度": ["百度", "baidu", "apollo", "文心"],
    "美团": ["美团", "meituan", "大众点评"],
    "京东": ["京东", "jd.com", "jingdong", "jd "],
    "网易": ["网易", "netease", "网易云", "雷火", "有道"],
    "快手": ["快手", "kuaishou"],
    "小米": ["小米", "xiaomi", "redmi"],
    "滴滴": ["滴滴", "didi"],
    "华为": ["华为", "huawei", "海思", "昇腾", "鸿蒙", "harmony"],
    "拼多多": ["拼多多", "pinduoduo", "pdd", "temu"],
    "哔哩哔哩": ["哔哩哔哩", "bilibili", "b站"],
    "携程": ["携程", "trip.com", "ctrip"],
    "微博/新浪": ["微博", "weibo", "新浪", "sina"],
    "OPPO/vivo": ["oppo", "vivo"],
    "新势力车企": ["理想汽车", "蔚来", "小鹏", "li auto", "nio", "xpeng", "比亚迪", "byd"],
    "AI/硬科技": ["商汤", "sensetime", "旷视", "megvii", "科大讯飞", "iflytek",
              "智谱", "zhipu", "月之暗面", "moonshot", "minimax", "深度求索", "deepseek"],
}

REMOTE_MARKERS = [
    "远程", "线上", "在线", "居家", "异地", "不限地点", "remote", "wfh",
    "work from home", "home office", "可远程", "全程线上",
]


def _bigtech_name(text: str) -> str | None:
    """命中则返回大厂规范名，否则 None。"""
    t = (text or "").lower()
    for canon, aliases in CHINA_BIGTECH.items():
        if any(a.lower() in t for a in aliases):
            return canon
    return None


def _is_remote(text: str) -> bool:
    t = (text or "").lower()
    return any(m in t for m in REMOTE_MARKERS)


# ============ 1) 腾讯招聘官方 API ============
TENCENT_API = "https://careers.tencent.com/tencentcareer/api/post/Query"


def _from_tencent(keyword: str, limit: int) -> list[JobPosting]:
    out: list[JobPosting] = []
    params = {
        "timestamp": int(time.time() * 1000),
        "keyword": keyword,
        "pageIndex": 1,
        "pageSize": min(max(limit, 5), 10),
        "language": "zh-cn",
        "area": "cn",
    }
    resp = http_get(TENCENT_API, params=params,
                    headers={"Referer": "https://careers.tencent.com/"})
    if not resp:
        return out
    try:
        posts = (resp.json().get("Data") or {}).get("Posts") or []
    except Exception:  # noqa: BLE001
        return out
    for p in posts:
        name = p.get("RecruitPostName", "") or ""
        loc = p.get("LocationName", "") or ""
        duty = p.get("Responsibility", "") or ""
        blob = f"{name} {loc} {duty}"
        if "实习" not in name and "intern" not in name.lower():
            continue
        if not _is_remote(blob):       # 仅保留线上/远程
            continue
        out.append(JobPosting(
            title=name,
            company="腾讯 Tencent",
            location=loc or "线上/远程",
            url=p.get("PostURL", "") or "",
            source="Tencent招聘",
            description=duty[:300],
            posted=(p.get("LastUpdateTime", "") or "")[:10],
            category="china_online",
        ))
        if len(out) >= limit:
            break
    return out


# ============ 2) 实习僧（聚合，覆盖各大厂）============
SHIXISENG = "https://www.shixiseng.com/interns?keyword={kw}&city=%E5%85%A8%E5%9B%BD&page=1"


def _from_shixiseng(keyword: str, limit: int) -> list[JobPosting]:
    out: list[JobPosting] = []
    url = SHIXISENG.format(kw=quote_plus(keyword))
    html = browser.get_html(url, wait_selector="a[href*='/intern']")
    if not html:
        return out
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, "lxml")
    except Exception:  # noqa: BLE001
        return out
    seen: set[str] = set()
    for a in soup.select("a[href*='/intern']"):
        href = a.get("href", "")
        if not href or "/interns" in href:    # 跳过列表页自身
            continue
        title = a.get_text(strip=True)
        if not title or len(title) < 2:
            continue
        full = href if href.startswith("http") else "https://www.shixiseng.com" + href
        if full in seen:
            continue
        card = a.find_parent(["li", "div"])
        ctext = card.get_text(" ", strip=True) if card else title
        company = _bigtech_name(ctext)
        if not company:                        # 非大厂 → 丢弃
            continue
        if not _is_remote(ctext):              # 卡片无远程标记 → 丢弃（必须线上）
            continue
        seen.add(full)
        out.append(JobPosting(
            title=title,
            company=company,
            location="线上/远程",
            url=full,
            source="实习僧",
            description=ctext[:200],
            category="china_online",
        ))
        if len(out) >= limit:
            break
    return out


def fetch(keyword: str, location: str, limit: int = 25) -> list[JobPosting]:
    """location 参数忽略（本源固定中国/线上）；keyword 为远程实习检索词。"""
    jobs: list[JobPosting] = []
    try:
        jobs += _from_tencent(keyword, limit)
    except Exception as e:  # noqa: BLE001
        print(f"    [china_intern/tencent] 异常 {e}")
    try:
        jobs += _from_shixiseng(keyword, limit)
    except Exception as e:  # noqa: BLE001
        print(f"    [china_intern/shixiseng] 异常 {e}")
    return jobs
