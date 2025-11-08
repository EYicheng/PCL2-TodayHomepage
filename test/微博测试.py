# weibo_hot.py
import requests
import json
import urllib.parse

# 模拟 COOKIE（注意：长期使用可能失效，需定期更新）
COOKIE = (
    'SUB=_2AkMfiZ0rf8NxqwFRmvsQzWzrb4t2wg7EieKp1WzwJRMxHRl-yT9kqlIitRB6NAmzxF4VA1utRFGp8rQgmyrgezcW39y0; '
    'SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9W53ZGSdSzBm4kF5jod8B.He; '
    '_s_tentry=passport.weibo.com; '
    'Apache=6768551213104.772.1758794271221; '
    'SINAGLOBAL=6768551213104.772.1758794271221; '
    'ULV=1758794271230:1:1:1:6768551213104.772.1758794271221:'
)

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

def fetch_weibo_hot():
    url = "https://m.weibo.cn/api/container/getIndex?containerid=106003type%3D25%26t%3D3%26disable_hot%3D1%26filter_type%3Drealtimehot"
    
    headers = {
        "User-Agent": USER_AGENT,
        "Cookie": COOKIE,
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        # 提取 card_group
        cards = data.get("data", {}).get("cards", [])
        if not cards:
            return []

        card_group = cards[0].get("card_group", [])
        # 过滤掉包含 'stick' 的条目（广告或置顶）
        filtered = [item for item in card_group if "stick" not in item.get("pic", "")]

        result = []
        for item in filtered:
            title = item.get("desc", "")
            link = f"https://s.weibo.com/weibo?q={urllib.parse.quote(title)}"
            result.append({
                "title": title,
                "hot_value": 0,  # 原 TS 代码未使用真实热度值
                "link": link
            })
        return result

    except Exception as e:
        print(f"Error fetching Weibo hot search: {e}")
        return []

def format_as_text(data, limit=20):
    lines = ["微博实时热搜", ""]
    for i, item in enumerate(data[:limit], 1):
        lines.append(f"{i}. {item['title']}")
    return "\n".join(lines)

def main():
    hot_list = fetch_weibo_hot()
    
    # 示例：输出文本格式
    print(format_as_text(hot_list))
    
    # 示例：输出 JSON 格式
    # print(json.dumps(hot_list, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()