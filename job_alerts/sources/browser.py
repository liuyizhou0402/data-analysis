# -*- coding: utf-8 -*-
"""Playwright 封装：给 JS 渲染 / 强反爬的站点用。

设计原则：每次抓取用独立浏览器上下文，失败只打印日志返回 None，
绝不让某一个源把整条 pipeline 拖崩。
"""
from __future__ import annotations

from contextlib import contextmanager
from typing import Optional

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
)


@contextmanager
def browser_page():
    """开一个伪装过的浏览器页面。用法：with browser_page() as page: ..."""
    try:
        from playwright.sync_api import sync_playwright
    except Exception as e:  # noqa: BLE001
        print(f"  [browser] Playwright 不可用，跳过浏览器类数据源: {e}")
        yield None
        return

    pw = browser = None
    try:
        pw = sync_playwright().start()
        browser = pw.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-blink-features=AutomationControlled"],
        )
        context = browser.new_context(
            user_agent=UA,
            locale="en-AU",
            viewport={"width": 1366, "height": 900},
        )
        # 去掉 navigator.webdriver 痕迹
        context.add_init_script(
            "Object.defineProperty(navigator,'webdriver',{get:()=>undefined})"
        )
        page = context.new_page()
        yield page
    except Exception as e:  # noqa: BLE001
        print(f"  [browser] 启动失败: {e}")
        yield None
    finally:
        try:
            if browser:
                browser.close()
        except Exception:  # noqa: BLE001
            pass
        try:
            if pw:
                pw.stop()
        except Exception:  # noqa: BLE001
            pass


def get_html(url: str, wait_selector: Optional[str] = None,
             timeout_ms: int = 25000) -> Optional[str]:
    """打开页面，返回渲染后的 HTML。"""
    with browser_page() as page:
        if page is None:
            return None
        try:
            page.goto(url, timeout=timeout_ms, wait_until="domcontentloaded")
            if wait_selector:
                try:
                    page.wait_for_selector(wait_selector, timeout=8000)
                except Exception:  # noqa: BLE001
                    pass
            page.wait_for_timeout(2000)
            return page.content()
        except Exception as e:  # noqa: BLE001
            print(f"  [browser] 打开 {url} 失败: {e}")
            return None


def fetch_json(home_url: str, api_url: str, timeout_ms: int = 25000):
    """先访问站点首页拿到 cookie，再在浏览器上下文里 fetch 同源 JSON 接口。

    专治 Seek 这种"页面是 React、数据走内部 JSON API、还套 Cloudflare"的站点。
    """
    with browser_page() as page:
        if page is None:
            return None
        try:
            page.goto(home_url, timeout=timeout_ms, wait_until="domcontentloaded")
            page.wait_for_timeout(1500)
            return page.evaluate(
                """async (u) => {
                    const r = await fetch(u, {headers: {'accept': 'application/json'}});
                    if (!r.ok) return null;
                    return await r.json();
                }""",
                api_url,
            )
        except Exception as e:  # noqa: BLE001
            print(f"  [browser] fetch_json 失败: {e}")
            return None
