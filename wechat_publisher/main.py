# -*- coding: utf-8 -*-
"""每日流水线入口：抓资讯 → 热度排序 → 生成三篇图文 → 存草稿/发布。

环境变量：
  ANTHROPIC_API_KEY   必需，生成文章
  WECHAT_APPID / WECHAT_APPSECRET   配置后才会推送到公众号；缺失则只本地生成
  WECHAT_AUTO_PUBLISH 设为 "true" 时存草稿后直接提交发布（需认证号），否则只存草稿
"""

import datetime
import json
import logging
import os
import sys

import anthropic

from config import ARTICLE_TOPICS, MAJORS_BY_WEEKDAY, NEWS_PER_ARTICLE, OUTPUT_DIR
from covers import make_cover
from fetch_news import fetch_all, filter_by_region
from generate import generate_article

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("main")

BADGES = ["澳新热点", "英国申请", "专业解析"]


def main() -> int:
    today = datetime.date.today()
    date_str = today.strftime("%Y年%m月%d日")
    out_dir = os.path.join(OUTPUT_DIR, today.isoformat())
    os.makedirs(out_dir, exist_ok=True)

    # 1. 抓取并按热度排序
    log.info("抓取资讯中…")
    all_news = fetch_all()
    log.info("共 %d 条资讯，热度第一：%s", len(all_news),
             all_news[0]["title"] if all_news else "（无）")
    with open(os.path.join(out_dir, "news_ranked.json"), "w", encoding="utf-8") as f:
        json.dump(all_news, f, ensure_ascii=False, indent=2)

    # 2. 生成三篇文章
    client = anthropic.Anthropic()
    major = MAJORS_BY_WEEKDAY[today.weekday()]
    articles = []
    for i, topic in enumerate(ARTICLE_TOPICS):
        topic = {**topic,
                 "title_hint": topic["title_hint"].format(major=major),
                 "focus": topic["focus"].format(major=major)}
        news = filter_by_region(all_news, topic["region_filter"], NEWS_PER_ARTICLE)
        log.info("生成第 %d 篇（%s），素材 %d 条…", i + 1, topic["slug"], len(news))
        article = generate_article(client, topic, news, date_str)
        article["cover_path"] = make_cover(
            article["title"], BADGES[i], i,
            os.path.join(out_dir, f"cover_{topic['slug']}.jpg"))
        articles.append(article)
        with open(os.path.join(out_dir, f"article_{topic['slug']}.html"), "w", encoding="utf-8") as f:
            f.write(f"<!-- {article['title']} | {article['digest']} -->\n{article['html']}")

    log.info("三篇文章已生成并保存到 %s", out_dir)

    # 3. 推送到公众号
    if not (os.environ.get("WECHAT_APPID") and os.environ.get("WECHAT_APPSECRET")):
        log.warning("未配置 WECHAT_APPID/WECHAT_APPSECRET，跳过公众号推送（文章已保存在本地）")
        return 0

    from wechat import add_draft, get_access_token, publish_draft, upload_thumb
    token = get_access_token()
    for a in articles:
        a["thumb_media_id"] = upload_thumb(token, a["cover_path"])
    draft_id = add_draft(token, articles)

    if os.environ.get("WECHAT_AUTO_PUBLISH", "").lower() == "true":
        try:
            publish_draft(token, draft_id)
            log.info("已自动提交发布")
        except Exception as e:
            log.error("自动发布失败（草稿已保留，可后台手动群发）: %s", e)
            return 0
    else:
        log.info("已存入草稿箱（WECHAT_AUTO_PUBLISH 未开启），请到公众号后台确认发布")
    return 0


if __name__ == "__main__":
    sys.exit(main())
