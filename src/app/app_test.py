from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import io
import re
import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from retrieval.retriever import (
    load_retriever,
    search_chunks,
    build_retrieved_context,
)
from core.report_generator import generate_report


def render_knowledge_card(title, text, sources, background_path=None):
    # --- 1. 基礎參數設定 ---
    CARD_WIDTH = 1400
    PADDING_X = 110 
    PADDING_Y = 100
    RADIUS = 70      

    # 保持您現有的配色方案
    COLOR_TEXT = (255, 255, 255, 255)     
    COLOR_MUTED = (255, 255, 255, 170)    
    COLOR_ACCENT = (255, 255, 255, 220)   
    COLOR_DIVIDER = (255, 255, 255, 50)   
    
    # 保持您現有的質感參數
    GLASS_TINT = (255, 255, 255, 15)      
    BORDER_WHITE = (255, 255, 255, 100)    
    INNER_GLOW = (255, 255, 255, 40)

    # 字體加載
    FONT_PATH = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
    FONT_BOLD_PATH = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
    
    def get_font(path, size):
        try: return ImageFont.truetype(path, size)
        except: return ImageFont.load_default()

    font_title = get_font(FONT_BOLD_PATH, 72) 
    font_h2 = get_font(FONT_BOLD_PATH, 46)    
    font_text = get_font(FONT_PATH, 34)
    font_source_title = get_font(FONT_BOLD_PATH, 34)
    font_source = get_font(FONT_PATH, 30)

    # --- 2. 文本處理與佈局計算 ---
    def wrap_line(draw, text_line, font, max_width):
        if not text_line: return [""]
        wrapped, current = [], ""
        for ch in text_line:
            w = draw.textbbox((0, 0), current + ch, font=font)[2]
            if w <= max_width: current += ch
            else:
                wrapped.append(current); current = ch
        if current: wrapped.append(current)
        return wrapped

    temp_draw = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    lines = text.splitlines()
    clean_lines, extracted_title = [], title
    for l in lines:
        s = l.strip()
        if s.startswith("# "): 
            extracted_title = s.replace("# ", "").strip(); continue
        if s == "---": clean_lines.append("__DIVIDER__")
        elif s.startswith("##"): clean_lines.append(f"§H2§{s.replace('##', '').strip()}")
        else: clean_lines.append(s)

    layout = []
    max_w = CARD_WIDTH - 2 * PADDING_X
    
    # 精確累計高度起點
    curr_y = PADDING_Y
    
    # 標題區高度計算
    title_bbox = temp_draw.textbbox((0, 0), extracted_title, font=font_title)
    # 這裡使用 bbox 的實際高度
    title_h = title_bbox[3] - title_bbox[1]
    layout.append(("title", extracted_title, curr_y))
    curr_y += title_h + 50 # 標題文字後間距
    
    layout.append(("line", None, curr_y))
    curr_y += 50 # 分隔線後間距

    for line in clean_lines:
        if line == "__DIVIDER__":
            layout.append(("divider", None, curr_y))
            curr_y += 60
        elif line == "":
            curr_y += 30 # 空行僅增加高度
        elif line.startswith("§H2§"):
            h2_t = line.replace("§H2§", "")
            wrapped = wrap_line(temp_draw, h2_t, font_h2, max_w)
            for wl in wrapped:
                layout.append(("h2", wl, curr_y))
                bbox = temp_draw.textbbox((0, 0), wl, font=font_h2)
                curr_y += (bbox[3] - bbox[1]) + 18
            curr_y += 12 # 補償 H2 段落間距
        else:
            wrapped = wrap_line(temp_draw, line, font_text, max_w)
            for wl in wrapped:
                layout.append(("text", wl, curr_y))
                bbox = temp_draw.textbbox((0, 0), wl, font=font_text)
                curr_y += (bbox[3] - bbox[1]) + 18
    
    # Sources 區域高度計算
    curr_y += 40 # 內容結束到 Sources 標題的間距
    layout.append(("src_title", "SOURCES", curr_y))
    src_title_bbox = temp_draw.textbbox((0, 0), "SOURCES", font=font_source_title)
    curr_y += (src_title_bbox[3] - src_title_bbox[1]) + 30
    
    for s in sources:
        wrapped = wrap_line(temp_draw, f"• {s}", font_source, max_w)
        for wl in wrapped:
            layout.append(("src", wl, curr_y))
            bbox = temp_draw.textbbox((0, 0), wl, font=font_source)
            curr_y += (bbox[3] - bbox[1]) + 20

    # 最終高度 = 最後一個元素的位置 + 底部 padding
    total_card_h = int(curr_y + PADDING_Y)

    # --- 3. 圖像合成 (保持風格) ---
    if background_path and os.path.exists(background_path):
        bg_full = Image.open(background_path).convert("RGBA")
        bg_full = ImageEnhance.Color(bg_full).enhance(1.2)
        
        bg_w, bg_h = bg_full.size
        scale = max(CARD_WIDTH / bg_w, total_card_h / bg_h)
        new_size = (int(bg_w * scale), int(bg_h * scale))
        bg_resized = bg_full.resize(new_size, Image.Resampling.LANCZOS)
        offset_x, offset_y = (new_size[0]-CARD_WIDTH)//2, (new_size[1]-total_card_h)//2
        card_img = bg_resized.crop((offset_x, offset_y, offset_x + CARD_WIDTH, offset_y + total_card_h))
    else:
        card_img = Image.new("RGBA", (CARD_WIDTH, total_card_h), (45, 50, 60, 255))

    card_img = card_img.filter(ImageFilter.GaussianBlur(radius=60))
    card_img = ImageEnhance.Brightness(card_img).enhance(0.85)

    glass_overlay = Image.new("RGBA", card_img.size, GLASS_TINT)
    card_img = Image.alpha_composite(card_img, glass_overlay)

    # 繪製文字
    draw = ImageDraw.Draw(card_img)
    x = PADDING_X
    
    for item in layout:
        kind, val, pos_y = item
        if kind == "title":
            draw.text((x, pos_y), val, font=font_title, fill=COLOR_TEXT)
        elif kind == "line":
            draw.line([(x, pos_y), (x + max_w, pos_y)], fill=COLOR_DIVIDER, width=1)
        elif kind == "divider":
            draw.line([(x, pos_y + 25), (x + max_w, pos_y + 25)], fill=COLOR_DIVIDER, width=1)
        elif kind == "h2":
            draw.text((x, pos_y), val, font=font_h2, fill=COLOR_TEXT)
        elif kind == "text":
            draw.text((x, pos_y), val, font=font_text, fill=COLOR_TEXT)
        elif kind == "src_title":
            draw.text((x, pos_y), val, font=font_source_title, fill=COLOR_ACCENT)
        elif kind == "src":
            draw.text((x, pos_y), val, font=font_source, fill=COLOR_MUTED)

    # --- 4. 圓角與修飾 ---
    final_output = Image.new("RGBA", (CARD_WIDTH, total_card_h), (255, 255, 255, 0))
    mask = Image.new("L", (CARD_WIDTH, total_card_h), 0)
    ImageDraw.Draw(mask).rounded_rectangle([(0, 0), (CARD_WIDTH, total_card_h)], radius=RADIUS, fill=255)
    final_output.paste(card_img, (0, 0), mask)
    
    final_draw = ImageDraw.Draw(final_output)
    # 內描邊與外框，嚴格貼合畫布邊緣
    final_draw.rounded_rectangle([(3, 3), (CARD_WIDTH-3, total_card_h-3)], radius=RADIUS, outline=INNER_GLOW, width=4)
    final_draw.rounded_rectangle([(0, 0), (CARD_WIDTH, total_card_h)], radius=RADIUS, outline=BORDER_WHITE, width=2)

    buffer = io.BytesIO()
    final_output.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer


