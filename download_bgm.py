
import os
import requests
from pathlib import Path
import time

# ============================================================
# 🎵 BGM Curation (GitHub Optimized - Direct Raw URLs)
# ============================================================

# These URLs use GitHub's raw content delivery which avoids 403 hotlinking issues.
# Sources: yuuniji/music (Lo-fi), noobsandnerdsgroup/audio (Pop/Corporate)
# All tracks are Creative Commons / Royalty-Free.

BGM_SOURCES = {
    "Chill": {
        "this_is_easy.mp3": "https://raw.githubusercontent.com/yuuniji/music/main/lofi_beats/1-this_is_easy_by_red_tractor.mp3",
        "asleep.mp3": "https://raw.githubusercontent.com/yuuniji/music/main/lofi_beats/2-asleep_by_les_marais.mp3",
        "winterblossom.mp3": "https://raw.githubusercontent.com/yuuniji/music/main/lofi_beats/3-winterblossom_by_lilibu.mp3",
        "coastal_road.mp3": "https://raw.githubusercontent.com/yuuniji/music/main/lofi_beats/14-coastal_road_by_mellow_fox.mp3",
        "cravings.mp3": "https://raw.githubusercontent.com/yuuniji/music/main/lofi_beats/15-Cravings_by_aunt.mp3"
    },
    "Pop": {
        "AcidJazz.mp3": "https://raw.githubusercontent.com/noobsandnerdsgroup/audio/main/AcidJazz.mp3",
        "ArrozConPollo.mp3": "https://raw.githubusercontent.com/noobsandnerdsgroup/audio/main/Arroz%20Con%20Pollo.mp3",
        "AlmostBliss.mp3": "https://raw.githubusercontent.com/noobsandnerdsgroup/audio/main/Almost%20Bliss.mp3",
        "BackOnTrack.mp3": "https://raw.githubusercontent.com/noobsandnerdsgroup/audio/main/Back%20on%20Track.mp3",
        "BeautyFlow.mp3": "https://raw.githubusercontent.com/noobsandnerdsgroup/audio/main/Beauty%20Flow.mp3"
    },
    "Corporate": {
        "AmazingPlan.mp3": "https://raw.githubusercontent.com/noobsandnerdsgroup/audio/main/Amazing%20Plan.mp3",
        "AlmostNew.mp3": "https://raw.githubusercontent.com/noobsandnerdsgroup/audio/main/Almost%20New.mp3",
        "AirportLounge.mp3": "https://raw.githubusercontent.com/noobsandnerdsgroup/audio/main/Airport%20Lounge.mp3",
        "BlippyTrance.mp3": "https://raw.githubusercontent.com/noobsandnerdsgroup/audio/main/Blippy%20Trance.mp3",
        "BleepingDemo.mp3": "https://raw.githubusercontent.com/noobsandnerdsgroup/audio/main/Bleeping%20Demo.mp3"
    }
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def download_bgm(force=False):
    base_path = Path("assets/bgm")
    
    print("🚀 Starting reliable BGM download from GitHub...")

    for genre, tracks in BGM_SOURCES.items():
        genre_path = base_path / genre
        genre_path.mkdir(parents=True, exist_ok=True)
        
        for filename, url in tracks.items():
            save_path = genre_path / filename
            
            if save_path.exists() and not force:
                print(f"✅ Already exists: {genre}/{filename}")
                continue
            
            print(f"⬇ Downloading [{genre}] {filename}...")
            try:
                response = requests.get(url, headers=HEADERS, stream=True, timeout=30)
                response.raise_for_status()
                
                with open(save_path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                print(f"✨ Downloaded: {filename}")
                # Small delay to prevent rate limits
                time.sleep(0.5)
            except Exception as e:
                print(f"❌ Failed to download {filename}: {e}")

if __name__ == "__main__":
    download_bgm()
