from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import io
import os
import sys
import re
import random
import datetime

import streamlit as st
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from retrieval.retriever import (
    load_retriever,
    search_chunks,
    build_retrieved_context,
)
from core.report_generator import generate_report


# =========================
# Environment
# =========================
load_dotenv()


# =========================
# Paths
# =========================
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))

ASSETS_DIR = os.path.join(PROJECT_ROOT, "assets")
KNOWLEDGE_DIR = os.path.join(PROJECT_ROOT, "knowledge", "ml")
CARDS_DIR = os.path.join(CURRENT_DIR, "generated_cards")

BACKGROUND_PATH = os.path.join(ASSETS_DIR, "bg.jpg")
FONT_PATH = os.path.join(ASSETS_DIR, "fonts", "NotoSansCJK-Regular.ttc")
FONT_BOLD_PATH = os.path.join(ASSETS_DIR, "fonts", "NotoSansCJK-Bold.ttc")

if not os.path.exists(CARDS_DIR):
    os.makedirs(CARDS_DIR)

if not os.path.exists(FONT_PATH):
    FONT_PATH = os.path.join(PROJECT_ROOT, "fonts", "NotoSansCJK-Regular.ttc")
if not os.path.exists(FONT_BOLD_PATH):
    FONT_BOLD_PATH = os.path.join(PROJECT_ROOT, "fonts", "NotoSansCJK-Bold.ttc")

# =========================
# Helpers
# =========================
def get_font(path: str, size: int):
    try:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
        return ImageFont.load_default()
    except Exception:
        return ImageFont.load_default()

def clean_math_and_markdown(text: str) -> str:
    """處理 LaTeX 與 Markdown 渲染相容性"""
    if not text: return ""
    replacements = {
        r"\\sigma": "σ", r"\\infty": "∞", r"\\rightarrow": "→",
        r"\\pm": "±", r"\\neq": "≠", r"\\approx": "≈",
        r"\\le": "≤", r"\\ge": "≥", r"\\times": "×",
        r"\\div": "÷", r"\\theta": "θ", r"\\lambda": "λ",
        r"\\frac\{1\}\{1 \+ e\^\{-z\}\}": "1 / (1 + e^-z)", 
        r"\$": "", 
    }
    for lat, uni in replacements.items():
        text = re.sub(lat, uni, text)
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"\*(.*?)\*", r"\1", text)
    text = re.sub(r"`(.*?)`", r"\1", text)
    return text

def wrap_line(draw, text_line, font, max_width):
    if not text_line: return [""]
    wrapped, current = [], ""
    for ch in text_line:
        bbox = draw.textbbox((0, 0), current + ch, font=font)
        if (bbox[2] - bbox[0]) <= max_width:
            current += ch
        else:
            wrapped.append(current)
            current = ch
    if current: wrapped.append(current)
    return wrapped

def extract_title_and_layout(text: str, fallback_title: str, draw, fonts, card_width, padding_x, padding_y):
    font_title, font_h2, font_text, _, _ = fonts
    max_w = card_width - 2 * padding_x
    lines = text.splitlines()

    clean_lines = []
    extracted_title = fallback_title.strip() if fallback_title else ""
    title_taken = False

    for raw_line in lines:
        s = clean_math_and_markdown(raw_line.strip())

        if not s:
            continue

        # 1. 優先抓第一個一級標題作為卡片 title，並且不放進內文
        if not title_taken and re.match(r"^#\s*", s):
            extracted_title = re.sub(r"^#\s*", "", s).strip()
            title_taken = True
            continue

        # 2. 如果還沒有抓到 title，就把第一個非空行當 title，並且不放進內文
        if not title_taken and not extracted_title:
            extracted_title = s
            title_taken = True
            continue

        # 3. 二級標題保留在內文
        if re.match(r"^##\s*", s):
            h2_text = re.sub(r"^##\s*", "", s).strip()
            clean_lines.append(f"§H2§{h2_text}")
            continue

        # 4. divider 保留
        if s == "---":
            clean_lines.append("__DIVIDER__")
            continue

        # 5. 其他內容正常保留
        clean_lines.append(s)

    # 6. 最後備援 title
    if not extracted_title:
        extracted_title = "ML Concept Card"

    layout = []
    curr_y = padding_y

    # title 自動換行
    t_lines = wrap_line(draw, extracted_title, font_title, max_w)
    for tl in t_lines:
        layout.append(("title", tl, curr_y))
        t_bbox = draw.textbbox((0, 0), tl, font=font_title)
        curr_y += (t_bbox[3] - t_bbox[1]) + 15

    # title 下方主線
    curr_y += 70
    layout.append(("line", None, curr_y))
    curr_y += 65

    first_h2_seen = False
    # body
    for line in clean_lines:
        if line == "__DIVIDER__":
            layout.append(("divider", None, curr_y + 20))
            curr_y += 60

        elif line.startswith("§H2§"):
            h2_text = line.replace("§H2§", "")

            if first_h2_seen:
                layout.append(("divider", None, curr_y + 10))
                curr_y += 50

            first_h2_seen = True
            for wl in wrap_line(draw, h2_text, font_h2, max_w):
                layout.append(("h2", wl, curr_y))
                bbox = draw.textbbox((0, 0), wl, font=font_h2)
                curr_y += (bbox[3] - bbox[1]) + 28
            
            curr_y += 10    

        else:
            for wl in wrap_line(draw, line, font_text, max_w):
                layout.append(("text", wl, curr_y))
                bbox = draw.textbbox((0, 0), wl, font=font_text)
                curr_y += (bbox[3] - bbox[1]) + 26

    return extracted_title, layout, curr_y, max_w

