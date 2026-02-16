# ============================================================
# 🎨 Visual Style Presets (15 Types)
# ============================================================

PRESETS = {
    # --- Category: Food ---
    "Food_Luxury": {
        "display_name": "Food Luxury (高級感)",
        "font_file": "Mincho", # ユーザーがassets/fontsに置くファイル名の一部
        "text_color": "#FFFFFF",
        "text_bg_color": None, # 文字背景なし
        "animation": "zoom_in_crossfade",
        "duration": 3.0,
        "bgm_genre": "Chill"
    },
    "Food_Casual": {
        "display_name": "Food Casual (親しみ)",
        "font_file": "Round",
        "text_color": "#333333",
        "text_bg_color": "#FFCC00", # 黄色背景
        "animation": "slide_in_left",
        "duration": 2.5,
        "bgm_genre": "Pop"
    },
    "Food_Sizzle": {
        "display_name": "Food Sizzle (シズル感)",
        "font_file": "ExtraBold",
        "text_color": "#FF0000",
        "text_bg_color": "#FFFFFF",
        "animation": "zoom_center_impact",
        "duration": 1.5, # 早めのカット
        "bgm_genre": "Rock"
    },
    "Food_Izakaya": {
        "display_name": "Food Izakaya (居酒屋)",
        "font_file": "Brush",
        "text_color": "#FFFFFF",
        "text_bg_color": "#000000",
        "animation": "slide_in_vertical",
        "duration": 2.0,
        "bgm_genre": "Pop"
    },

    # --- Category: Beauty ---
    "Beauty_Salon": {
        "display_name": "Beauty Salon (サロン)",
        "font_file": "Thin",
        "text_color": "#555555",
        "text_bg_color": "#F0F0F0", # 薄いグレー
        "animation": "soft_pan",
        "duration": 4.0, # ゆったり
        "bgm_genre": "Chill"
    },
    "Fitness_Gym": {
        "display_name": "Fitness Gym (ジム)",
        "font_file": "Italic",
        "text_color": "#FFFF00", # 蛍光イエロー
        "text_bg_color": "#000000",
        "animation": "fast_cut_shake",
        "duration": 1.0, # かなり早い
        "bgm_genre": "Rock"
    },
    "RealEstate": {
        "display_name": "Real Estate (不動産)",
        "font_file": "Gothic",
        "text_color": "#FFFFFF",
        "text_bg_color": "#003366", # 紺色
        "animation": "pan_horizontal",
        "duration": 3.5,
        "bgm_genre": "Corporate"
    },
    "Fashion": {
        "display_name": "Fashion (アパレル)",
        "font_file": "Serif",
        "text_color": "#000000",
        "text_bg_color": "#FFFFFF",
        "animation": "flash_cut",
        "duration": 0.8, # フラッシュカット
        "bgm_genre": "Pop"
    },

    # --- Category: Business ---
    "Corporate": {
        "display_name": "Corporate (企業紹介)",
        "font_file": "Standard",
        "text_color": "#FFFFFF",
        "text_bg_color": "#000000",
        "animation": "static_fade",
        "duration": 3.0,
        "bgm_genre": "Corporate"
    },
    "Tech_Startup": {
        "display_name": "Tech Startup (IT)",
        "font_file": "Digital",
        "text_color": "#00FFFF", # サイバーブルー
        "text_bg_color": "rgba(0,0,0,0.5)",
        "animation": "slide_fast_tint",
        "duration": 2.0,
        "bgm_genre": "Electronic"
    },
    "Recruit": {
        "display_name": "Recruit (採用)",
        "font_file": "BoldGothic",
        "text_color": "#FFFFFF",
        "text_bg_color": "#FF6600",
        "animation": "zoom_face_text",
        "duration": 3.0,
        "bgm_genre": "Corporate"
    },

    # --- Category: Other ---
    "Kids_Edu": {
        "display_name": "Kids Education (子供)",
        "font_file": "Round",
        "text_color": "#FFFFFF",
        "text_bg_color": "#FF99CC", # ピンク
        "animation": "bounce_zoom",
        "duration": 2.5,
        "bgm_genre": "Pop"
    },
    "Wedding": {
        "display_name": "Wedding (ブライダル)",
        "font_file": "Mincho",
        "text_color": "#FFFFFF",
        "shadow_color": "#000000",
        "text_bg_color": None,
        "animation": "slow_dissolve",
        "duration": 4.0,
        "bgm_genre": "Wed"
    },
    "Sale_Campaign": {
        "display_name": "Sale Campaign (セール)",
        "font_file": "ExtraBold",
        "text_color": "#FFFFFF",
        "text_bg_color": "#FF0000",
        "animation": "pulse_zoom",
        "duration": 1.5,
        "bgm_genre": "Upbeat"
    },
    "Night_Bar": {
        "display_name": "Night Bar (バー)",
        "font_file": "ThinGothic",
        "text_color": "#FFFFFF",
        "text_bg_color": None,
        "video_effect": "high_contrast",
        "animation": "fade_dark",
        "duration": 3.0,
        "bgm_genre": "Jazz"
    },
}

# デフォルト設定
DEFAULT_DURATION = 3.0
VIDEO_SIZE = (1080, 1920) # 9:16 Full HD
WATERMARK_PATH = "assets/logo.png"
WATERMARK_OPACITY = 0.3
