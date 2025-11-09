import requests
import datetime
from datetime import datetime
import pytz
from xml.sax.saxutils import escape
import time
import chinese_calendar as calendar

# 微博热搜：经过两个月，主任终于想起我了！喵~

# TOKEN = os.environ.get("Token") if 1==1 else 
# CHINA_NEWS_URL = f"https://api.istero.com/resource/v1/cctv/china/latest/news?token={TOKEN}"
# WORLD_NEWS_URL = f"https://api.istero.com/resource/v1/cctv/world/latest/news?token={TOKEN}"
# HOLIDAY_URL = f"https://api.istero.com/resource/v1/check/holiday?token={TOKEN}&date={datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).date().isoformat()}"
# TODAY_INTHEHISTORY_URL = f"https://api.istero.com/resource/v1/history/today?token={TOKEN}"
TOUTIAO_URL = "https://www.toutiao.com/hot-event/hot-board/?origin=toutiao_pc"
QQ_URL = "https://r.inews.qq.com/gw/event/hot_ranking_list?page_size=20"
WY_URL = "https://m.163.com/fe/api/hot/news/flow"
WEIBO_URL = f"https://uapis.cn/api/v1/misc/hotboard?type=weibo"
BILIBILI_URL = "https://api.bilibili.com/x/web-interface/ranking/v2?rid=0&type=all"
NOWPATH = "https://pcl.wyc-w.top/"
# today_str = datetime.date.today().isoformat()
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.2739.42",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",  # 表示客户端希望优先使用 HTTPS
    # "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Cache-Control": "max-age=0",
}

bilibili_header = {
"Host": "api.bilibili.com",
"Sec-Fetch-Site": "same-origin",
"Sec-Fetch-Mode": "cors",
"Sec-Fetch-Dest": "empty",
"Referer": "https://api.bilibili.com/x/web-interface/ranking/v2?rid=0&type=all",
"Accept-Encoding": "gzip, deflate, br",
"Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
"Priority": "u=1, i",
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.2739.42",
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
"Connection": "keep-alive",
"Upgrade-Insecure-Requests": "1",  # 表示客户端希望优先使用 HTTPS
"Sec-Fetch-Dest": "document",
"Sec-Fetch-Mode": "navigate",
"Sec-Fetch-Site": "none",
"Sec-Fetch-User": "?1",
"Cache-Control": "max-age=0",
"Cookie": "buvid3=653872FF-1CF0-02FC-2074-129616C4E5C110686infoc; b_nut=1754286310; _uuid=A7FF93F7-5281-58F3-D9E1-A74A10D1474B511536infoc; enable_web_push=DISABLE; DedeUserID=1676930979; DedeUserID__ckMd5=45937a9f5a76c250; theme-tip-show=SHOWED; theme-avatar-tip-show=SHOWED; rpdid=0zbfvRPVwD|pi6kNXLC|2qX|3w1UIO2O; LIVE_BUVID=AUTO9217551666069914; CURRENT_QUALITY=127; PVID=10; theme_style=light; home_feed_column=5; SESSDATA=810d1acd%2C1771588529%2Ca78a7%2A82CjALWkQN420X9oMSpjLA-cB1HfJj1-gHsvANM-w0OCDkuoU98f0TlDGZ8yPSbS5bYzgSVkpFZk1ITWhBT3Z5bEFhNUd2NFB0ZnlBUFA2MDVnMVB2b3p0OHl2anZ3RGdMdW5FQTFGV19FYnFaeGQ2TlpXT2VFRjJsWUd2VFFrenVYb1NTUkJSYWNnIIEC; bili_jct=3e0f8ad277ecdfde6fcc8e97352bf7d0; browser_resolution=1738-909; CURRENT_FNVAL=4048; buvid4=23FA359E-2ECF-606A-54D8-896C96D86E1937591-025011914-UMn4/nSnCr2JD8oBg2SoGI9FBPgLOgjSuWNSK7WZcCtfAqu/7ftYx4ojwmtcTWFw; bsource=search_bing; fingerprint=16280899fd5e483b819deaa24cdfab68; buvid_fp_plain=undefined; buvid_fp=16280899fd5e483b819deaa24cdfab68; sid=hdqfnlia; bp_t_offset_1676930979=1105391060047101952; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NTY0Njc5MDMsImlhdCI6MTc1NjIwODY0MywicGx0IjotMX0.D7fYD_QHDjb-1pnJwcMgGrPklRqPqvL3oTuX5-2SEuo; bili_ticket_expires=1756467843; b_lsid=462A67CE_198E63EF677"
}

