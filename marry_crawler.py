from bs4 import BeautifulSoup
import requests
from openpyxl import Workbook
import re
import time
import emoji
import json



#excel表建立

wb = Workbook()
ws = wb.active
title = ['廠商firm','評價Rank', '評論comment']
ws.append(title)




# 反反爬蟲

header = {
    'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15'
    }

# 按頁碼爬取

for index in range(31,33):
    url = 'https://www.marry.com.tw/reviews-kwbt2003mmpg'
    url = url + str(index) + 'mm'
    print(url)
    response = requests.get(url, verify=False, headers = header)
    soup = BeautifulSoup(response.text, "html.parser")
    
    
    #轉換成json
    
    html = soup.find_all("script",type = "application/ld+json")[2]
    html = html.string.replace("\r\n",'') #去除換行
    root_json = json.loads(html, strict = False)


    #篩選出有價值的資料

    
    for data in root_json:
        
        db =[]
        
        firm = data['itemReviewed']['name']        #找出廠商
        rank = data['reviewRating']['ratingValue'] #找出評價
        raw_comment = data['reviewBody']           #找出評論
        
        
        #前處理 移除評論中的emoji
        
        str_emoji = emoji.demojize(raw_comment)
        comment = re.sub(':\S+?:', ' ', str_emoji)
        
        
        #將找到的資料寫入excel
        
        db.append(firm)
        db.append(rank)
        db.append(comment)
        
        ws.append(db)
        
        time.sleep(1) # 反反爬蟲



wb.save('data.xlsx') #儲存檔案