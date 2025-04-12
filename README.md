# CSV 到 HTML 轉換工具

這是一個將 CSV 格式的配置文件轉換為互動式 HTML 頁面的工具。該工具可以將具有層級結構的 CSV 數據轉換為美觀的、可互動的 HTML 頁面，支援主題切換和節點展開/折疊功能。

## 功能特點

- 將 CSV 格式的配置文件轉換為 JSON 結構
- 生成美觀的互動式 HTML 頁面
- 支援深色/淺色主題切換
- 支援節點展開/折疊功能
- 支援多級層級結構顯示
- 顯示數據類型、預設值和註釋信息
- 響應式設計，適配不同螢幕尺寸

## 文件結構

- `csv_to_html.py`: 主程序文件
- `data.csv`: 示例 CSV 配置文件
- `output.html`: 生成的 HTML 文件

## 使用方法

1. 確保已安裝所需的 Python 依賴：
   ```bash
   pip install pandas
   ```

2. 準備 CSV 文件：
   - CSV 文件應包含以下列：JSON Format, Data Type, Default Value, Comment
   - 使用縮進來表示層級結構
   - 示例格式請參考 `data.csv`

3. 運行程序：
   ```bash
   python csv_to_html.py
   ```

4. 查看結果：
   - 程序會在當前目錄生成 `output.html` 文件
   - 用瀏覽器打開該文件即可查看結果

## CSV 文件格式說明

CSV 文件應遵循以下格式：
- 第一行為標題行
- 使用縮進（空列）表示層級結構
- 每行包含以下信息：
  - 節點名稱
  - 數據類型（可選）
  - 預設值（可選）
  - 註釋（可選）

## HTML 頁面功能

生成的 HTML 頁面提供以下功能：
- 主題切換：點擊右上角的"切換主題"按鈕
- 展開/折疊：點擊節點前的箭頭圖標
- 展開全部：點擊右上角的"展開全部"按鈕
- 折疊全部：點擊右上角的"折疊全部"按鈕

## 示例

CSV 文件示例：
```
JSON Format,,,,,,,,Data Type,Default Value,Comment
network,,,,,,,,,,,,,,,,,
,id,,,,,,,string,1,1~1000
,country,,,,,,,string,840,Follow Country Table
,ethernet,,,,,,,,,,,,,,,,,
,,ip,,,,,,string,192.168.1.1,ip string
```

## 注意事項

- 確保 CSV 文件使用 UTF-8 編碼
- 縮進層級不要超過 10 層
- 建議使用文本編輯器編輯 CSV 文件，避免使用 Excel 等工具 