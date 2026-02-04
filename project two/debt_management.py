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
ACTIVATION_FILE = os.path.join(os.environ.get('APPDATA', ''), '.activated')
LICENSE_FILE = "license.txt"
LICENSE_CONTENT = "Licensed to Anas Mohammed - Valid License"

def check_activation():
    """
    Check if the program has been activated by looking for the activation file and license.
    Returns True if activated, False otherwise.
    """
    print("فحص التفعيل...")
    if not os.path.exists(LICENSE_FILE):
        print("ملف الترخيص غير موجود.")
        return False
    with open(LICENSE_FILE, "r") as f:
        if f.read().strip() != LICENSE_CONTENT:
            print("محتوى الترخيص غير صحيح.")
            return False
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
        Returns a dict of lists of debts per person.
        """
        if os.path.exists("debts.json"):
            with open("debts.json", "r") as f:
                data = json.load(f)
                # Convert old format if necessary
                if isinstance(data, list):
                    # Old format: list of dicts
                    new_data = {}
                    for debt in data:
                        name = debt['name']
                        if name not in new_data:
                            new_data[name] = []
                        new_data[name].append({'amount': debt['amount'], 'due_date': debt['due_date']})
                    return new_data
                return data
        return {}

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

        tk.Button(self.root, text="إضافة شخص جديد", command=self.add_person).pack(side=tk.LEFT, padx=5)
        tk.Button(self.root, text="عرض ديون الشخص", command=self.view_person).pack(side=tk.LEFT, padx=5)
        tk.Button(self.root, text="حذف شخص", command=self.delete_person).pack(side=tk.LEFT, padx=5)
        tk.Button(self.root, text="خروج", command=self.root.quit).pack(side=tk.RIGHT, padx=5)

    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for name, debts in self.debts.items():
            total = sum(debt['amount'] for debt in debts)
            self.listbox.insert(tk.END, f"{name}: إجمالي الديون {total} دينار عراقي")

    def add_person(self):
        name = simpledialog.askstring("إضافة شخص جديد", "اسم المدين:")
        if not name:
            return
        if name in self.debts:
            messagebox.showerror("خطأ", "الشخص موجود بالفعل!")
            return
        amount = simpledialog.askfloat("إضافة دين", "المبلغ بالدينار العراقي:")
        if amount is None:
            return
        due_date = simpledialog.askstring("إضافة دين", "تاريخ الاستحقاق (YYYY-MM-DD):")
        if not due_date:
            return
        self.debts[name] = [{"amount": amount, "due_date": due_date}]
        self.save_debts()
        self.update_listbox()

    def view_person(self):
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showwarning("تحذير", "اختر شخصاً لعرض ديونه!")
            return
        index = selected[0]
        name = list(self.debts.keys())[index]
        self.open_person_window(name)

    def open_person_window(self, name):
        person_window = tk.Toplevel(self.root)
        person_window.title(f"ديون {name}")
        try:
            person_window.iconbitmap('icon.ico')
        except:
            pass

        debts = self.debts[name]
        total = sum(debt['amount'] for debt in debts)

        tk.Label(person_window, text=f"إجمالي الديون: {total} دينار عراقي", font=("Arial", 14)).pack(pady=10)

        listbox = tk.Listbox(person_window, width=50, height=10)
        listbox.pack(pady=10)
        for i, debt in enumerate(debts):
            listbox.insert(tk.END, f"{i+1}. {debt['amount']} دينار - استحقاق: {debt['due_date']}")

        tk.Button(person_window, text="إضافة دين جديد", command=lambda: self.add_debt_to_person(name, listbox, person_window)).pack(side=tk.LEFT, padx=5)
        tk.Button(person_window, text="دفع دين", command=lambda: self.pay_debt_person(name, listbox, person_window)).pack(side=tk.LEFT, padx=5)
        tk.Button(person_window, text="حذف دين", command=lambda: self.delete_debt_person(name, listbox, person_window)).pack(side=tk.LEFT, padx=5)
        tk.Button(person_window, text="إغلاق", command=person_window.destroy).pack(side=tk.RIGHT, padx=5)

    def add_debt_to_person(self, name, listbox, window):
        amount = simpledialog.askfloat("إضافة دين", "المبلغ بالدينار العراقي:")
        if amount is None:
            return
        due_date = simpledialog.askstring("إضافة دين", "تاريخ الاستحقاق (YYYY-MM-DD):")
        if not due_date:
            return
        self.debts[name].append({"amount": amount, "due_date": due_date})
        self.save_debts()
        self.update_person_window(name, listbox, window)

    def pay_debt_person(self, name, listbox, window):
        selected = listbox.curselection()
        if not selected:
            messagebox.showwarning("تحذير", "اختر ديناً للدفع!")
            return
        index = selected[0]
        pay_amount = simpledialog.askfloat("دفع دين", f"مبلغ الدفع بالدينار العراقي:")
        if pay_amount is None or pay_amount <= 0:
            return
        if pay_amount >= self.debts[name][index]['amount']:
            del self.debts[name][index]
        else:
            self.debts[name][index]['amount'] -= pay_amount
        self.save_debts()
        self.update_person_window(name, listbox, window)
        self.update_listbox()

    def delete_debt_person(self, name, listbox, window):
        selected = listbox.curselection()
        if not selected:
            messagebox.showwarning("تحذير", "اختر ديناً لحذفه!")
            return
        index = selected[0]
        del self.debts[name][index]
        self.save_debts()
        self.update_person_window(name, listbox, window)
        self.update_listbox()

    def update_person_window(self, name, listbox, window):
        debts = self.debts[name]
        total = sum(debt['amount'] for debt in debts)
        # Update total label - assuming it's the first label
        for widget in window.winfo_children():
            if isinstance(widget, tk.Label) and "إجمالي" in widget.cget("text"):
                widget.config(text=f"إجمالي الديون: {total} دينار عراقي")
                break
        listbox.delete(0, tk.END)
        for i, debt in enumerate(debts):
            listbox.insert(tk.END, f"{i+1}. {debt['amount']} دينار - استحقاق: {debt['due_date']}")

    def delete_person(self):
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showwarning("تحذير", "اختر شخصاً لحذفه!")
            return
        index = selected[0]
        name = list(self.debts.keys())[index]
        if messagebox.askyesno("تأكيد", f"هل تريد حذف {name} وجميع ديونه؟"):
            del self.debts[name]
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