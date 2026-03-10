# ML Concept Engine

一個基於 **LLM + RAG** 的機器學習概念解釋系統，  
可以將技術概念自動轉換成 **結構化說明與視覺知識卡片**。

🔗 Live Demo  
https://ml-concept-engine.streamlit.app/

---

## 專案介紹

ML Concept Engine 是一個 AI 輔助知識系統，  
透過 **Retrieval Augmented Generation (RAG)**  
從整理好的機器學習知識庫中檢索內容，  
並使用 LLM 生成結構化技術解釋。

系統會自動產生：

- 機器學習概念說明
- 檢索到的知識來源
- 視覺化知識卡片

使用者只需輸入問題，例如：

- capacity 與 depth 的關係？
- learning rate 是什麼
- dropout 的作用
- activation function
- model capacity
- attention mechanism

系統就會生成完整的技術說明與知識卡片。

---

## Demo

### Knowledge Base (RAG Source)

系統會從整理好的機器學習知識庫中檢索概念內容。

![Knowledge Base](assets/demo/demo_kb.png)

---

### Web Interface

使用者可以輸入機器學習問題。

![Web UI](assets/demo/demo_ui.png)

---

### Generated Knowledge Card

系統會生成結構化知識卡片。

![Knowledge Card](assets/demo/demo_card.png)

---

## 使用提示

- 本專案 UI 目前以 **桌面瀏覽器** 為主要設計目標
- 首次開啟可能需要 **數秒載入時間**

建議使用較大螢幕瀏覽

---

## 系統流程

```text
使用者輸入問題
    ↓
Streamlit Web App
    ↓
RAG Retrieval (Knowledge Base)
    ↓
Gemini LLM Generation
    ↓
PIL Generate Knowledge Card
    ↓
Upload Image to Cloudinary
    ↓
Save Card Metadata to Supabase
    ↓
Return Result to Frontend
```

---

## 系統功能

### 機器學習概念問答

使用 LLM 生成技術說明。

---

### RAG 知識檢索

系統會從整理好的 ML Markdown 知識庫中  
檢索最相關的概念內容。

---

### 自動生成知識卡片

系統會生成可視化卡片，包含：

- 概念定義
- 核心原理
- 實務觀察
- 相關概念
- 來源文件

---

### 卡片歷史紀錄

每張生成的知識卡片會：

- 上傳至 Cloudinary
- 紀錄於 Supabase

可追蹤生成歷史。

---

# 技術架構

### 前端

- Streamlit

### AI / NLP

- Gemini API
- sentence-transformers

### 後端

- Python

### 雲端服務

- Cloudinary（圖片儲存）
- Supabase（資料庫）

### 部署

- Streamlit Community Cloud

---

# 專案結構


![Architecture](assets/demo/demo_architecture.png)

#結構說明

| Folder | Description |
|------|------|
| assets | 背景圖、字體與視覺資源 |
| knowledge/ml | 機器學習概念知識庫（Markdown）持續更新中 |
| src/app | Streamlit Web App 入口 |
| src/core | 核心邏輯（LLM、Cloudinary、Supabase） |
| src/retrieval | RAG 檢索模組 |

---

# 作者

Neurons-33