import customtkinter as ctk
from db.db_base import DBClass
from db.inventory_repository import InventoryRepository
from db.paths import IconPath
from ui.items_manager import ItemTile
from ui.ticket_manager import TicketRow

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")


class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Electrical Supplies Inventory")
        self.geometry("1200x680+100+5")

        self.db = DBClass()
        self.repo = InventoryRepository(self.db)
        self.icon_list = IconPath().get_icons()
        self.ticket_items = {}
        self.item_tiles = {}   # {item_id: ItemTile}
        self.all_items = []    # raw item data cache


        # seed DB once
        self.repo.seed_items_if_empty()

        # self.main_frame = ctk.CTkFrame(self, fg_color="#eaeaea", border_width=1)
        self.main_frame = ctk.CTkFrame(self, border_width=0, fg_color="black", corner_radius=0)
        self.main_frame.pack(fill="both", expand=True)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(0, weight=1)

        # self.details_view = ctk.CTkFrame(self.main_frame, fg_color="#eaeaea")
        self.details_view = ctk.CTkFrame(self.main_frame, fg_color="white", corner_radius=0)
        self.details_view.grid(row=0, column=0, sticky="nsew")

        self.details_view.columnconfigure((0), weight=1)
        # self.details_view.rowconfigure((0), weight=1)
        # self.details_view.grid_columnconfigure(0, weight=1, uniform="a")
        # self.details_view.grid_rowconfigure(0, weight=0)  
        # self.details_view.grid_rowconfigure(1, weight=1)  

        self.checkout_view = ctk.CTkFrame(self.main_frame, fg_color="#eaeaea", corner_radius=0)
        self.checkout_view.grid(row=0, column=0, sticky="nsew")
        self.checkout_view.grid_columnconfigure(0, weight=1)
        self.checkout_view.grid_columnconfigure(1, weight=0)
        self.checkout_view.grid_rowconfigure(2, weight=1)
        self.checkout_view.grid_propagate(False)

        self.build_details_section()
        self.build_checkout_view()

        self.show_details_view()

        self.bind("<Escape>", lambda e: self.back_to_main_menu())
        self.bind("<F12>", lambda e: self.open_checkout())

    def show_details_view(self):
        # self.details_view.grid_columnconfigure(0, weight=1, uniform="a")
        self.details_view.grid_columnconfigure(0, weight=1)
        self.details_view.grid_columnconfigure(1, weight=0)
        self.details_view.grid_rowconfigure(0, weight=0)  
        self.details_view.grid_rowconfigure(1, weight=1)  
        self.details_view.tkraise()

    def show_checkout_view(self):
        self.checkout_view.tkraise()

    def open_checkout(self):
        self.build_checkout_orders()  # refresh data only
        self.show_checkout_view()

    def back_to_main_menu(self):
        self.refresh_ticket()
        self.show_details_view()

    def build_item_tiles(self, parent, items):
        col_count = 4
        row = col = 0

        for item in items:
            tile = ItemTile(
                parent,
                item=item,
                on_click=self.add_to_ticket
            )

            tile.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")

            self.item_tiles[item["id"]] = tile

            col += 1
            if col == col_count:
                col = 0
                row += 1

    def build_details_section(self):
        # ===================== MENU SECTION ========================= #

        menu_frame = ctk.CTkFrame(self.details_view, fg_color="#2CC985", corner_radius=0)
        menu_frame.grid(row=0, column=0, sticky="nsew")
        menu_frame.grid_propagate(False)
        menu_frame.grid_columnconfigure(1, weight=1)
        menu_frame.configure(height=80)

        ctk.CTkButton(
            menu_frame, 
            text="", 
            image=self.icon_list["menu"],
            fg_color="transparent",
            hover_color="#1FA169",
            width=50,
            height=50,
            command=self.open_sidebar
        ).grid(row=0, column=0, padx=(25, 0), pady=(15, 0))

        ctk.CTkLabel(menu_frame, text="SPB Electrical Supply", text_color="#FFFFFF", font=ctk.CTkFont(family="Poppins", size=27, weight="normal")).grid(row=0, column=1, padx=(15, 0), pady=(17, 0), sticky="w")

        optionmenu_var = ctk.StringVar(value="All items")
        optionmenu = ctk.CTkOptionMenu(
            menu_frame,
            values=["All items", "Solder", "Label", "Scanner", "Wireless", "Sticker"],
            variable=optionmenu_var,
            font=ctk.CTkFont(family="Poppins", size=22),
            dropdown_font=ctk.CTkFont(family="Poppins", size=16),
            fg_color="#2CC985",
            button_color="#2CC985",
            width=105,
            height=50,
            command=self.optionmenu_callback,
        )
        optionmenu.grid(row=0, column=2, padx=(0, 10), pady=(18, 0))

        search_btn = ctk.CTkLabel(
            menu_frame, 
            text="", 
            image=self.icon_list["search"],
            width=50,
            height=50,
            cursor="hand2",
        )
        search_btn.grid(row=0, column=3, padx=(0, 25), pady=(15, 0), sticky="e")
        search_btn.bind("<Button-1>", self.open_search_pane)

        # ===================== TICKET SECTION ========================= #

        ticket_frame = ctk.CTkFrame(self.details_view, fg_color="#fffefe", corner_radius=0)
        ticket_frame.grid(row=0, column=1, sticky="nsew")
        ticket_frame.grid_propagate(False)
        ticket_frame.grid_columnconfigure(0, weight=1)
        ticket_frame.configure(height=80, width=500)

        ctk.CTkLabel(ticket_frame, text="Ticket", font=ctk.CTkFont(family="Poppins", size=25, weight="normal"), fg_color="transparent").grid(row=0, column=0, padx=(30, 0), pady=(20, 0), sticky="w")
        
        account_btn = ctk.CTkLabel(
            ticket_frame, 
            text="", 
            image=self.icon_list["account"],
            width=50,
            height=50,
            cursor="hand2"
            # fg_color="lightgreen"
        )
        account_btn.grid(row=0, column=1, padx=(25, 0), pady=(15, 0))
        account_btn.bind("<Button-1>", self.open_account_pane)

        ticket_options_btn = ctk.CTkLabel(
            ticket_frame, 
            text="", 
            image=self.icon_list["more_vert"],
            width=50,
            height=50,
            cursor="hand2",
            # fg_color="lightgreen"
        )
        ticket_options_btn.grid(row=0, column=2, padx=(15, 25), pady=(15, 0))
        ticket_options_btn.bind("<Button-1>", self.open_ticket_option_menu)

        # ===================== ITEMS SECTION ========================= #
        self.items_frame = ctk.CTkFrame(self.details_view, fg_color="#eaeaea", corner_radius=0, border_width=1)
        self.items_frame.grid(row=1, column=0, sticky="nsew")
        self.items_frame.grid_propagate(False)

        # grid config → 4 columns
        for col in range(4):
            self.items_frame.grid_columnconfigure(col, weight=1)

        # items = self.fetch_items_for_ui()
        # self.load_items(self.items_frame, items)

        self.all_items = self.fetch_items_for_ui()
        self.build_item_tiles(self.items_frame, self.all_items)

        # ===================== ORDERS SECTION ========================= #

        orders_frame = ctk.CTkFrame(self.details_view, fg_color="#fffefe", corner_radius=0, border_width=1)
        orders_frame.grid(row=1, column=1, sticky="nsew")
        orders_frame.grid_propagate(False)
        orders_frame.grid_rowconfigure(2, weight=1)
        orders_frame.grid_columnconfigure(0, weight=1)
        orders_frame.configure(width=500)

        purchase_option_var = ctk.StringVar(value="Delivery")
        purchase_option = ctk.CTkOptionMenu(
            orders_frame,
            values=["Delivery", "Walk-In"],
            variable=purchase_option_var,
            font=ctk.CTkFont(family="Poppins", size=17),
            text_color="#6D6D6D",
            dropdown_font=ctk.CTkFont(family="Poppins", size=16),
            fg_color="#fffefe",
            button_color="#fffefe",
            button_hover_color="#c3c0c0",
            height=50
            # command=self.optionmenu_callback,
        )
        purchase_option.grid(row=0, column=0, sticky="nsew", padx=(15, 25), pady=(15, 10))

        divider = ctk.CTkFrame(orders_frame, border_width=0.8, fg_color="transparent", height=2)

        divider.grid(row=1, column=0, sticky="nsew", padx=(16, 25))

        # Scrollable items
        self.ticket_items_frame = ctk.CTkScrollableFrame(
            orders_frame,
            fg_color="transparent"
        )
        self.ticket_items_frame.grid(row=2, column=0, sticky="nsew", padx=10)

        self.ticket_action_frame = ctk.CTkFrame(orders_frame, fg_color="transparent")
        self.ticket_action_frame.grid(row=3, column=0, sticky="ew", padx=15, pady=10)

        ctk.CTkButton(
            self.ticket_action_frame,
            text="Save Ticket",
            height=45,
            command=self.save_ticket
        ).pack(side="left", expand=True, fill="x", padx=(0, 8))

        ctk.CTkButton(
            self.ticket_action_frame,
            text="Charge",
            height=45,
            fg_color="#2CC985",
            command=self.open_checkout
        ).pack(side="right", expand=True, fill="x", padx=(8, 0))

    def build_checkout_view(self):

        # Back to menu button
        back_btn = ctk.CTkButton(
            self.checkout_view,
            text="",
            image=self.icon_list["back_ios"],
            fg_color="#EAEAEA",
            hover_color="#959494",
            width=65,
            height=40,
            command=self.back_to_main_menu
        )
        back_btn.grid(row=0, column=0, columnspan=2, padx=(15, 0), pady=(15, 0), sticky="w")

        # Header
        header = ctk.CTkLabel(
            self.checkout_view,
            text="Checkout",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        header.grid(row=1, column=0, columnspan=2, pady=15)

        # # LEFT — Order Summary
        self.checkout_orders = ctk.CTkFrame(self.checkout_view, fg_color="#E5E1E1")
        self.checkout_orders.grid(row=2, column=0, sticky="nsew", padx=15, pady=10)

        self.checkout_view.grid_columnconfigure(0, weight=1)
        self.checkout_view.grid_columnconfigure(1, weight=0)
        self.checkout_view.grid_rowconfigure(2, weight=1)

        self.checkout_orders_inner = ctk.CTkFrame(self.checkout_orders,fg_color="#E5E1E1")
        self.checkout_orders_inner.pack(fill="both", expand=True, padx=10, pady=10)

        self.build_checkout_orders()

        # RIGHT — Payment
        self.checkout_payment = ctk.CTkFrame(self.checkout_view, width=550, border_width=1)
        self.checkout_payment.grid(row=2, column=1, padx=15, pady=10, sticky="ns")
        self.checkout_payment.pack_propagate(False)

        self.build_payment_panel()

    def build_payment_panel(self):
        self.cash_var = ctk.StringVar(value="")
        self.cash_var.trace_add("write", lambda *_: self.calculate_change())
        self.change_var = ctk.StringVar(value="0.00")

        ctk.CTkLabel(self.checkout_payment, text="Cash Received", font=ctk.CTkFont(family="Poppins", size=22, weight="bold")).pack(anchor="center", padx=10, pady=(100, 10))

        cash_entry = ctk.CTkEntry(
            self.checkout_payment,
            textvariable=self.cash_var,
            width=300
        )
        cash_entry.pack(padx=10, pady=5, anchor="center")
        cash_entry.focus_set()

        ctk.CTkLabel(
            self.checkout_payment,
            textvariable=self.change_var,
            font=ctk.CTkFont(family="Poppins", size=22, weight="bold"),
            text_color="#484848"
        ).pack(pady=15)

        ctk.CTkButton(
            self.checkout_payment,
            text="Charge",
            fg_color="#2CC985",
            command=self.complete_transaction
        ).pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(
            self.checkout_payment,
            text="Print Receipt",
            command=self.print_receipt
        ).pack(fill="x", padx=10, pady=(0, 10))

    def build_checkout_orders(self):
        # clear previous content
        for w in self.checkout_orders_inner.winfo_children():
            w.destroy()

        # column layout (matches orders_frame style)
        self.checkout_orders_inner.grid_columnconfigure(0, weight=3)  # name
        self.checkout_orders_inner.grid_columnconfigure(1, weight=4)  # description
        self.checkout_orders_inner.grid_columnconfigure(2, weight=1)  # qty
        self.checkout_orders_inner.grid_columnconfigure(3, weight=2)  # price

        total = 0
        row = 0

        for entry in self.ticket_items.values():
            item = entry["item"]
            qty = entry["qty"]
            line_total = item["price"] * qty
            total += line_total

            # NAME
            ctk.CTkLabel(
                self.checkout_orders_inner,
                text=item["name"],
                text_color="#2B2B2B",
                font=ctk.CTkFont(family="Poppins", size=15),
                anchor="w"
            ).grid(row=row, column=0, sticky="w", padx=(10, 4), pady=4)

            # DESCRIPTION
            ctk.CTkLabel(
                self.checkout_orders_inner,
                text=item["description"],
                font=ctk.CTkFont(family="Poppins", size=14),
                text_color="#8E8D8D",
                anchor="w"
            ).grid(row=row, column=1, sticky="w", padx=4)

            # QTY
            ctk.CTkLabel(
                self.checkout_orders_inner,
                text=f"×{qty}",
                font=ctk.CTkFont(family="Poppins", size=16, weight="bold"),
                anchor="center"
            ).grid(row=row, column=2, sticky="e", padx=4)

            # PRICE
            ctk.CTkLabel(
                self.checkout_orders_inner,
                text=f"{line_total:.2f}",
                font=ctk.CTkFont(family="Poppins", size=15),
                anchor="e"
            ).grid(row=row, column=3, sticky="e", padx=(4, 10))

            row += 1

        # divider
        ctk.CTkFrame(
            self.checkout_orders_inner,
            height=1,
            border_width=1.5
        ).grid(row=row, column=0, columnspan=4, sticky="ew", padx=10, pady=10)

        row += 1
        self.checkout_total = total

        # TOTAL aligned with price column
        ctk.CTkLabel(
            self.checkout_orders_inner,
            text="TOTAL",
            font=ctk.CTkFont(family="Poppins", size=17, weight="bold"),
            anchor="w"
        ).grid(row=row, column=0, sticky="w", padx=(10, 0))

        ctk.CTkLabel(
            self.checkout_orders_inner,
            text=f"{total:.2f}",
            font=ctk.CTkFont(family="Poppins", size=16, weight="bold"),
            anchor="e"
        ).grid(row=row, column=3, sticky="e", padx=(4, 10))

    def calculate_change(self):
        cash_str = self.cash_var.get().strip()

        if cash_str == "":
            self.change_var.set("Enter cash amount")
            return

        try:
            cash = float(cash_str)
        except ValueError:
            self.change_var.set("Invalid amount")
            return

        change = cash - self.checkout_total

        if change < 0:
            self.change_var.set("Insufficient cash")
        else:
            self.change_var.set(f"Change: ₱{change:.2f}")

    def open_sidebar(self):
        print("Side bar menu open.")

    def optionmenu_callback(self, choice):
        if choice == "All items":
            filtered = self.all_items
        else:
            filtered = [item for item in self.all_items if item["category"] == choice]

        self.filter_items(filtered)

    # def optionmenu_callback(self, choice):
    #     if choice == "All items":
    #         rows = self.repo.get_all_items()
    #     else:
    #         # Map UI labels to actual DB category values if needed
    #         rows = self.repo.get_items_by_category(choice)

    #     items = []
    #     for row in rows:
    #         barcode, name, category, qty, created_at, price, description = row

    #         items.append({
    #             "id": barcode,
    #             "name": name,
    #             "description": description,
    #             "category": category,
    #             "price": price,
    #             "stock": qty,
    #             "image": self.icon_list["product"]
    #         })

    # Reload items grid
    # You need a reference to items_frame; easiest is to store it as self.items_frame
    # self.load_items(self.items_frame, items)

    def open_search_pane(self, event):
        print("Search pane open.")

    def open_account_pane(self, event):
        print("Account pane open.")

    def open_ticket_option_menu(self, event):
        print("Ticket options open.")

    def filter_items(self, items_to_show):
        # Hide all tiles first
        for tile in self.item_tiles.values():
            tile.grid_remove()

        col_count = 4
        row = col = 0

        for item in items_to_show:
            tile = self.item_tiles.get(item["id"])
            if not tile:
                continue

            tile.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")

            col += 1
            if col == col_count:
                col = 0
                row += 1

    # def load_items(self, items_frame, items):
    #     for widget in items_frame.winfo_children():
    #         widget.destroy()

    #     col_count = 4
    #     row = col = 0

    #     for item in items:
    #         tile = ItemTile(
    #             items_frame,
    #             item=item,
    #             on_click=self.add_to_ticket
    #         )
    #         tile.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")

    #         col += 1
    #         if col == col_count:
    #             col = 0
    #             row += 1

    def fetch_items_for_ui(self):
        rows = self.repo.get_all_items()
        items = []

        for row in rows:
            barcode, name, category, qty, created_at, price, description = row

            items.append({
                "id": barcode,                 # UI still uses "id"
                "name": name,
                "description": description,
                "category": category,
                "price": price,
                "stock": qty,
                "image": self.icon_list["product"]
            })

        return items
    
    def add_to_ticket(self, item):
        item_id = item["id"]
        available_stock = item["stock"]

        if item_id in self.ticket_items:
            current_qty = self.ticket_items[item_id]["qty"]

            if current_qty >= available_stock:
                ctk.CTkMessagebox(
                    title="Stock Warning",
                    message=f"Only {available_stock} item(s) available.",
                    icon="warning"
                )
                return

            self.ticket_items[item_id]["qty"] += 1
        else:
            if available_stock <= 0:
                ctk.CTkMessagebox(
                    title="Out of Stock",
                    message="This item is out of stock.",
                    icon="warning"
                )
                return

            self.ticket_items[item_id] = {
                "item": item,
                "qty": 1
            }

        self.refresh_ticket()

    def refresh_ticket(self):
        for widget in self.ticket_items_frame.winfo_children():
            widget.destroy()

        total = 0

        for entry in self.ticket_items.values():
            item = entry["item"]
            qty = entry["qty"]

            row = TicketRow(self.ticket_items_frame, item, qty)
            row.pack(fill="x", pady=6)

            total += item["price"] * qty

        # self.total_label.configure(text=f"{total:.2f}")

    def save_ticket(self):
        print("Ticket saved")

    def complete_transaction(self):
        print("Transaction completed")
        self.ticket_items.clear()
        self.refresh_ticket()
        self.show_details_view()
        # deduct stock
        # record transaction
        # clear ticket
        # return to main screen

    def print_receipt(self):
        print("Printing receipt...")