wbheaders = {
    "Referer": "https://s.weibo.com/top/summary?cate=realtimehot",
    "MWeibo-Pwa": "1",
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1"
}

def fetch_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        print(response.json())
        return response.json()
    except Exception as e:
        print(f"请求失败 {url}: {e}")
        return None
    
def fetch_data_hasheaders(url, headers_):
    try:
        response = requests.get(url, headers=headers_)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"请求失败 {url}: {e}")
        return None
    
def doutiaonewsdata___(list):
    items = []
    i = 0
    for item in list:
        i += 1
        title = item.get("Title", "无标题")
        labelUrl = item.get("LabelUrl", "").replace("&", "&amp;")
        LogoUrl = f"{NOWPATH}images/toutiao/{i}.PNG".replace("&", "&amp;")
        url = item.get("Url", "").replace("&", "&amp;")
        hotValue = item.get("HotValue", 0)
        line = f'''
        <local:MyListItem
            Margin="-5,2,-5,8"
            Logo="{LogoUrl}"
            Title="{title}"
            Info="🔥{hotValue}"
            EventType="打开网页"
            EventData="{url}"
            Type="Clickable" />'''
        items.append(line)
    return "\n".join(items)

def nend___(list):
    items = []
    i = 0
    for item in list:
        i += 1
        if i != 1:
            title = item.get("title", "无标题").replace('"', "“")
            url = item.get("url", "#").replace("&", "&amp;")
            time = item.get("time", "未知时间")
            LogoUrl = f"{NOWPATH}images/toutiao/{i-1}.PNG".replace("&", "&amp;")
            abstract = item.get("abstract", "")
            # 使用 XAML 超链接语法
            line = f'''
            <local:MyListItem
                Margin="-5,2,-5,8"
                Logo="{LogoUrl}"
                Title="{title}"
                Info="{time}  |  {abstract}"
                EventType="打开网页"
                EventData="{url}"
                Type="Clickable" />'''
            items.append(line)
    return "\n".join(items)

def wb(list):
    items = []
    i = 0
    for item in list:
        i += 1
        title = item.get("title", "").replace('"', "“")
        url = item.get("url", "#").replace("&", "&amp;")
        time = item.get("hot_value", "")
        LogoUrl = f"{NOWPATH}images/toutiao/{i}.PNG".replace("&", "&amp;")
        line = f'''
        <local:MyListItem
            Margin="-5,2,-5,8"
            Logo="{LogoUrl}"
            Title="{title}"
            Info="🔥{time}"
            EventType="打开网页"
            EventData="{url}"
            Type="Clickable" />'''
        items.append(line)
    return "\n".join(items)

def wy(list):
    items = []
    i = 0
    for item in list:
        i += 1
        title = item.get("title", "无标题").replace('"', "“")
        url = item.get("url", "#").replace("&", "&amp;")
        time = item.get("createTime", "无标题")
        writer = item.get("source", "无作者").replace('"', "“")
        LogoUrl = f"{NOWPATH}images/toutiao/{i}.PNG".replace("&", "&amp;")
        line = f'''
        <local:MyListItem
            Margin="-5,2,-5,8"
            Logo="{LogoUrl}"
            Title="{title}"
            Info="{time}  |  {writer}"
            EventType="打开网页"
            EventData="{url}"
            Type="Clickable" />'''
        items.append(line)
    return "\n".join(items)

