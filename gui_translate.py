import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import subprocess
import os
import json

SETTINGS_FILE = "gui_settings.json"

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_settings(settings):
    try:
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(settings, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Failed to save settings: {e}")

def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("EPUB and SRT Files", "*.epub *.srt")])
    entry_file.delete(0, tk.END)
    entry_file.insert(0, file_path)

def start_translation():
    file_path = entry_file.get()
    api_key = entry_key.get()
    language = entry_language.get()
    model = entry_model.get()

    if not file_path or not api_key or not language or not model:
        messagebox.showwarning("缺少欄位", "請填寫所有欄位！")
        return

    command = [
        "python3", "make_book.py",
        "--book_name", file_path,
        "--openai_key", api_key,
        "--language", language,
        "-m", model
    ]

    try:
        subprocess.run(command, check=True)
        settings = {
            "file_path": file_path,
            "api_key": api_key,
            "language": language,
            "model": model
        }
        save_settings(settings)
        messagebox.showinfo("完成", "翻譯完成！")
    except Exception as e:
        messagebox.showerror("錯誤", f"翻譯時出錯了：\n{e}")

# 建立 GUI 視窗
root = tk.Tk()
root.title("字幕/電子書 翻譯小工具")

tk.Label(root, text="選擇檔案：").grid(row=0, column=0, sticky="e")
entry_file = tk.Entry(root, width=50)
entry_file.grid(row=0, column=1)
tk.Button(root, text="選擇檔案", command=select_file).grid(row=0, column=2)

tk.Label(root, text="API金鑰：").grid(row=1, column=0, sticky="e")
entry_key = tk.Entry(root, width=50)
entry_key.grid(row=1, column=1, columnspan=2)

# 從環境變數載入 API 金鑰
default_api_key = os.environ.get("OPENAI_API_KEY", "")
if default_api_key:
    entry_key.insert(0, default_api_key)

tk.Label(root, text="目標語言（如zh-hant）：").grid(row=2, column=0, sticky="e")
entry_language = ttk.Combobox(root, width=47, values=["en", "zh-hans", "zh-hant", "ja", "ko", "fr", "de", "es"])
entry_language.grid(row=2, column=1, columnspan=2)
entry_language.set("zh-hant")

tk.Label(root, text="使用模型（如gpt4o）：").grid(row=3, column=0, sticky="e")
entry_model = ttk.Combobox(root, width=47, values=["gpt-3.5-turbo", "gpt-4", "gpt4o", "claude-3-5-sonnet-latest", "geminipro", "groq"])
entry_model.grid(row=3, column=1, columnspan=2)
entry_model.set("gpt4o")

settings = load_settings()
if settings:
    if "file_path" in settings:
        entry_file.insert(0, settings["file_path"])
    if "api_key" in settings and not default_api_key:
        entry_key.insert(0, settings["api_key"])
    if "language" in settings:
        entry_language.set(settings["language"])
    if "model" in settings:
        entry_model.set(settings["model"])


tk.Button(root, text="開始翻譯", command=start_translation).grid(row=4, column=1, pady=10)

# 關閉視窗時儲存部分設定
def on_closing():
    # 關閉前儲存：檔案路徑、語言、模型（不要儲存 API 金鑰）
    settings = {
        "file_path": entry_file.get(),
        "language": entry_language.get(),
        "model": entry_model.get()
    }
    save_settings(settings)
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()