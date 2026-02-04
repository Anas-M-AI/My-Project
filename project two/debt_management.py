import os
import sys

# Set console encoding to UTF-8 for Arabic support on Windows
if sys.platform == 'win32':
    os.system('chcp 65001 > nul')

print("بدء تشغيل البرنامج...")

# Debt Management System
# Copyright (c) 2026 Anas Mohammed. All rights reserved.
# This software is protected and may not be copied or distributed without permission.

import tkinter as tk
from tkinter import messagebox, simpledialog
import json

print("بدء تشغيل النظام...")

# Activation code (hardcoded for demo, change to your desired code)
ACTIVATION_CODE = "my sweet"
ACTIVATION_FILE = ".activated"

def check_activation():
    """
    Check if the program has been activated by looking for the activation file.
    Returns True if activated, False otherwise.
    """
    print("فحص التفعيل...")
    if os.path.exists(ACTIVATION_FILE):
        print("ملف التفعيل موجود.")
        return True
    print("ملف التفعيل غير موجود.")
    return False

def activate_program():
    """
    Prompt the user for activation code and activate if correct.
    Returns True if activated, False otherwise.
    """
    print("طلب رمز التفعيل...")
    code = simpledialog.askstring("تفعيل", "أدخل رمز التفعيل:")
    if code == ACTIVATION_CODE:
        with open(ACTIVATION_FILE, 'w') as f:
            f.write("activated")
        messagebox.showinfo("نجح", "تم تفعيل البرنامج بنجاح!")
        print("تم التفعيل بنجاح.")
        return True
    else:
        messagebox.showerror("خطأ", "رمز التفعيل غير صحيح!")
        print("رمز التفعيل خاطئ.")
        return False

class DebtManager:
    """
    Main class for the Debt Management GUI application.
    """
    def __init__(self, root):
        """
        Initialize the DebtManager with the root window.
        """
        self.root = root
        self.root.title("نظام إدارة الديون")
        # Set window icon if icon.ico exists
        try:
            self.root.iconbitmap('icon.ico')
        except:
            pass  # Icon not found, continue without it
        self.debts = self.load_debts()
        self.create_widgets()

    def load_debts(self):
        """
        Load debts from the JSON file.
        Returns a list of debts.
        """
        if os.path.exists("debts.json"):
            with open("debts.json", "r") as f:
                return json.load(f)
        return []

    def save_debts(self):
        """
        Save the current debts to the JSON file.
        """
        with open("debts.json", "w") as f:
            json.dump(self.debts, f)

    def create_widgets(self):
        self.listbox = tk.Listbox(self.root, width=50, height=10)
        self.listbox.pack(pady=10)
        self.update_listbox()

        tk.Button(self.root, text="إضافة دين", command=self.add_debt).pack(side=tk.LEFT, padx=5)
        tk.Button(self.root, text="دفع دين", command=self.pay_debt).pack(side=tk.LEFT, padx=5)
        tk.Button(self.root, text="حذف دين", command=self.delete_debt).pack(side=tk.LEFT, padx=5)
        tk.Button(self.root, text="خروج", command=self.root.quit).pack(side=tk.RIGHT, padx=5)

    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for debt in self.debts:
            self.listbox.insert(tk.END, f"{debt['name']}: {debt['amount']} دينار عراقي - استحقاق: {debt['due_date']}")

    def add_debt(self):
        name = simpledialog.askstring("إضافة دين", "اسم المدين:")
        if not name:
            return
        amount = simpledialog.askfloat("إضافة دين", "المبلغ بالدينار العراقي:")
        if amount is None:
            return
        due_date = simpledialog.askstring("إضافة دين", "تاريخ الاستحقاق (YYYY-MM-DD):")
        if not due_date:
            return
        self.debts.append({"name": name, "amount": amount, "due_date": due_date})
        self.save_debts()
        self.update_listbox()

    def pay_debt(self):
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showwarning("تحذير", "اختر ديناً للدفع!")
            return
        index = selected[0]
        pay_amount = simpledialog.askfloat("دفع دين", f"مبلغ الدفع بالدينار العراقي لـ {self.debts[index]['name']}:")
        if pay_amount is None or pay_amount <= 0:
            return
        if pay_amount >= self.debts[index]['amount']:
            del self.debts[index]
        else:
            self.debts[index]['amount'] -= pay_amount
        self.save_debts()
        self.update_listbox()

    def delete_debt(self):
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showwarning("تحذير", "اختر ديناً لحذفه!")
            return
        index = selected[0]
        del self.debts[index]
        self.save_debts()
        self.update_listbox()

if __name__ == "__main__":
    print("جاري تشغيل النظام...")
    if not check_activation():
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        # Set icon for activation dialog
        try:
            root.iconbitmap('icon.ico')
        except:
            pass
        if not activate_program():
            exit()
        root.destroy()

    root = tk.Tk()
    app = DebtManager(root)
    root.mainloop()