def bili(list):
    items = []
    i = 0
    for item in list:
        i += 1
        title = item.get("title", "无标题").replace('"', "“")
        url = item.get("short_link_v2", "#").replace("&", "&amp;")
        time = item.get("owner", {}).get("name", "无标题").replace('"', "“")
        LogoUrl = item.get("pic", "").replace("&", "&amp;")
        desc = item.get("desc", "").replace('"', "“")
        line = f'''
        <local:MyListItem
            Margin="-5,2,-5,8"
            Logo="{LogoUrl}"
            Title="{title}"
            Info="{desc}  ——  {time}"
            EventType="打开网页"
            EventData="{url}"
            Type="Clickable" />'''
        items.append(line)
    return "\n".join(items)

def format_news_items(news_list):
    items = []
    for item in news_list:
        title = item.get("title", "无标题")
        url = item.get("url", "#")
        time = item.get("time", "未知时间")
        poster = item.get("poster", "pack://application:,,,/images/Blocks/RedstoneBlock.png")
        description = item.get("description", "")
        # 使用 XAML 超链接语法
        line = f'''
        <local:MyListItem  Margin="-5,2,-5,8"
                    Logo="{poster}" Title="{title}" Info="{time}  |  {description}"
                    EventType="打开网页" EventData="{url}" Type="Clickable" />'''
        items.append(line)
    return "\n".join(items)

def history_items(history_list):
    items = []
    i = 0
    for item in history_list:
        i += 1
        title = escape(item.get("title", "无标题"))
        time = item.get("time", "未知时间")
        # 使用 XAML 超链接语法
        if i == 1:
            line = f'''
        <UniformGrid Columns="2" Margin="0,0,0,8">
            <local:MyListItem 
                Margin="0,2,10,8"
                Title="{title}" 
                Info="{time}"
                EventType="打开网页" 
                EventData="https://cn.bing.com/search?q={title}" 
                Type="Clickable" />
            '''
        elif i == 10:
            line = f'''
            <local:MyListItem 
                Margin="0,2,10,8"
                Title="{title}" 
                Info="{time}"
                EventType="打开网页" 
                EventData="https://cn.bing.com/search?q={title}" 
                Type="Clickable" />
        </UniformGrid>
            '''
        else:
            line = f'''
            <local:MyListItem 
                Margin="0,2,10,8"
                Title="{title}" 
                Info="{time}"
                EventType="打开网页" 
                EventData="https://cn.bing.com/search?q={title}" 
                Type="Clickable" />'''
            
        items.append(line)
    return "\n".join(items)

