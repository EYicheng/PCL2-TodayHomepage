import requests

# API URL
url = "https://m.weibo.cn/api/container/getIndex?containerid=106003type%3D25%26t%3D3%26disable_hot%3D1%26filter_type%3Drealtimehot&title=%E5%BE%AE%E5%8D%9A%E7%83%AD%E6%90%9C&extparam=filter_type%3Drealtimehot%26mi_cid%3D100103%26pos%3D0_0%26c_type%3D30%26display_time%3D1540538388&luicode=10000011&lfid=231583"

# 请求头
headers = {
    "Referer": "https://s.weibo.com/top/summary?cate=realtimehot",
    "MWeibo-Pwa": "1",
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1"
}

# 发起请求
response = requests.get(url, headers=headers)

# 检查请求是否成功
if response.status_code == 200:
    result = response.json()
    print(result)
else:
    print(f"请求失败，状态码：{response.status_code}")