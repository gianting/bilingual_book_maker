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
    progress_bar['value'] = 0
    progress_label.config(text="進度：0%")
    root.update_idletasks()
    file_path = entry_file.get()
    api_key = entry_key.get()
    language = entry_language.get()
    model = entry_model.get()

    if not file_path or not api_key or not language or not model:
        messagebox.showwarning("缺少欄位", "請填寫所有欄位！")
        progress_bar['value'] = 0
        progress_label.config(text="進度：0%")
        root.update_idletasks()
        return

    command = [
        "python3", "make_book.py",
        "--book_name", file_path,
        "--openai_key", api_key,
        "--language", language,
        "-m", model
    ]

    try:
        # 模擬進度條增長（僅為視覺效果，非實際進度）
        for pct in range(0, 81, 20):
            progress_bar['value'] = pct
            progress_label.config(text=f"進度：{pct}%")
            root.update_idletasks()
            root.after(100)
        subprocess.run(command, check=True)
        progress_bar['value'] = 100
        progress_label.config(text="進度：100%")
        root.update_idletasks()
        settings = {
            "file_path": file_path,
            "api_key": api_key,
            "language": language,
            "model": model
        }
        save_settings(settings)
        messagebox.showinfo("完成", "翻譯完成！")
    except Exception as e:
        progress_bar['value'] = 0
        progress_label.config(text="進度：0%")
        root.update_idletasks()
        messagebox.showerror("錯誤", f"翻譯時出錯了：\n{e}")

# 建立 GUI 視窗
root = tk.Tk()
topmost_var = tk.BooleanVar(value=True)
root.attributes("-topmost", True)
root.title("字幕/電子書 翻譯小工具")
root.geometry("650x350")
root.configure(bg="#f7f7f7")
default_font = ("Helvetica", 12)

main_frame = tk.Frame(root, bg="#f7f7f7", padx=15, pady=15)
main_frame.grid(row=0, column=0, sticky="nsew")

tk.Label(main_frame, text="選擇檔案：", font=default_font, bg="#f7f7f7").grid(row=0, column=0, sticky="e", pady=6)
entry_file = tk.Entry(main_frame, width=50, font=default_font)
entry_file.grid(row=0, column=1, pady=6, padx=(0,10))
tk.Button(main_frame, text="選擇檔案", command=select_file, font=default_font).grid(row=0, column=2, pady=6)

tk.Label(main_frame, text="API金鑰：", font=default_font, bg="#f7f7f7").grid(row=1, column=0, sticky="e", pady=6)
entry_key = tk.Entry(main_frame, width=50, font=default_font)
entry_key.grid(row=1, column=1, columnspan=2, pady=6, padx=(0,10))

# 從環境變數載入 API 金鑰
default_api_key = os.environ.get("OPENAI_API_KEY", "")
if default_api_key:
    entry_key.insert(0, default_api_key)

tk.Label(main_frame, text="目標語言（如zh-hant）：", font=default_font, bg="#f7f7f7").grid(row=2, column=0, sticky="e", pady=6)
entry_language = ttk.Combobox(main_frame, width=47, values=["en", "zh-hans", "zh-hant", "ja", "ko", "fr", "de", "es"], font=default_font)
entry_language.grid(row=2, column=1, columnspan=2, pady=6, padx=(0,10))
entry_language.set("zh-hant")

tk.Label(main_frame, text="使用模型（如gpt4o）：", font=default_font, bg="#f7f7f7").grid(row=3, column=0, sticky="e", pady=6)
entry_model = ttk.Combobox(main_frame, width=47, values=["gpt-3.5-turbo", "gpt-4", "gpt4o", "claude-3-5-sonnet-latest", "geminipro", "groq"], font=default_font)
entry_model.grid(row=3, column=1, columnspan=2, pady=6, padx=(0,10))
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
    topmost_var.set(settings.get("topmost", True))
    root.attributes("-topmost", topmost_var.get())

start_button = tk.Button(main_frame, text="開始翻譯", command=start_translation,
                         bg="#4CAF50", fg="black", activeforeground="black", activebackground="#45A049",
                         font=("Helvetica", 14, "bold"), height=2, relief="raised")
start_button.grid(row=4, column=1, pady=15, sticky="ew", columnspan=1)

progress_bar = ttk.Progressbar(main_frame, mode='determinate', maximum=100)
progress_bar.grid(row=5, column=0, columnspan=3, sticky="ew", pady=(5,2), padx=(0,10))

progress_label = tk.Label(main_frame, text="進度：0%", font=("Helvetica", 10), bg="#f7f7f7")
progress_label.grid(row=6, column=0, columnspan=3, pady=(0,10))

topmost_checkbox = tk.Checkbutton(main_frame, text="視窗置頂", variable=topmost_var, bg="#f7f7f7", font=default_font, command=lambda: root.attributes("-topmost", topmost_var.get()))
topmost_checkbox.grid(row=7, column=0, columnspan=3, pady=(5, 10))

# 關閉視窗時儲存部分設定
def on_closing():
    # 關閉前儲存：檔案路徑、語言、模型（不要儲存 API 金鑰）
    settings = {
        "file_path": entry_file.get(),
        "language": entry_language.get(),
        "model": entry_model.get(),
        "topmost": topmost_var.get()
    }
    save_settings(settings)
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()