def generate_xaml(toutionews_data, nend, wbd, wyd, bilid, history_data):
    today = calendar.get_holiday_detail(datetime.now(pytz.timezone('Asia/Shanghai')))
    today_holiday = ""
    if today is True:
        if calendar.Holiday.labour_day.value:
            today_holiday = f"今天是{datetime.now(pytz.timezone('Asia/Shanghai')).strftime('%Y年%m月%d日')}，今天放假！"
        else:
            today_holiday = f"今天是{datetime.now(pytz.timezone('Asia/Shanghai')).strftime('%Y年%m月%d日')}，今天是周末！"
    else:
        today_holiday = f"今天是{datetime.now(pytz.timezone('Asia/Shanghai')).strftime('%Y年%m月%d日')}，今天是工作日。"


    toutionews_items = ""
    if toutionews_data and toutionews_data.get("status") == "success":
        toutionews_items = doutiaonewsdata___(toutionews_data["data"][:10])
    else:
        toutionews_items = '<TextBlock TextWrapping="Wrap" Margin="0,0,0,4" Foreground="Red">获取今日头条失败</TextBlock>'

    nend_items = ""
    if nend and nend.get("status") != "success":
        nend_items = nend___(nend["idlist"][0]["newslist"][:11])
    else:
        nend_items = '<TextBlock TextWrapping="Wrap" Margin="0,0,0,4" Foreground="Red">获取今日新闻失败</TextBlock>'

    wb_it = ""
    if wbd and wbd.get("type") == "weibo":
        wb_it = wb(wbd["list"][:10])
        print("成功")
    else:
        wb_it = '<TextBlock TextWrapping="Wrap" Margin="0,0,0,4" Foreground="Red">获取微博失败</TextBlock>'

    wy_it = ""
    if wyd and wyd.get("code") == 200:
        wy_it = wy(wyd["data"]["list"][:10])
    else:
        wy_it = '<TextBlock TextWrapping="Wrap" Margin="0,0,0,4" Foreground="Red">获取网易新闻失败</TextBlock>'

    # blit = ""
    # if bilid and bilid.get("code") == 0:
    #     blit = bili(bilid["data"]["list"][:10])
    # else:
    #     blit = '<TextBlock TextWrapping="Wrap" Margin="0,0,0,4" Foreground="Red">获取哔哩哔哩失败</TextBlock>'

    xaml_content = f'''
<!-- 这是 PCL 的主页自定义文件。由 Python 脚本自动生成 -->
<local:MyCard Title="📅 今日" Margin="0,0,0,15" CanSwap="False">
    <StackPanel Margin="25,40,23,15">
        <TextBlock TextWrapping="Wrap" Margin="0,0,0,4" FontSize="16">{today_holiday}</TextBlock>
        <TextBlock TextWrapping="Wrap" Margin="0,10,0,0" FontSize="11" Foreground="#888">
            更新时间: {datetime.now(pytz.timezone('Asia/Shanghai')).strftime("%Y-%m-%d %H:%M:%S")}
        </TextBlock>
        <local:MyIconTextButton Margin="-15,10,0,0" Height="35" HorizontalAlignment="Left"
                    Text="刷新主页" EventType="刷新主页" Grid.Column="1"
                    LogoScale="0.8" ColorType="Highlight"
                    Logo="M256.455,8C322.724,8.119,382.892,34.233,427.314,76.685L463.029,40.97C478.149,25.851,504,36.559,504,57.941L504,192C504,205.255,493.255,216,480,216L345.941,216C324.559,216,313.851,190.149,328.97,175.029L370.72,133.279C339.856,104.38 299.919,88.372 257.49,88.006 165.092,87.208 87.207,161.983 88.0059999999999,257.448 88.764,348.009 162.184,424 256,424 297.127,424 335.997,409.322 366.629,382.444 371.372,378.283 378.535,378.536 382.997,382.997L422.659,422.659C427.531,427.531 427.29,435.474 422.177,440.092 378.202,479.813 319.926,504 256,504 119.034,504 8.001,392.967 8,256.002 7.999,119.193 119.646,7.755 256.455,8z" />
    </StackPanel>
</local:MyCard>



<Grid Margin="0,0,0,8">
     <Grid.ColumnDefinitions>
          <ColumnDefinition Width="1*" />
          <ColumnDefinition Width="100" />
          <ColumnDefinition Width="1*" />
     </Grid.ColumnDefinitions>
     <Line X1="0" X2="100" Stroke="{{DynamicResource ColorBrush3}}" StrokeThickness="1.5"
          Stretch="Fill" Grid.Column="0" />
     <TextBlock Text="🔥 新闻热点" FontSize="15" Foreground="{{DynamicResource ColorBrush4}}" Grid.Column="1"
          VerticalAlignment="Center" HorizontalAlignment="Center" />
     <Line X1="0" X2="100" Stroke="{{DynamicResource ColorBrush3}}" StrokeThickness="1.5"
          Stretch="Fill" Grid.Column="2" />
</Grid>


<local:MyCard Title="🔥 新闻热点" Margin="0,0,0,15" CanSwap="True" IsSwapped="False">
    <StackPanel Margin="25,40,23,15">
        <UniformGrid Columns="2" Margin="0,0,0,8"> 
            <StackPanel Margin="0,2,10,8">
                <TextBlock Margin="0,4,0,6" FontWeight="Bold" Text="🔥 微博热搜" />
                {wb_it}
                <Grid>
                    <Grid.ColumnDefinitions>
                            <ColumnDefinition Width="1*" />
                    </Grid.ColumnDefinitions>
                    <local:MyButton Grid.Column="0" Margin="0,10,10,0" Height="35" Text="查看更多……" EventType="打开网页" EventData="https://weibo.com/newlogin?tabtype=search" />
                </Grid>
            </StackPanel>
            <StackPanel Margin="0,2,10,8">
                <TextBlock Margin="0,4,0,6" FontWeight="Bold" Text="🔥 头条热榜" />
                {toutionews_items}
                <Grid>
                    <Grid.ColumnDefinitions>
                            <ColumnDefinition Width="1*" />
                    </Grid.ColumnDefinitions>
                    <local:MyButton Grid.Column="0" Margin="0,10,10,0" Height="35" Text="查看更多……" EventType="打开网页" EventData="https://www.toutiao.com/" />
                </Grid>
            </StackPanel>
        </UniformGrid>
    </StackPanel>
</local:MyCard>

<local:MyCard Title="🔥 新闻热点" Margin="0,0,0,15" CanSwap="True" IsSwapped="False">
    <StackPanel Margin="25,40,23,15">
        <UniformGrid Columns="2" Margin="0,0,0,8"> 
            <StackPanel Margin="0,2,10,8">
                <TextBlock Margin="0,4,0,6" FontWeight="Bold" Text="🐧 腾讯新闻" />
                {nend_items}
                <Grid>
                    <Grid.ColumnDefinitions>
                            <ColumnDefinition Width="1*" />
                    </Grid.ColumnDefinitions>
                    <local:MyButton Grid.Column="0" Margin="0,10,10,0" Height="35" Text="查看更多……" EventType="打开网页" EventData="https://www.qq.com/" />
                </Grid>
            </StackPanel>
            <StackPanel Margin="0,2,10,8">
                <TextBlock Margin="0,4,0,6" FontWeight="Bold" Text="🆕 网易新闻" />
                {wy_it}
                <Grid>
                    <Grid.ColumnDefinitions>
                            <ColumnDefinition Width="1*" />
                    </Grid.ColumnDefinitions>
                    <local:MyButton Grid.Column="0" Margin="0,10,0,0" Height="35" Text="查看更多……" EventType="打开网页" EventData="https://www.163.com/" />
                </Grid>
            </StackPanel>
        </UniformGrid>
    </StackPanel>
</local:MyCard>

'''
    with open("index.xaml", "w", encoding="utf-8") as f:
        f.write(xaml_content)
    print("✅ index.xaml 文件已生成！")