def append_sources_layout(layout, curr_y, sources, draw, font_source_title, font_source, max_w):
    curr_y += 40
    layout.append(("src_title", "SOURCES", curr_y))
    curr_y += 60
    for source in sources:
        for wl in wrap_line(draw, f"• {source}", font_source, max_w):
            layout.append(("src", wl, curr_y))
            bbox = draw.textbbox((0, 0), wl, font=font_source)
            curr_y += (bbox[3] - bbox[1]) + 15
    return layout, curr_y

def build_card_background(card_width, total_card_h, background_path):
    if background_path and os.path.exists(background_path):
        bg_full = Image.open(background_path).convert("RGBA")
        bg_w, bg_h = bg_full.size
        scale = max(card_width / bg_w, total_card_h / bg_h)
        new_size = (int(bg_w * scale), int(bg_h * scale))
        bg_resized = bg_full.resize(new_size, Image.Resampling.LANCZOS)
        offset_x, offset_y = (new_size[0] - card_width) // 2, (new_size[1] - total_card_h) // 2
        card_img = bg_resized.crop((offset_x, offset_y, offset_x + card_width, offset_y + total_card_h))
    else:
        card_img = Image.new("RGBA", (card_width, total_card_h), (45, 50, 60, 255))
    card_img = card_img.filter(ImageFilter.GaussianBlur(radius=50))
    card_img = ImageEnhance.Brightness(card_img).enhance(0.8)
    return Image.alpha_composite(card_img, Image.new("RGBA", card_img.size, (255, 255, 255, 15)))

def render_knowledge_card(title, text, sources, background_path=None):
    card_width, padding_x, padding_y, radius = 1400, 110, 100, 70
    colors = ((255,255,255,255), (255,255,255,170), (255,255,255,220), (255,255,255,50))
    fonts = (get_font(FONT_BOLD_PATH, 72), get_font(FONT_BOLD_PATH, 40), get_font(FONT_PATH, 34), get_font(FONT_BOLD_PATH, 34), get_font(FONT_PATH, 30))

    BACKGROUND_LIST = ["bg.jpg", "bg2.jpg", "bg3.jpg"]
    selected_bg_file = random.choice(BACKGROUND_LIST)
    selected_bg_path = os.path.join(ASSETS_DIR, selected_bg_file)
    final_bg_path = background_path if background_path and os.path.exists(background_path) else selected_bg_path

    temp_draw = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    extracted_title, layout, curr_y, max_w = extract_title_and_layout(text, title, temp_draw, fonts, card_width, padding_x, padding_y)
    layout, curr_y = append_sources_layout(layout, curr_y, sources, temp_draw, fonts[3], fonts[4], max_w)

    total_card_h = int(curr_y + padding_y)
    card_img = build_card_background(card_width, total_card_h, final_bg_path)
    
    draw = ImageDraw.Draw(card_img)
    color_text, color_muted, color_accent, color_divider = colors
    for kind, val, pos_y in layout:
        if kind == "title": draw.text((padding_x, pos_y), val, font=fonts[0], fill=color_text)
        elif kind == "line": draw.line([(padding_x, pos_y), (padding_x + max_w, pos_y)], fill=color_divider, width=2)
        elif kind == "divider": draw.line([(padding_x, pos_y + 25), (padding_x + max_w, pos_y + 25)], fill=color_divider, width=1)
        elif kind == "h2": draw.text((padding_x, pos_y), val, font=fonts[1], fill=color_text)
        elif kind == "text": draw.text((padding_x, pos_y), val, font=fonts[2], fill=color_text)
        elif kind == "src_title": draw.text((padding_x, pos_y), val, font=fonts[3], fill=color_accent)
        elif kind == "src": draw.text((padding_x, pos_y), val, font=fonts[4], fill=color_muted)

    mask = Image.new("L", (card_width, total_card_h), 0)
    ImageDraw.Draw(mask).rounded_rectangle([(0, 0), (card_width, total_card_h)], radius=radius, fill=255)
    final_output = Image.new("RGBA", (card_width, total_card_h), (0,0,0,0))
    final_output.paste(card_img, (0, 0), mask)
    ImageDraw.Draw(final_output).rounded_rectangle([(0, 0), (card_width, total_card_h)], radius=radius, outline=(255, 255, 255, 60), width=3)

    buffer = io.BytesIO()
    final_output.save(buffer, format="PNG")
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    final_output.save(os.path.join(CARDS_DIR, f"card_{timestamp}.png"))
    buffer.seek(0)
    return buffer

