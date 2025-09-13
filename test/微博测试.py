import requests
from bs4 import BeautifulSoup
def fetch_weibo_hot_search():
   url = "https://s.weibo.com/top/summary?cate=realtimehot"
   headers = {
       "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
   }
   response = requests.get(url, headers=headers)
   print(response)
   soup = BeautifulSoup(response.text, "html.parser")
   table = soup.find("table", class_="table")
   rows = table.find_all("tr")[1:] # 跳过表头
   data = []
   for row in rows:
       cols = row.find_all("td")
       rank = cols[0].text.strip()
       keyword = cols[1].text.strip()
       link = "https://s.weibo.com" + cols[1].a["href"]
       heat = cols[2].text.strip() if len(cols) > 2 else "N/A"
       data.append({"排名": rank, "关键词": keyword, "热度": heat, "链接": link})
   return data
data = fetch_weibo_hot_search()
for item in data:
   print(item)