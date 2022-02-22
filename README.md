## FindGoods專題的爬蟲程式

### 爬取的網站
- ikea
- pinkoi
- trplus

### 執行過程
- 爬取專題中所需七種傢俱
- 從第一頁開始抓取每筆商品資訊
  - ＩＤ
  - 名稱
  - 圖片
  - 網址
  - 評價
- 抓取完單筆商品資訊後，寫入mongoDB中
- 下載的圖片會存至當前目錄下./商店名稱/商品類別 資料夾中，以便後續物件辨識模型訓練使用
- 最後 trans_mysql.py 將後續網頁會使用的資訊轉換到mySQL資料庫中，方便網頁讀取資訊
