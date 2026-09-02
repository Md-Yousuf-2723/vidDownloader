import customtkinter as ctk
import yt_dlp
from tkinter import filedialog
import threading

ctk.set_appearance_mode("Dark")

BG_DEEP      = "#0D131F"
CARD_BG      = "#172033"
BORDER_COL   = "#27354F"
INPUT_BG     = "#0A0F1A"
TEXT_MAIN    = "#F1F5F9"
TEXT_MUTED   = "#8B9BB4"
LANTERN_GOLD = "#F59E0B"
LANTERN_HOVER= "#D97706"
SUCCESS_COL  = "#34D399"
ERROR_COL    = "#F87171"

app = ctk.CTk()
app.title("vidDownloader")
app.geometry("540x480")
app.resizable(False, False)
app.configure(fg_color=BG_DEEP)

title_label = ctk.CTkLabel(
    app,
    text="vidDownloader",
    font=("Helvetica", 22, "bold"),
    text_color=LANTERN_GOLD
)
title_label.pack(pady=(26, 4))

subtitle_label = ctk.CTkLabel(
    app,
    text="Developed by Md. Yousuf",
    font=("Helvetica", 12),
    text_color=TEXT_MUTED
)
subtitle_label.pack(pady=(0, 16))

main_card = ctk.CTkFrame(
    app,
    fg_color=CARD_BG,
    corner_radius=18,
    border_width=1,
    border_color=BORDER_COL
)
main_card.pack(pady=5, padx=35, fill="both", expand=True)

url_entry = ctk.CTkEntry(
    main_card,
    placeholder_text="Paste your video link here...",
    placeholder_text_color=TEXT_MUTED,
    fg_color=INPUT_BG,
    text_color=TEXT_MAIN,
    border_width=1,
    border_color=BORDER_COL,
    corner_radius=10,
    height=44,
    font=("Helvetica", 13)
)
url_entry.pack(pady=(22, 12), padx=20, fill="x")

path_frame = ctk.CTkFrame(main_card, fg_color="transparent")
path_frame.pack(pady=(0, 18), padx=20, fill="x")

path_entry = ctk.CTkEntry(
    path_frame,
    placeholder_text="Select save folder...",
    placeholder_text_color=TEXT_MUTED,
    fg_color=INPUT_BG,
    text_color=TEXT_MAIN,
    border_width=1,
    border_color=BORDER_COL,
    corner_radius=10,
    height=44,
    font=("Helvetica", 13)
)
path_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

selected_path = ""

def browse_folder():
    global selected_path
    chosen_dir = filedialog.askdirectory()
    if chosen_dir:
        selected_path = chosen_dir
        path_entry.configure(state="normal")
        path_entry.delete(0, "end")
        path_entry.insert(0, selected_path)
        path_entry.configure(state="readonly")

browse_btn = ctk.CTkButton(
    path_frame,
    text="Browse",
    font=("Helvetica", 12, "bold"),
    fg_color="#1E293B",
    hover_color="#334155",
    text_color=LANTERN_GOLD,
    border_width=1,
    border_color=BORDER_COL,
    corner_radius=10,
    height=44,
    width=90,
    command=browse_folder
)
browse_btn.pack(side="right")

status_label = ctk.CTkLabel(
    app,
    text="Ready",
    font=("Helvetica", 12),
    text_color=TEXT_MUTED
)
status_label.pack(pady=(12, 4))

progress_bar = ctk.CTkProgressBar(
    app,
    width=440,
    height=6,
    corner_radius=3,
    fg_color="#121824",
    progress_color=LANTERN_GOLD
)
progress_bar.set(0)
progress_bar.pack(pady=(0, 14))

def download_hook(d):
    if d['status'] == 'downloading':
        try:
            downloaded = d.get('downloaded_bytes', 0)
            total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
            percentage = (downloaded / total) if total > 0 else 0
            
            speed = d.get('speed', 0)
            speed_mb = (speed / (1024 * 1024)) if speed else 0
            
            progress_bar.set(percentage)
            status_label.configure(
                text=f"Downloading {percentage * 100:.1f}%  |  {speed_mb:.2f} MB/s",
                text_color=TEXT_MAIN
            )
        except Exception:
            pass

def run_download():
    link = url_entry.get().strip()
    if not link or not selected_path:
        status_label.configure(text="Please provide a link and select a folder", text_color=ERROR_COL)
        download_btn.configure(state="normal")
        return

    try:
        status_label.configure(text="Connecting...", text_color=TEXT_MAIN)
        progress_bar.set(0)
        
        opt = {
            'paths': {'home': selected_path},
            'format': 'best[ext=mp4]/best',
            'outtmpl': '%(title)s.%(ext)s',
            'progress_hooks': [download_hook],
            'noplaylist': True,
            'geo_bypass': True,
            'extractor_args': {'youtube': {'player_client': ['android', 'web']}},
        }


        with yt_dlp.YoutubeDL(opt) as downloader:
            downloader.download([link])

        status_label.configure(text="Download Complete", text_color=SUCCESS_COL)
        progress_bar.set(1.0)
    except yt_dlp.utils.DownloadError:
        status_label.configure(text="Error: Video unavailable, private, or login required.", text_color=ERROR_COL)
        progress_bar.set(0)
    except Exception as e:
        safe_msg = str(e).split(':')[-1].strip()[:35]
        status_label.configure(text=f"Error: {safe_msg}", text_color=ERROR_COL)
        progress_bar.set(0)
    finally:
        download_btn.configure(state="normal")

def start_download():
    download_btn.configure(state="disabled")
    threading.Thread(target=run_download, daemon=True).start()

download_btn = ctk.CTkButton(
    app,
    text="Download Video",
    font=("Helvetica", 14, "bold"),
    fg_color=LANTERN_GOLD,
    hover_color=LANTERN_HOVER,
    text_color="#0D131F",
    corner_radius=12,
    height=46,
    width=440,
    command=start_download
)
download_btn.pack(pady=(0, 24))

app.mainloop()