@st.cache_resource
def get_retriever(): 
    if not os.path.exists(KNOWLEDGE_DIR):
        os.makedirs(KNOWLEDGE_DIR, exist_ok=True)
    return load_retriever(KNOWLEDGE_DIR)

# =========================
# State Management
# =========================
if "last_result" not in st.session_state: st.session_state.last_result = ""
if "last_sources" not in st.session_state: st.session_state.last_sources = []
if "last_png" not in st.session_state: st.session_state.last_png = None

# =========================
# Streamlit Page Config
# =========================
st.set_page_config(page_title="ML Knowledge RAG", layout="wide")
st.title("ML Concept Engine")

# =========================
# Main UI
# =========================
retriever_state = get_retriever()
question = st.text_input("Ask ML questions and generate visual explanation cards")
if st.button("Enter") and question:
    try:
        with st.spinner("思考與檢索中..."):
            results = search_chunks(question, retriever_state, top_k=3)
            context = build_retrieved_context(results)
            result = generate_report(context=context, question=question)
            
            source_list = [os.path.basename(r["source"]) for r in results]
            png_buffer = render_knowledge_card("", result, source_list if source_list else ["Unknown"], None)
            
            st.session_state.last_result = result
            st.session_state.last_sources = [f"- **{os.path.basename(r['source'])}** — {r['title']}" for r in results]
            st.session_state.last_png = png_buffer.getvalue()
    except Exception as e:
        st.error(f"Error: {e}")

# --- 新增功能：遞迴列出 ml 下所有子資料夾的 MD 檔案 ---
st.markdown("### Available ML Concepts")
try:
    if os.path.exists(KNOWLEDGE_DIR):
        all_md_info = []
        # 使用 os.walk 進行遞迴掃描
        for root, dirs, files in os.walk(KNOWLEDGE_DIR):
            for file in files:
                if file.endswith(".md"):
                    # 計算相對路徑以便顯示類別
                    rel_path = os.path.relpath(root, KNOWLEDGE_DIR)
                    category = "Root" if rel_path == "." else rel_path
                    all_md_info.append({"name": file, "category": category})

        if all_md_info:
            # 按類別排序
            all_md_info.sort(key=lambda x: (x["category"], x["name"]))
            
            with st.expander(f"可查詢概念列表 ( {len(all_md_info)} page )"):
                current_cat = None
                for info in all_md_info:
                    if info["category"] != current_cat:
                        current_cat = info["category"]
                        st.markdown(f"**📁：{current_cat}**")
                    st.write(f"&nbsp;&nbsp;&nbsp;&nbsp;📄 `{info['name']}`")
        else:
            st.info(f"知識庫資料夾 `{KNOWLEDGE_DIR}` 中目前沒有任何 .md 檔案。")
    else:
        st.error(f"找不到指定的知識庫目錄: `{KNOWLEDGE_DIR}`")
except Exception as e:
    st.warning(f"無法讀取知識庫清單: {e}")

st.markdown("---") 

# 顯示目前的結果
if st.session_state.last_result:
    st.markdown(st.session_state.last_result)
    st.markdown("---")
    for line in st.session_state.last_sources: st.markdown(line)
    if st.session_state.last_png:
        st.download_button("Download card", st.session_state.last_png, "knowledge_card.png", "image/png")

# 歷史卡片區
st.subheader("最新生成卡片")
if os.path.exists(CARDS_DIR):
    all_files = sorted([f for f in os.listdir(CARDS_DIR) if f.endswith(".png")], 
                       key=lambda x: os.path.getmtime(os.path.join(CARDS_DIR, x)), reverse=True)
    if all_files:
        cols = st.columns(5)
        for i, f in enumerate(all_files[:5]):
            with cols[i]: st.image(os.path.join(CARDS_DIR, f), use_container_width=True)
    st.markdown(f"**累計生成卡片：{len(all_files)}**")