
import os
import random
import numpy as np
from PIL import Image, ImageFilter, ImageDraw, ImageFont, ImageOps
from moviepy.editor import (
    ImageClip, CompositeVideoClip, ColorClip, VideoClip, AudioFileClip,
    vfx, transfx, concatenate_videoclips
)
from moviepy.video.fx.all import crop, resize
from pilmoji import Pilmoji
# Try import audio_loop
try:
    from moviepy.audio.fx.all import audio_loop
except ImportError:
    # Fallback for older moviepy
    audio_loop = None

DEFAULT_FONT = "arial.ttf" # Windows standard
ASSETS_DIR = "assets"

# Monkey-patch: Fix MoviePy compatibility with Pillow 10+
if not hasattr(Image, 'ANTIALIAS'):
    Image.ANTIALIAS = Image.LANCZOS

# ============================================================
# 📐 Aspect Ratio & Layout
# ============================================================

def resize_with_blur(clip, target_size=(1080, 1920)):
    """
    画像が9:16でない場合、背景にブラー画像を配置して余白を埋める
    """
    w, h = clip.size
    target_w, target_h = target_size
    
    # アスペクト比計算
    img_ratio = w / h
    target_ratio = target_w / target_h
    
    # ほぼ一致ならリサイズしてクロップ
    if abs(img_ratio - target_ratio) < 0.05:
        if img_ratio > target_ratio:
            return clip.resize(height=target_h).crop(x1=(clip.w*target_h/clip.h - target_w)/2, width=target_w, height=target_h)
        else:
            return clip.resize(width=target_w).crop(y1=(clip.h*target_w/clip.w - target_h)/2, width=target_w, height=target_h)

    # 縦長すぎる or 横長すぎる場合
    if img_ratio > target_ratio:
        # 横長: 幅を合わせて上下に黒帯(ブラー)
        main = clip.resize(width=target_w)
    else:
        # 縦長: 高さを合わせて左右に黒帯(ブラー)
        main = clip.resize(height=target_h)
        
    # 背景: 画面いっぱいに拡大してブラー (簡易的に暗くする)
    bg = clip.resize(height=target_h if img_ratio > target_ratio else target_w * 2)
    bg = bg.crop(x_center=bg.w/2, y_center=bg.h/2, width=target_w, height=target_h)
    bg = bg.fx(vfx.colorx, 0.4) # 暗くする
    
    return CompositeVideoClip([bg.set_position("center"), main.set_position("center")], size=target_size)

# ============================================================
# 🎬 Animations
# ============================================================

def apply_animation(clip, animation_type, duration):
    """
    config.py で定義されたアニメーションタイプに応じてエフェクトを適用
    """
    clip = clip.set_duration(duration)
    w, h = clip.size
    
    if animation_type == "zoom_in_crossfade":
        return clip.resize(lambda t: 1 + 0.05 * t)
        
    elif animation_type == "zoom_center_impact":
        return clip.resize(lambda t: 1 + 0.3 * t)
        
    elif animation_type == "slide_in_left":
        return clip.set_position(lambda t: (min(0, int(w * (t/0.5 - 1))), "center") if t < 0.5 else "center")
        
    elif animation_type == "slide_in_vertical":
        return clip.set_position(lambda t: ("center", min(0, int(h * (t/0.5 - 1)))) if t < 0.5 else "center")
    
    elif animation_type == "pan_horizontal":
        clip = clip.resize(1.2)
        return clip.set_position(lambda t: (int(-0.1*w + 0.05*w*t), "center"))
        
    elif animation_type == "soft_pan":
        clip = clip.resize(1.1)
        return clip.set_position(lambda t: ("center", int(-0.05*h + 0.02*h*t)))
        
    elif animation_type == "flash_cut":
        return clip.fx(vfx.fadein, 0.1)
        
    elif animation_type == "pulse_zoom":
        return clip.resize(lambda t: 1 + 0.05 * abs(np.sin(t * 3)))
        
    elif animation_type == "bounce_zoom":
        return clip.resize(lambda t: 1 + 0.1 * abs(np.sin(t * 5)))

    # Default
    return clip

# ============================================================
# 💧 Watermark
# ============================================================