def main():
    print("📡 正在获取新闻与节假日信息...")
    toutiao_news = fetch_data(TOUTIAO_URL)
    print("-------头条-------\n\n\n\n\n")
    time.sleep(1)
    nend_news = fetch_data(QQ_URL)
    print("-------QQ-------\n\n\n\n\n")
    time.sleep(1)
    wb = fetch_data(WEIBO_URL)
    print("-------weibo-------\n\n\n\n\n")
    # wb = "0"
    time.sleep(1)
    wy = fetch_data(WY_URL)
    print("-------wy-------\n\n\n\n\n")
    time.sleep(1)
    # bilibili = fetech_data_bili(BILIBILI_URL)
    # time.sleep(1)
    bilibili = "0"
    # china_news = fetch_data(CHINA_NEWS_URL)
    # time.sleep(1)
    # world_news = fetch_data(WORLD_NEWS_URL)
    # time.sleep(1)
    # holiday_info = fetch_data(HOLIDAY_URL)
    # time.sleep(1)
    # history = fetch_data(TODAY_INTHEHISTORY_URL)
    history = "0"

    generate_xaml(toutiao_news, nend_news, wb, wy, bilibili, history)

    # 生成版本号：YYYYMMDD-HHMM（24小时制）
    version_str = datetime.now(pytz.timezone('Asia/Shanghai')).strftime("%Y-%m-%d %H:%M:%S")
        
    # 写入 version 文件
    with open('index.xaml.ini', 'w', encoding='utf-8') as f:
        f.write(version_str)
    print(f"✅ 已更新 index.xaml.ini: {version_str}")


