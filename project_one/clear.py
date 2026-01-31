import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

"""
اسم البرنامج: منظم الملفات الذكي (Smart File Organizer)
المطور: أنس محمد (Anas Mohammed)
الوصف: يقوم البرنامج بتنظيم المجلدات وتصنيف الملفات تلقائياً
الحقوق: جميع الحقوق محفوظة © 2024
"""

class FileOrganizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart File Organizer | Anas Mohammed")
        self.root.geometry("400x250")
        self.root.resizable(False, False)
        
        # تنسيق الألوان
        self.bg_color = "#f0f0f0"
        self.root.configure(bg=self.bg_color)
        
        # واجهة المستخدم
        self.create_widgets()

    def create_widgets(self):
        # عنوان ترحيبي
        label = tk.Label(self.root, text="منظم الملفات الذكي", font=("Arial", 16, "bold"), bg=self.bg_color)
        label.pack(pady=20)

        # زر اختيار المجلد
        self.organize_btn = ttk.Button(self.root, text="اختر المجلد لتنظيمه", command=self.start_organizing)
        self.organize_btn.pack(pady=10)

        # اسم المطور في الأسفل
        footer = tk.Label(self.root, text="Developed by: Anas Mohammed", font=("Arial", 8), bg=self.bg_color)
        footer.pack(side="bottom", pady=10)

    def start_organizing(self):
        directory = filedialog.askdirectory()
        if not directory:
            return

        try:
            self.organize_files(directory)
            messagebox.showinfo("تم بنجاح", "تم تنظيم الملفات بنجاح يا أنس!")
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ أثناء التنظيم: {str(e)}")

    def organize_files(self, folder_path):
        # تعريف الامتدادات لكل نوع
        file_types = {
            'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp'],
            'Documents': ['.pdf', '.docx', '.txt', '.xlsx', '.pptx'],
            'Videos': ['.mp4', '.mkv', '.avi', '.mov'],
            'Audio': ['.mp3', '.wav', '.flac'],
            'Archives': ['.zip', '.rar', '.7z', '.tar']
        }

        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            
            if os.path.isdir(file_path):
                continue
                
            extension = os.path.splitext(filename)[1].lower()
            
            for folder, extensions in file_types.items():
                if extension in extensions:
                    dest_folder = os.path.join(folder_path, folder)
                    os.makedirs(dest_folder, exist_ok=True)
                    shutil.move(file_path, os.path.join(dest_folder, filename))
                    break

if __name__ == "__main__":
    root = tk.Tk()
    app = FileOrganizerApp(root)
    root.mainloop()