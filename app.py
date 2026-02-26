
import streamlit as st
import os
import tempfile
from pathlib import Path
from config import PRESETS
import video_utils
import download_bgm


st.set_page_config(page_title="インスタ・リール自動生成ツール", layout="wide")

st.title("📱 業務用リール動画 自動生成ツール")
st.caption("Produced by LuvisYouth AI")


# ============================================================
# 🔒 Password Protection
# ============================================================
def check_password():
    """Returns `True` if the user had the correct password."""
    
    # 1. 開発/本番環境のパスワード設定
    # Streamlitの「Secrets」機能を使用して、コード上にはパスワードを書かないようにします。
    # ローカル実行時: .streamlit/secrets.toml に password = "xxx" と記述してください。
    # クラウド実行時: Streamlit Cloudの管理画面から Secrets に設定してください。
    try:
        if "password" in st.secrets:
            correct_password = st.secrets["password"]
        else:
            # Secretsはあるがパスワードキーがない場合
            st.error("⚠️ パスワード設定(Secrets)が見つかりません。")
            st.stop()
    except Exception:
        # Secrets自体が未設定の場合（ローカル初期状態など）
        st.info("💡 初期設定が必要です。プロジェクトフォルダの `.streamlit/secrets.toml` ファイルに `password = \"好きな文字\"` を追記してください。")
        st.stop()

    if "password_correct" not in st.session_state:
        st.session_state.password_correct = False

    if st.session_state.password_correct:
        return True

    # Show input
    st.warning("🔒 このツールは関係者限定です")
    password = st.text_input("パスワードを入力してください", type="password")
    
    if st.button("ログイン"):
        if password == correct_password:
            st.session_state.password_correct = True
            st.rerun()
        else:
            st.error("パスワードが違います")
            
    return False

if not check_password():
    st.stop()