def add_watermark(video_clip, logo_path="assets/logo.png", opacity=0.3):
    if not os.path.exists(logo_path):
        return video_clip
        
    logo = ImageClip(logo_path).resize(width=video_clip.w * 0.15) 
    logo = logo.set_opacity(opacity)
    # 右下 (マージン20px)
    logo = logo.set_position(("right", "bottom")).set_duration(video_clip.duration).margin(right=20, bottom=20, opacity=0)
    
    return CompositeVideoClip([video_clip, logo], size=video_clip.size)

# ============================================================
# 📝 Text Overlay (via PIL & Pilmoji)
# ============================================================

def wrap_text(text, font, max_width):
    """
    指定された幅に収まるようにテキストを改行する
    """
    lines = []
    # ユーザーが入力した改行を尊重
    for paragraph in text.split('\n'):
        words = list(paragraph) # 日本語の場合は文字単位で分割
        if not words:
            lines.append("")
            continue
            
        current_line = ""
        for word in words:
            test_line = current_line + word
            # textbboxで幅を確認
            bbox = font.getbbox(test_line)
            if bbox[2] - bbox[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        lines.append(current_line)
    return lines

def create_text_image(text, font_path, fontsize=60, color='white', bg_color=None, size=(1080, 400)):
    """
    PILを使ってテキスト画像を生成し、ImageClipとして返す (改行・見切れ防止対応)
    """
    if not text:
        return None
        
    line_spacing = 10
    area_w, area_h = size
    max_text_w = area_w * 0.9 # 左右に5%ずつのマージン
    
    # 1. 最適なフォントサイズを決定 (領域に収まるまで小さくする)
    current_fontsize = fontsize
    while current_fontsize > 20:
        try:
            font = ImageFont.truetype(font_path, current_fontsize)
        except OSError:
            font = ImageFont.load_default()
        
        # テキストをラッピング
        lines = wrap_text(text, font, max_text_w)
        
        # 全体の高さを計算
        total_h = 0
        max_measured_w = 0
        for line in lines:
            bbox = font.getbbox(line or " ")
            total_h += (bbox[3] - bbox[1]) + line_spacing
            max_measured_w = max(max_measured_w, bbox[2] - bbox[0])
            
        if total_h <= area_h:
            break
        current_fontsize -= 5 # 収まらなければサイズを下げる

    # 2. 描画
    img = Image.new('RGBA', size, (0, 0, 0, 0))
    
    # 中央配置のための開始位置
    current_y = (area_h - total_h) / 2
    
    stroke_color = 'black'
    if color.lower() in ['black', '#000000', '#000'] or (color.startswith('#') and color.lower() < '#444'):
        stroke_color = 'white'

    with Pilmoji(img) as pilmoji:
        for line in lines:
            if not line:
                current_y += current_fontsize + line_spacing
                continue
                
            bbox = font.getbbox(line)
            line_w = bbox[2] - bbox[0]
            line_h = bbox[3] - bbox[1]
            current_x = (area_w - line_w) / 2
            
            # 背景矩形 (行単位)
            if bg_color:
                padding = 10
                # Pilmojiの背後にあるImageDrawを直接使うことはできないので、
                # 事前にimgに対して背景を描画するか、pilmojiオブジェクト経由で描画が必要な場合がある。
                # 幸いpilmoji.imageは元のimg。
                draw = ImageDraw.Draw(img)
                draw.rectangle(
                    [current_x - padding, current_y, current_x + line_w + padding, current_y + line_h + padding],
                    fill=bg_color
                )
                
            # 文字描画 (Pilmojiなら絵文字が自動的に置換される)
            pilmoji.text((current_x, current_y), line, font=font, fill=color, stroke_width=4, stroke_fill=stroke_color)
                
            current_y += line_h + line_spacing
    
    return np.array(img)

def create_text_clip_pil(text, font_path, fontsize=70, color='white', bg_color=None, duration=3, canvas_size=(1080, 1920)):
    """
    テキストクリップ生成 (解像度対応)
    """
    # 解像度に合わせてフォントサイズとエリアを調整
    scale = canvas_size[0] / 1080.0
    scaled_fontsize = int(fontsize * scale)
    
    # テキストエリア: 幅は画面いっぱい、高さは30%
    area_w = canvas_size[0]
    area_h = int(canvas_size[1] * 0.3)
    
    img_array = create_text_image(text, font_path, scaled_fontsize, color, bg_color, size=(area_w, area_h))
    if img_array is None:
        return None
        
    txt_clip = ImageClip(img_array).set_duration(duration)
    
    # 位置: 画面下部 (margin調整)
    bottom_margin = int(canvas_size[1] * 0.15)
    txt_clip = txt_clip.set_position(("center", "bottom")).margin(bottom=bottom_margin, opacity=0)
    
    return txt_clip

# ============================================================
# 🚀 Generator Main
# ============================================================

def generate_reel(images, texts, preset, output_path="output/reel.mp4", logo_path="assets/logo.png", target_resolution=(1080, 1920)):
    """
    メイン生成ロジック
    """
    clips = []
    
    for i, img_path in enumerate(images):
        txt = texts[i] if i < len(texts) else ""
        
        # 1. 画像読み込み & EXIF回転
        pil_img = Image.open(img_path)
        pil_img = ImageOps.exif_transpose(pil_img)
        img_clip = ImageClip(np.array(pil_img))
        
        # 2. アスペクト比調整
        base_clip = resize_with_blur(img_clip, target_size=target_resolution)
        
        # 3. アニメーション
        anim_clip = apply_animation(base_clip, preset["animation"], preset["duration"])
        
        # 4. テキスト合成
        font_file = preset.get("font_file", "Arial")
        font_path = DEFAULT_FONT
        
        # Font finding logic
        for ext in [".ttf", ".otf", ".ttc"]:
            candidate = os.path.join(ASSETS_DIR, "fonts", f"{font_file}{ext}")
            if os.path.exists(candidate):
                font_path = candidate
                break
        
        if font_path == DEFAULT_FONT:
             fallback_candidate = os.path.join(ASSETS_DIR, "fonts", "BoldGothic.otf")
             if os.path.exists(fallback_candidate):
                 font_path = fallback_candidate

        final_clip = anim_clip
        if txt:
             t_clip = create_text_clip_pil(txt, font_path, color=preset["text_color"], duration=preset["duration"], canvas_size=target_resolution)
             if t_clip:
                 final_clip = CompositeVideoClip([anim_clip, t_clip], size=target_resolution).set_duration(preset["duration"])
        
        clips.append(final_clip)
        
    # 連結
    final_video = concatenate_videoclips(clips, method="compose")
    
    
    # BGM追加
    if "bgm_path" in preset and preset["bgm_path"] and os.path.exists(preset["bgm_path"]):
        try:
            audio = AudioFileClip(preset["bgm_path"])
            # Loop check
            if audio.duration < final_video.duration:
                # Loop audio to match video duration
                if audio_loop:
                    audio = audio_loop(audio, duration=final_video.duration)
                else:
                    # Manual loop fallback
                    count = int(final_video.duration / audio.duration) + 1
                    # Note: Concatenating AudioFileClips can be tricky, so we load subclip?
                    # Simply making a new CompositeAudioClip with loops is safer if concatenate is hard
                    # But concatenate_audioclips exists in moviepy.editor
                    from moviepy.editor import concatenate_audioclips
                    audio = concatenate_audioclips([audio] * count)
                    audio = audio.subclip(0, final_video.duration)
            else:
                audio = audio.subclip(0, final_video.duration)
                
            # Audio Fadeout (3sec)
            # Try to use audio_fadeout from moviepy.audio.fx.all
            try:
                from moviepy.audio.fx.all import audio_fadeout
                audio = audio.fx(audio_fadeout, 3)
            except ImportError:
                 # Fallback: manually fadeout if possible, or skip
                 # audio.audio_fadeout exists in some versions?
                 if hasattr(audio, 'audio_fadeout'):
                     audio = audio.audio_fadeout(3)
            except Exception as e:
                print(f"Audio Fadeout failed: {e}")
                pass

            final_video = final_video.set_audio(audio)
        except Exception as e:
            print(f"BGM Error: {e}")
            pass
            
    # Video Fadeout (End 3 sec)
    try:
        final_video = final_video.fx(vfx.fadeout, 3)
    except:
        pass # vfx.fadeout might need color argument? vfx.fadeout(clip, duration)
    
    # 5. 透かし
    final_video = add_watermark(final_video, logo_path=logo_path, opacity=0.3)
    
    # 書き出し
    final_video.write_videofile(output_path, fps=30, codec="libx264", audio_codec="aac")
    return output_path