if __name__ == "__main__":
    main()

'''
<Grid Margin="0,0,0,8">
     <Grid.ColumnDefinitions>
          <ColumnDefinition Width="1*" />
          <ColumnDefinition Width="100" />
          <ColumnDefinition Width="1*" />
     </Grid.ColumnDefinitions>
     <Line X1="0" X2="100" Stroke="{{DynamicResource ColorBrush3}}" StrokeThickness="1.5"
          Stretch="Fill" Grid.Column="0" />
     <TextBlock Text="📺 热门视频" FontSize="15" Foreground="{{DynamicResource ColorBrush4}}" Grid.Column="1"
          VerticalAlignment="Center" HorizontalAlignment="Center" />
     <Line X1="0" X2="100" Stroke="{{DynamicResource ColorBrush3}}" StrokeThickness="1.5"
          Stretch="Fill" Grid.Column="2" />
</Grid>

<local:MyCard Title="📺 热门视频" Margin="0,0,0,15" CanSwap="True" IsSwapped="False">
    <StackPanel Margin="25,40,23,15">
        <UniformGrid Columns="1" Margin="0,0,0,8"> 
            <StackPanel Margin="0,2,10,8">
                <TextBlock Margin="0,4,0,6" FontWeight="Bold" Text="📺 哔哩哔哩" />
                {blit}
                <Grid>
                    <Grid.ColumnDefinitions>
                            <ColumnDefinition Width="1*" />
                    </Grid.ColumnDefinitions>
                    <local:MyButton Grid.Column="0" Margin="0,10,10,0" Height="35" Text="查看更多……" EventType="打开网页" EventData="https://www.bilibili.com/v/popular/rank/all" />
                </Grid>
            </StackPanel>
        </UniformGrid>
    </StackPanel>
</local:MyCard>

<local:MyCard Title="📖 历史上的今天" Margin="0,0,0,15" CanSwap="True" IsSwapped="True">
    <StackPanel Margin="25,40,23,15">
{history_text}
    </StackPanel>
</local:MyCard>


<Grid Margin="0,0,0,8">
     <Grid.ColumnDefinitions>
          <ColumnDefinition Width="1*" />
          <ColumnDefinition Width="100" />
          <ColumnDefinition Width="1*" />
     </Grid.ColumnDefinitions>
     <Line X1="0" X2="100" Stroke="{{DynamicResource ColorBrush3}}" StrokeThickness="1.5"
          Stretch="Fill" Grid.Column="0" />
     <TextBlock Text="📺 CCTV 新闻" FontSize="15" Foreground="{{DynamicResource ColorBrush4}}" Grid.Column="1"
          VerticalAlignment="Center" HorizontalAlignment="Center" />
     <Line X1="0" X2="100" Stroke="{{DynamicResource ColorBrush3}}" StrokeThickness="1.5"
          Stretch="Fill" Grid.Column="2" />
</Grid>

<local:MyCard Title="📰 CCTV 国内新闻" Margin="0,0,0,15" CanSwap="True" IsSwapped="False">
    <StackPanel Margin="25,40,23,15">
    </StackPanel>
</local:MyCard>

<local:MyCard Title="🌍 CCTV 国际新闻" Margin="0,0,0,15" CanSwap="True" IsSwapped="True">
    <StackPanel Margin="25,40,23,15">
    </StackPanel>
</local:MyCard>
'''