# ============================================================
# 🎨 Custom CSS (Instagram Theme)
# ============================================================
st.markdown("""
<style>
    /* Font & Base Colors */
    html, body, [class*="css"] {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Buttons: Instagram Gradient */
    div.stButton > button {
        background: linear-gradient(45deg, #f09433 0%, #e6683c 25%, #dc2743 50%, #cc2366 75%, #bc1888 100%);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        transition: transform 0.2s;
    }
    div.stButton > button:hover {
        transform: scale(1.02);
        color: white;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #fafafa;
        border-right: 1px solid #dbdbdb;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #262626;
        font-weight: 700;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: #fff;
        border: 1px solid #dbdbdb;
        border-radius: 4px;
    }
    
    /* Scene Box Style */
    .scene-box {
        border: 1px solid #dbdbdb;
        padding: 15px;
        border-radius: 8px;
        background: white;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# 📂 Asset Loader
# ============================================================

def get_bgm_files():
    """
    assets/bgm/Genre/Track.mp3 をスキャンして辞書化
    Returns: {"Pop": ["track1.mp3", ...], "Rock": [...]}
    """
    bgm_dict = {}
    bgm_root = Path("assets/bgm")
    if bgm_root.exists():
        for genre_dir in bgm_root.iterdir():
            if genre_dir.is_dir():
                tracks = [f.name for f in genre_dir.glob("*.mp3")]
                if tracks:
                    bgm_dict[genre_dir.name] = tracks
    return bgm_dict

bgm_data = get_bgm_files()

# ============================================================
# 🎨 Sidebar Settings (Config)
# ============================================================

with st.sidebar:
    st.image("assets/logo.png", width=100) # Show App Logo if exists
    
    # --- Smart BGM Auto-Setup (Hidden if ready) ---
    bgm_data = get_bgm_files()
    total_tracks = sum(len(tracks) for tracks in bgm_data.values())
    
    if total_tracks < 10:
        st.info(f"🎵 BGMのセットアップが必要です (現在 {total_tracks} 曲)")
        if st.button("BGMを自動セットアップ"):
            with st.spinner("ダウンロード中..."):
                download_bgm.download_bgm()
                st.rerun()

    st.divider()
    st.markdown("### ⚙️ 設定・構成")
    
    # 1. 解像度選択 (Resolution)
    st.markdown("**1. 出力サイズ**")
    res_options = {
        "Reel / Story (9:16)": (1080, 1920),
        "Post / Square (1:1)": (1080, 1080),
        "YouTube / TV (16:9)": (1920, 1080)
    }
    selected_res_name = st.radio("サイズを選択", list(res_options.keys()), index=0, label_visibility="collapsed")
    target_res = res_options[selected_res_name]
    st.caption(f"解像度: {target_res[0]}x{target_res[1]}")
    
    st.divider()
    
    # 2. ロゴ (Watermark)
    st.markdown("**2. 透かしロゴ**")
    logo_file = st.file_uploader("ロゴ画像 (PNG)", type=["png"])
    wm_opacity = st.slider("ロゴ透明度", 0.0, 1.0, 0.3, 0.1)
    
    logo_path = "assets/logo.png"
    if logo_file:
        with open("temp_logo.png", "wb") as f:
            f.write(logo_file.getbuffer())
        logo_path = "temp_logo.png"
        st.image(logo_path, caption="現在のロゴ", width=80)

# ============================================================
# 🎬 Main UI (2-Column Layout)
# ============================================================

col_editor, col_preview = st.columns([1.5, 1])


def get_base64_image(file_buffer):
    import base64
    return base64.b64encode(file_buffer.getvalue()).decode()

# --- Left: Editor ---
with col_editor:
    st.subheader("🛠️ 動画エディタ")
    
    # 1. Style & Audio
    with st.expander("🎨 スタイル & BGM設定", expanded=True):
        c1, c2 = st.columns(2)
        with c1:
            # Preset Selection
            categories = sorted(list(set([k.split("_")[0] for k in PRESETS.keys()])))
            # ... (omitted for brevity, assume content is same)
            CATEGORY_NAMES = {
                "Food": "🍽️ グルメ・飲食", "Beauty": "💇‍♀️ 美容・サロン", "Fitness": "💪 フィットネス",
                "RealEstate": "🏠 不動産", "Fashion": "👗 ファッション", "Corporate": "🏢 企業・ビジネス",
                "Tech": "💻 IT・テック", "Recruit": "🤝 採用・人事", "Kids": "👶 キッズ・教育",
                "Wedding": "💍 ブライダル", "Sale": "📢 セール", "Night": "🍸 バー・ナイト"
            }
            def get_cat_name(key): return CATEGORY_NAMES.get(key, key)
            selected_cat = st.selectbox("カテゴリ", categories, format_func=get_cat_name)
            
            cat_presets = {k: v for k, v in PRESETS.items() if k.startswith(selected_cat)}
            selected_preset_key = st.selectbox("演出スタイル", list(cat_presets.keys()), format_func=lambda x: PRESETS[x]["display_name"])
            preset_data = PRESETS[selected_preset_key].copy() # Copy to avoid mutating original presets
            
            # --- Color Customization Overrides ---
            st.markdown("🎨 **色カスタマイズ (オプション)**")
            cc1, cc2 = st.columns(2)
            with cc1:
                custom_text_color = st.color_picker("文字色", preset_data.get("text_color", "#FFFFFF"))
            with cc2:
                # Use current bg color as default, or #000000 if None
                default_bg = preset_data.get("text_bg_color") or "#000000"
                has_bg = st.checkbox("背景あり", value=preset_data.get("text_bg_color") is not None)
                if has_bg:
                    custom_bg_color = st.color_picker("背景色", default_bg)
                else:
                    custom_bg_color = None
            
            # Apply overrides
            preset_data["text_color"] = custom_text_color
            preset_data["text_bg_color"] = custom_bg_color
            
        with c2:
            # BGM
            default_genre = preset_data.get("bgm_genre", list(bgm_data.keys())[0] if bgm_data else None)
            if bgm_data:
                sel_genre = st.selectbox("BGMジャンル", list(bgm_data.keys()), index=list(bgm_data.keys()).index(default_genre) if default_genre in bgm_data else 0)
                sel_track = st.selectbox("曲名", bgm_data[sel_genre])
                bgm_path = str(Path("assets/bgm") / sel_genre / sel_track)
                st.audio(bgm_path, format='audio/mp3') # BGM Preview
            else:
                st.warning("BGMなし")
                bgm_path = None

    # 2. Scene Editor (Grid)
    st.markdown("##### 🎞️ シーン編集 (Scene 1 - 5)")
    st.caption("最大5枚まで組み合わせられます。プレビューはInstagram風のリング枠で表示されます。")
    
    scenes = []
    
    scenes = []
    
    # Use Row-based Grid Layout to ensure alignment (Scene 1|2, 3|4, 5)
    # Iterate 0, 2, 4
    for row_start_idx in range(0, 5, 2):
        cols = st.columns(2)
        
        for col_idx in range(2):
            scene_idx = row_start_idx + col_idx
            if scene_idx >= 5:
                break
            
            with cols[col_idx]:
                with st.container():
                    # Stylish Header
                    st.markdown(f"**📸 Scene {scene_idx+1}**")
                    
                    # Preview Placeholder
                    preview_container = st.empty()
                    
                    img = st.file_uploader(f"画像 {scene_idx+1}", type=["jpg", "png", "jpeg"], key=f"img_{scene_idx}", label_visibility="collapsed")
                    
                    if img:
                        # Gradient Border Preview
                        b64_img = get_base64_image(img)
                        # Simplified gradient Ring effect
                        html = f"""
                        <div style="
                            padding: 3px;
                            background: linear-gradient(45deg, #f09433, #e6683c, #dc2743, #cc2366, #bc1888);
                            border-radius: 12px;
                            display: inline-block;
                            width: 100%;
                        ">
                            <img src="data:image/png;base64,{b64_img}" style="
                                width: 100%;
                                border-radius: 9px;
                                display: block;
                            ">
                        </div>
                        """
                        preview_container.markdown(html, unsafe_allow_html=True)
                    
                    # Text Input full width below image
                    txt = st.text_input(f"テキスト {scene_idx+1}", placeholder="文字を入力...", key=f"txt_{scene_idx}", label_visibility="collapsed")
                    
                st.divider()
                
                if img:
                    scenes.append({"image": img, "text": txt, "index": scene_idx})
    
    # Sort scenes by index
    scenes.sort(key=lambda x: x["index"])
    scenes = [s for s in scenes if s["image"] is not None]

# --- Right: Preview & Action ---
with col_preview:
    st.subheader("📱 プレビュー")
    
    # Duration Control
    st.caption("⏱️ 動画の長さ調整")
    duration_mode = st.radio("", ["自動調整", "15秒固定"], horizontal=True, label_visibility="collapsed")
    
    if duration_mode == "自動調整":
        dur = st.slider("1枚の時間(秒)", 1.0, 5.0, preset_data["duration"])
    else:
        cnt = len(scenes) if scenes else 1
        dur = 15.0 / cnt
        st.info(f"1枚あたり: {dur:.1f}秒 (計15秒)")
    
    preset_data["duration"] = dur
    if bgm_path:
        preset_data["bgm_path"] = bgm_path
    
    st.write("") # Spacer
    
    # Generate Button
    if st.button("✨ 動画を生成する (Generate)", type="primary", use_container_width=True):
        if not scenes:
            st.error("左側で画像を1枚以上アップロードしてください")
        else:
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Temp save
            temp_img_paths = []
            image_texts = []
            temp_dir = tempfile.mkdtemp()
            
            for sc in scenes:
                p = os.path.join(temp_dir, sc["image"].name)
                with open(p, "wb") as f:
                    f.write(sc["image"].getbuffer())
                temp_img_paths.append(p)
                image_texts.append(sc["text"])
                
            status_text.text("生成中... ☕")
            
            try:
                output_file = "output/generated_reel.mp4"
                if not os.path.exists("output"): os.makedirs("output")
                
                final_path = video_utils.generate_reel(
                    images=temp_img_paths, texts=image_texts, preset=preset_data,
                    output_path=output_file, logo_path=logo_path, target_resolution=target_res
                )
                
                progress_bar.progress(100)
                status_text.success("完成しました！")
                st.video(final_path)
                
                with open(final_path, "rb") as f:
                    st.download_button("📥 ダウンロード", f, "reel.mp4", "video/mp4", use_container_width=True)
                    
            except Exception as e:
                st.error(f"エラー: {e}")
                import traceback
                st.code(traceback.format_exc())

st.write("---")