st.set_page_config(page_title="ML Knowledge RAG", layout="wide")
st.title("ML Knowledge RAG")

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))
KNOWLEDGE_DIR = os.path.join(PROJECT_ROOT, "knowledge")
BACKGROUND_PATH = os.path.join(PROJECT_ROOT, "assets", "bg.jpg")


@st.cache_resource
def get_retriever():
    return load_retriever(KNOWLEDGE_DIR)


retriever_state = get_retriever()

mock_mode = st.toggle("Mock UI 測試模式", value=True)
question = st.text_input("Ask a question", value="What is probability?")

if question:
    with st.spinner("Retrieving and generating..."):
        results = search_chunks(question, retriever_state, top_k=3)
        context = build_retrieved_context(results)

        result = generate_report(
            context=context,
            question=question,
            mock=mock_mode,
        )

    st.markdown(result)

    st.markdown("---")
    st.markdown("### 資料來源")

    if mock_mode:
        source_list = [
            "probability.md",
            "logit.md",
            "threshold.md",
        ]
        for filename in source_list:
            st.markdown(f"- **{filename}** — Mock Source")
    else:
        for item in results:
            filename = os.path.basename(item["source"])
            item_title = item["title"] if item["title"] else "Untitled"
            st.markdown(f"- **{filename}** — {item_title}")

        source_list = [os.path.basename(x["source"]) for x in results]

    png_buffer = render_knowledge_card(
        title="ML Knowledge RAG",
        text=result,
        sources=source_list,
        background_path=BACKGROUND_PATH,
    )

    st.download_button(
        label="Download Knowledge Card (.png)",
        data=png_buffer,
        file_name="knowledge_card.png",
        mime="image/png"
    )