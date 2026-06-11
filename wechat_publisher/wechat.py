# -*- coding: utf-8 -*-
"""微信公众号 API 封装：access_token、上传封面、存草稿、发布。

需要环境变量：
  WECHAT_APPID      公众号 AppID
  WECHAT_APPSECRET  公众号 AppSecret
注意：
  - 草稿箱 / 发布接口需要「已认证」的公众号。
  - 调用方公网 IP 必须加入公众号后台「IP 白名单」。
"""

import logging
import os

import requests

log = logging.getLogger(__name__)
BASE = "https://api.weixin.qq.com/cgi-bin"


class WeChatError(RuntimeError):
    pass


def _check(resp_json: dict, action: str) -> dict:
    if resp_json.get("errcode", 0) != 0:
        raise WeChatError(f"{action} 失败: {resp_json}")
    return resp_json


def get_access_token() -> str:
    appid = os.environ["WECHAT_APPID"]
    secret = os.environ["WECHAT_APPSECRET"]
    r = requests.get(f"{BASE}/token", params={
        "grant_type": "client_credential", "appid": appid, "secret": secret,
    }, timeout=30).json()
    if "access_token" not in r:
        raise WeChatError(f"获取 access_token 失败: {r}")
    return r["access_token"]


def upload_thumb(token: str, image_path: str) -> str:
    """上传封面为永久素材，返回 thumb_media_id。"""
    with open(image_path, "rb") as f:
        r = requests.post(
            f"{BASE}/material/add_material",
            params={"access_token": token, "type": "image"},
            files={"media": (os.path.basename(image_path), f, "image/jpeg")},
            timeout=60,
        ).json()
    if "media_id" not in r:
        raise WeChatError(f"上传封面失败: {r}")
    return r["media_id"]


def add_draft(token: str, articles: list[dict]) -> str:
    """把多篇文章作为一个图文草稿提交，返回草稿 media_id。

    articles 每项需含: title, digest, html, thumb_media_id
    """
    payload = {"articles": [{
        "title": a["title"],
        "author": a.get("author", ""),
        "digest": a["digest"],
        "content": a["html"],
        "content_source_url": "",
        "thumb_media_id": a["thumb_media_id"],
        "need_open_comment": 1,
        "only_fans_can_comment": 0,
    } for a in articles]}
    r = requests.post(
        f"{BASE}/draft/add", params={"access_token": token},
        # 微信要求 UTF-8 编码且不能转义中文
        data=__import__("json").dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8"},
        timeout=60,
    ).json()
    if "media_id" not in r:
        raise WeChatError(f"新增草稿失败: {r}")
    log.info("草稿已创建 media_id=%s（%d 篇）", r["media_id"], len(articles))
    return r["media_id"]


def publish_draft(token: str, draft_media_id: str) -> str:
    """提交发布（freepublish），返回 publish_id。需要已认证公众号。"""
    r = requests.post(
        f"{BASE}/freepublish/submit", params={"access_token": token},
        json={"media_id": draft_media_id}, timeout=60,
    ).json()
    _check(r, "提交发布")
    log.info("已提交发布 publish_id=%s", r.get("publish_id"))
    return str(r.get("publish_id"))
