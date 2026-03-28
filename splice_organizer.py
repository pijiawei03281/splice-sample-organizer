import os
import re
import shutil
from datetime import datetime

# --- 設定路徑 ---
SOURCE_DIR = 'C:/Users/water/Downloads/splice classification/splice'  # 你從 Splice 下載的原始路徑
EXPORT_DIR = 'C:/Users/water/Downloads/splice classification/organized_samples'
REPORT_FILE = 'classification_report.txt'

# ==========================================
# 2. 完整的詳細分類對照表
# ==========================================
SAMPLE_MAP = {
    "Drums": {
        "Kicks": ["kick", "bd"], "Snares": ["snare", "sd"], "Hats": ["hat", "hh", "hihat"],
        "Claps": ["clap", "clp"], "Toms": ["tom"], "Cymbals": ["cymbal", "ride", "crash"],
        "Breaks": ["break"], "Fills": ["fill"], "Acoustic": ["acoustic drum"], "808": ["808"]
    },
    "Vocals": {
        "Female Vocals": ["female"], "Male Vocals": ["male"], "Vocal FX": ["vocal fx", "vxfx"],
        "Spoken Word": ["spoken"], "Vocoder": ["vocoder"], "Vocal Phrases": ["phrase"],
        "Screams": ["scream"], "Vocal Shouts": ["shout"], "Whisper Vocals": ["whisper"], "Dialogue": ["dialogue"]
    },
    "Percussion": {
        "Shakers": ["shaker"], "Conga": ["conga"], "Grooves": ["perc loop", "groove"],
        "Tambourine": ["tamb"], "Bongos": ["bongo"], "Cowbells": ["cowbell"],
        "Woodblock": ["woodblock"], "Bells": ["bell"], "Djembe": ["djembe"], "Timbales": ["timbale"]
    },
    "Synth": {
        "Bass": ["synth bass", "s-bass"], "Leads": ["lead"], "Pads": ["pad"], "Arp": ["arp"],
        "Stabs": ["stab"], "Chords": ["chord"], "Plucks": ["pluck"], "Analog": ["analog"],
        "FX": ["synth fx"], "Synth Melody": ["melody"]
    },
    "Brass and Woodwinds": {
        "Saxophone": ["sax"], "Trumpet": ["trumpet"], "Trombone": ["trombone"], "Flute": ["flute"],
        "Ensemble": ["ensemble"], "Synth": ["synth brass"], "Riffs": ["riff"], "Stabs": ["stab"],
        "Pads": ["brass pad"], "Harmonica": ["harmonica"], "Keys": ["brass keys"]
    },
    "Piano": {
        "Electric Piano": ["epiano", "rhodes"], "Wurlitzer": ["wurlitzer"], "Organ": ["organ"],
        "Synth": ["synth piano"], "Clavinet": ["clav"], "Chords": ["piano chord"],
        "Keys Melody": ["keys melody"], "Stabs": ["piano stab"], "Classical": ["grand piano"]
    },
    "Guitar": {
        "Electric": ["elec gtr", "electric guitar"], "Acoustic": ["acoustic gtr"], "Clean": ["clean"],
        "Distorted": ["distorted", "dist gtr"], "Synth": ["guitar synth"], "Chords": ["gtr chord"],
        "Leads": ["gtr lead"], "Guitar Melody": ["gtr melody"], "Riffs": ["riff"], "Rhythm": ["rhythm"]
    },
    "Bass": {
        "Synth": ["synth bass"], "Sub": ["sub"], "Analog": ["analog bass"], "Acoustic": ["upright"],
        "Electric": ["electric bass"], "Acid": ["acid"], "Saw": ["saw"], "Distorted": ["distorted bass"],
        "Wobble": ["wobble"], "Pulse": ["pulse"]
    },
    "FX": {
        "Noise": ["noise"], "Risers": ["riser"], "Downers": ["downer"], "Sweeps": ["sweep"],
        "Impacts": ["impact", "hit"], "Atmospheres": ["atmos"], "Textures": ["texture"],
        "Reverse": ["reverse"], "Field Recordings": ["field"], "FX Vocals": ["vocal fx"]
    },
    "Strings": {
        "Violin": ["violin"], "Cello": ["cello"], "Viola": ["viola"], "Bass": ["string bass"],
        "Ensemble": ["ensemble"], "Orchestral": ["orchestra"], "Synth": ["synth string"],
        "Pads": ["string pad"], "Staccato": ["staccato"], "Strings Melody": ["string melody"]
    }
}

# ==========================================
# 3. 核心處理邏輯
# ==========================================

def get_category(filename):
    fname = filename.lower()
    # 這裡的邏輯是：只要檔名包含關鍵字，就回傳分類
    for main_cat, sub_cats in SAMPLE_MAP.items():
        for sub_cat, keywords in sub_cats.items():
            if any(kw in fname for kw in keywords):
                return main_cat, sub_cat
    return "Unclassified", "Other"

def run_organizer():
    # 統計用變數
    stats = {"Total": 0, "Success": 0, "Unclassified": 0}
    logs = []

    # 確保目標資料夾存在
    if not os.path.exists(EXPORT_DIR):
        os.makedirs(EXPORT_DIR)

    # 讀取檔案清單 (排除資料夾，只讀取音訊檔)
    try:
        files = [f for f in os.listdir(SOURCE_DIR) if f.lower().endswith(('.wav', '.aif', '.mp3', '.flac'))]
    except FileNotFoundError:
        print(f"錯誤：找不到路徑 {SOURCE_DIR}，請確認路徑是否正確。")
        return

    stats["Total"] = len(files)

    for filename in files:
        main_cat, sub_cat = get_category(filename)
        
        # 決定搬運的目的地
        target_path = os.path.join(EXPORT_DIR, main_cat, sub_cat)
        
        if not os.path.exists(target_path):
            os.makedirs(target_path)

        # 執行移動
        try:
            shutil.move(os.path.join(SOURCE_DIR, filename), os.path.join(target_path, filename))
            
            # 紀錄狀態
            if main_cat == "Unclassified":
                stats["Unclassified"] += 1
                logs.append(f"[?] 未分類: {filename}")
            else:
                stats["Success"] += 1
                logs.append(f"[✓] {main_cat}/{sub_cat}: {filename}")
        except Exception as e:
            logs.append(f"[!] 錯誤: {filename} (原因: {e})")

    # ==========================================
    # 4. 自動產生報告
    # ==========================================
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write(f"=== Splice 自動分類報告 ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')}) ===\n")
        f.write(f"來源目錄: {SOURCE_DIR}\n")
        f.write(f"目標目錄: {EXPORT_DIR}\n")
        f.write("-" * 60 + "\n")
        f.write(f"總處理檔案: {stats['Total']}\n")
        f.write(f"成功分類: {stats['Success']}\n")
        f.write(f"無法識別: {stats['Unclassified']}\n")
        f.write("-" * 60 + "\n\n")
        f.writelines([line + "\n" for line in logs])
        f.write("\n=== 報告結束 ===")

    print(f"\n✅ 整理完成！")
    print(f"📊 總數: {stats['Total']} | 成功: {stats['Success']} | 未分類: {stats['Unclassified']}")
    print(f"📝 詳細紀錄請查看: {os.path.abspath(REPORT_FILE)}")

if __name__ == "__main__":
    run_organizer()