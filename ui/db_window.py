import customtkinter as ctk
from tkinter import ttk

from ui.operations import OperationsWindow
from db.db_base import DBClass
from db.inventory_repository import InventoryRepository

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")


class DBWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Inventory – Item List")
        self.geometry("1100x685+200+5")

        self.db = DBClass()
        self.repo = InventoryRepository(self.db)

        title = ctk.CTkLabel(
            self, text="Electrical Supplies Inventory",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        title.pack(pady=10)

        self.search_var = ctk.StringVar()
        self.search_var.trace_add("write", self.on_search)

        search_frame = ctk.CTkFrame(self)
        search_frame.pack(fill="x", padx=20, pady=(5, 0))

        ctk.CTkLabel(search_frame, text="Search:").pack(side="left", padx=(10, 5))

        self.search_entry = ctk.CTkEntry(
            search_frame,
            textvariable=self.search_var,
            placeholder_text="Barcode, name, or category..."
        )
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        # =========================
        # Item List Frame
        # =========================
        self.list_frame = ctk.CTkFrame(self)
        self.list_frame.pack(fill="both", expand=True, padx=20, pady=(5, 10))

        style = ttk.Style()
        style.theme_use("default")

        style.configure(
            "Treeview",
            font=("Segoe UI", 10),
            rowheight=28,
            background="#ffffff",
            fieldbackground="#ffffff",
            foreground="#222222",
            borderwidth=0
        )

        style.configure(
            "Treeview.Heading",
            font=("Segoe UI", 10, "bold"),
            background="#f1f5f9",
            foreground="#1f2933",
            borderwidth=0
        )

        style.map(
            "Treeview",
            background=[("selected", "#dbeafe")],
            foreground=[("selected", "#1e3a8a")]
        )

        self.build_item_table()
        self.load_items()

        ctk.CTkButton(
            self,
            text="Open Operations Panel",
            command=self.open_operations
        ).pack(pady=10)

        self.tree.bind("<Double-1>", self.show_description)
        self.tree.bind("<Double-2>", self.edit_selected_item)
        self.tree.bind("<Button-3>", self.show_context_menu)

        import tkinter as tk
        self.menu = tk.Menu(self, tearoff=0)
        self.menu.add_command(label="Edit Item", command=self.edit_selected_item)

    # =========================
    # TABLE SETUP
    # =========================
    def build_item_table(self):
        columns = ("barcode", "name", "category", "quantity", "price", "created")

        self.tree = ttk.Treeview(
            self.list_frame,
            columns=columns,
            show="headings",
            height=15
        )

        self.tree.heading("barcode", text="Barcode")
        self.tree.heading("name", text="Name")
        self.tree.heading("category", text="Category")
        self.tree.heading("quantity", text="Qty")
        self.tree.heading("price", text="Price")
        self.tree.heading("created", text="Created At")

        self.tree.column("barcode", width=180)
        self.tree.column("name", width=260)
        self.tree.column("category", width=160)
        self.tree.column("quantity", width=80, anchor="center")
        self.tree.column("price", width=100, anchor="e")
        self.tree.column("created", width=200)

        scrollbar = ttk.Scrollbar(
            self.list_frame,
            orient="vertical",
            command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def show_description(self, event):
        selected = self.tree.focus()
        if not selected:
            return

        barcode = self.tree.item(selected)["values"][0]
        item = self.repo.get_item_full(barcode)

        description = item["description"] or "No description available."

        from ui.popups import InfoDialog
        InfoDialog(
            self,
            title="Item Description",
            header=item["name"],
            info=description
        )

    def show_context_menu(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.tree.focus(item)
            self.menu.tk_popup(event.x_root, event.y_root)

    # =========================
    # LOAD / REFRESH
    # =========================
    def on_search(self, *_):
        query = self.search_var.get().lower().strip()

        if not query:
            self.populate_tree(self.all_items)
            return

        filtered = [
            item for item in self.all_items
            if query in item[0].lower()
            or query in item[1].lower()
            or query in (item[2] or "").lower()
        ]

        self.populate_tree(filtered)

    def load_items(self):
        self.all_items = self.repo.get_all_items()
        self.populate_tree(self.all_items)

    def populate_tree(self, items):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for item in items:
            self.tree.insert("", "end", values=(
                item[0],  # barcode
                item[1],  # name
                item[2],  # category
                item[3],  # qty
                f"{item[5]:,.2f}",  # price
                item[4],  # created
            ))

    # def load_items(self):
    #     for row in self.tree.get_children():
    #         self.tree.delete(row)

    #     for item in self.repo.get_all_items():
    #         self.tree.insert("", "end", values=(
    #             item[0],  # barcode
    #             item[1],  # name
    #             item[2],  # category
    #             item[3],  # qty
    #             f"{item[5]:,.2f}",  # price
    #             item[4],  # created_at
    #         ))

    def edit_selected_item(self):
        selected = self.tree.focus()
        if not selected:
            return

        barcode = self.tree.item(selected)["values"][0]
        item = self.repo.get_item_full(barcode)

        from ui.edit_item_dialog import EditItemDialog
        dlg = EditItemDialog(self, item)
        self.wait_window(dlg)

        if dlg.result:
            self.repo.update_item(barcode, dlg.result)
            self.refresh_item_list()

    # def edit_selected_item(self):
    #     selected = self.tree.focus()
    #     if not selected:
    #         return

    #     barcode = self.tree.item(selected)["values"][0]
    #     item = self.repo.get_item_full(barcode)

    #     from ui.edit_item_dialog import EditItemDialog
    #     dlg = EditItemDialog(self, item)
    #     self.wait_window(dlg)

    #     if dlg.result:
    #         self.repo.update_item(barcode, dlg.result)
    #         self.refresh_item_list()

    def refresh_item_list(self):
        self.load_items()

    def open_operations(self):
        OperationsWindow(self, self.db)
