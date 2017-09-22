# make_a_spider

嘗試做一個排程，多進程的爬蟲
需要安裝redis

## 使用
先打開監聽的程式(獨立在一個Console運行)
```
$ python start.py -c 進程數
```
(以下開在另一個Console)
執行ptt爬蟲
```
$python ptt.py  -s 開始頁 -e 結束頁(-1為最後一頁) -b 看板名 -o 輸出檔案檔名
```
執行591爬蟲
```
$python s591.py  -s 開始頁 -e 結束頁(-1為最後一頁) -o 輸出檔案檔名
```
執行東海課程爬蟲
```
$python thu.py  -y 學年 -s 學期 -o 輸出檔案檔名
```
