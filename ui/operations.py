import customtkinter as ctk
from datetime import datetime
from barcode import Code128
from barcode.writer import ImageWriter

from ui.popups import InputDialog, InfoDialog, InOutDialog
from db.paths import LABEL_DIR
from db.inventory_repository import InventoryRepository


class OperationsWindow(ctk.CTkToplevel):
    def __init__(self, master, db):
        super().__init__(master)

        self.db = db
        self.repo = InventoryRepository(db)

        self.title("Inventory Operations")
        self.geometry("650x400+380+140")
        self.grab_set()

        ctk.CTkButton(
            self, text="New Item",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.create_item
        ).pack(pady=(30, 10))

        ctk.CTkButton(
            self, text="Reset Barcodes",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.reset_database
        ).pack(pady=10)

        ctk.CTkLabel(self, text="Scan Barcode").pack(pady=(40, 5))

        self.barcode_entry = ctk.CTkEntry(self, width=250)
        self.barcode_entry.pack()
        self.after(10, self.barcode_entry.focus_set)

        self.barcode_entry.bind("<Return>", self.scan_barcode)

    def create_item(self):
        code = self.generate_barcode()

        name = InputDialog(self, "Product Name")
        self.wait_window(name)

        category = InputDialog(self, "Category")
        self.wait_window(category)

        if not name.result:
            return

        self.repo.create_item(code, name.result, category.result)
        self.print_barcode(code)
        self.master.refresh_item_list()

        # self.db.cur.execute("""
        #     INSERT INTO items VALUES (?, ?, ?, 0, ?)
        # """, (code, name.result, category.result, datetime.now().isoformat()))
        # self.db.conn.commit()
        # self.master.refresh_item_list()

        # self.print_barcode(code)
        InfoDialog(self, "New Product", "Created", f"{name.result}\n{code}")

    def generate_barcode(self):
        count = self.repo.count_items()
        return f"EL-{count + 1:08d}"

    # def generate_barcode(self):
    #     self.db.cur.execute("SELECT COUNT(*) FROM items")
    #     return f"EL-{self.db.cur.fetchone()[0] + 1:08d}"

    def print_barcode(self, code):
        LABEL_DIR.mkdir(parents=True, exist_ok=True)
        Code128(code, writer=ImageWriter()).save(LABEL_DIR / code)

    def scan_barcode(self, event=None):
        code = self.barcode_entry.get().strip()
        print(f"code: {code}")
        self.barcode_entry.delete(0, "end")

        item = self.repo.get_item_by_barcode(code)
        # self.db.cur.execute("SELECT name, quantity FROM items WHERE barcode=?", (code,))
        # item = self.db.cur.fetchone()

        print(item)

        if not item:
            InfoDialog(self, title="Error", header="Error", info="Barcode not found")
            # messagebox.showerror("Error", "Barcode not found")
            return

        name, qty = item

        action_dialog = InOutDialog(self, name)
        self.wait_window(action_dialog)
        action_value = action_dialog.result

        qty_dialog = None
        if action_value:
            qty_dialog = InputDialog(self, title="Quantity", entry_width=150)
            self.wait_window(qty_dialog)
        else:
            qty_dialog = InputDialog(self, title="Quantity", entry_width=150)
            self.wait_window(qty_dialog)

        amount = int(qty_dialog.result)
        print(f"amount: {amount}")

        if not amount:
            return

        if not action_value and amount > qty:
            InfoDialog(self, title="", header="Error", info="Insufficient stock")
            # messagebox.showerror("Error", "Insufficient stock")
            return
        
        new_qty = qty + amount if action_value else qty - amount
        self.repo.update_quantity(code, new_qty)
        self.repo.record_transaction(code, "IN" if action_value else "OUT", amount)

        self.master.refresh_item_list()

        # qty = qty + amount if action_value else qty - amount

        # self.db.cur.execute("UPDATE items SET quantity=? WHERE barcode=?", (qty, code))
        # self.db.cur.execute("""
        #     INSERT INTO transactions (barcode, action, qty, timestamp)
        #     VALUES (?, ?, ?, ?)
        # """, (code, "IN" if action_value else "OUT", amount, datetime.now().isoformat()))

        # self.db.conn.commit()
        # self.master.refresh_item_list()

        InfoDialog(self, title="Info", header="Updated", info=f"{name}\nStock: {qty}")

    def reset_database(self):
        confirm_dialog = InputDialog(self, "Type RESET to confirm")
        self.wait_window(confirm_dialog)
        confirm_result = confirm_dialog.result.lower()

        if confirm_result == "reset":
            png_files = list(LABEL_DIR.glob("*.png"))
        
            if not png_files:
                InfoDialog(self, header="No png files found.", info="/error/")
                return
            
            for file in png_files:
                file.unlink()

            self.db.reset_db()
            InfoDialog(self, title="Reset", header="Complete", info="Database reset.\nAll barcode images are deleted.")
