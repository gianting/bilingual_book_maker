import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import subprocess
import os

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

tk.Button(root, text="開始翻譯", command=start_translation).grid(row=4, column=1, pady=10)

root.mainloop()