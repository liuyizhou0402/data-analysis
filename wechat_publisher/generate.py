# -*- coding: utf-8 -*-
"""调用 Claude 把当日热点资讯写成三篇公众号图文（HTML 格式）。"""

import json
import logging

import anthropic

from config import CLAUDE_MODEL

log = logging.getLogger(__name__)

SYSTEM_PROMPT = """你是一位资深留学顾问兼公众号主编，主营澳大利亚、新西兰、英国留学申请服务。
你写的公众号文章特点：标题抓人但不标题党、信息准确、有数据有来源、给出可执行的申请建议、
语气亲切专业、适合 22-30 岁准留学生和家长阅读。

输出要求（严格遵守）：
1. 只输出一个 JSON 对象，不要输出其他任何文字或 markdown 代码块标记。
2. JSON 结构：
{
  "title": "公众号标题，不超过30个字",
  "digest": "摘要，不超过54个字，用于公众号卡片",
  "html": "正文 HTML"
}
3. 正文 HTML 规范（微信公众号编辑器兼容）：
   - 只用 <section> <p> <h2>(用<p><strong>模拟) <strong> <em> <ul> <li> <blockquote> 等内联样式标签
   - 不要用 <img>（封面图由程序另外处理）、不要外链 <a>（微信会过滤）
   - 用 style 内联样式做排版：小标题用
     <p style="margin:24px 0 12px;font-size:17px;font-weight:bold;color:#1a73e8;border-left:4px solid #1a73e8;padding-left:10px">
   - 正文段落 <p style="margin:0 0 14px;font-size:15px;line-height:1.8;color:#3f3f3f">
   - 重点信息用 <strong style="color:#d93025"> 强调
   - 引用政策原文/数据用 <blockquote style="margin:14px 0;padding:10px 14px;background:#f5f7fa;border-left:3px solid #ccc;font-size:14px;color:#666">
   - 字数 1500-2500 字
   - 文末加一段引导关注+咨询的 CTA（提示读者私信/留言咨询留学申请）
4. 涉及具体数字（学费、分数线、政策日期）时，如新闻素材里没有就写大致范围并注明"以官网为准"，不要编造精确数字。"""


def generate_article(client: anthropic.Anthropic, topic: dict, news_items: list[dict],
                     date_str: str) -> dict:
    """生成一篇文章，返回 {title, digest, html}。"""
    news_block = "\n\n".join(
        f"【热度{it['score']}】来源：{it['source']}（{it['link']}）\n标题：{it['title']}\n摘要：{it['summary']}"
        for it in news_items
    ) or "（今日无新增资讯，请基于你掌握的常识性申请知识写一篇干货文章，注明政策细节以官网为准）"

    user_prompt = f"""今天是 {date_str}。请写一篇公众号文章。

主题方向：{topic['focus']}
参考标题方向：{topic['title_hint']}

以下是今天抓取到的相关资讯素材，已按热度从高到低排序（热度高的优先写、写得更详细）：

{news_block}

要求：内容必须与上面两篇姊妹文章错开（本篇专注自己的主题方向），按热度顺序组织资讯解读部分。"""

    with client.messages.stream(
        model=CLAUDE_MODEL,
        max_tokens=16000,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_prompt}],
    ) as stream:
        message = stream.get_final_message()

    text = next(b.text for b in message.content if b.type == "text").strip()
    # 容错：剥掉可能出现的 ```json 包裹
    if text.startswith("```"):
        text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()
    article = json.loads(text)

    for key in ("title", "digest", "html"):
        if not article.get(key):
            raise ValueError(f"生成结果缺少字段 {key}")
    article["digest"] = article["digest"][:54]
    article["title"] = article["title"][:30]
    log.info("生成文章：%s", article["title"])
    return article
