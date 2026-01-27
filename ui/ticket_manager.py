import customtkinter as ctk
from sympy import expand

class TicketRow(ctk.CTkFrame):
    def __init__(self, parent, item, qty):
        super().__init__(parent, fg_color="transparent")

        self.grid_columnconfigure((0), weight=1)

        left = ctk.CTkFrame(self, fg_color="transparent")
        left.grid(row=0, column=0, sticky="w", columnspan=2)

        ctk.CTkLabel(
            left,
            text=item["name"],
            font=ctk.CTkFont(family="Poppins", size=16, weight="bold"),
            anchor="w"
        ).pack(anchor="w", padx=(6, 0))

        ctk.CTkLabel(
            left,
            text=item["description"],
            font=ctk.CTkFont(family="Poppins", size=13),
            text_color="#777",
            anchor="w"
        ).pack(anchor="w", padx=(6, 0))

        self.insert_divider(left)

        right = ctk.CTkFrame(self, fg_color="transparent")
        right.grid(row=0, column=1, sticky="ew", padx=10, pady=(0, 10))

        ctk.CTkLabel(
            right,
            text=f"x{qty}",
            font=ctk.CTkFont(family="Poppins", size=16, weight="bold"),
            anchor="nw"
        ).pack(side="left", anchor="w", padx=(0, 50))

        ctk.CTkLabel(
            right,
            text=f"{item['price'] * qty:.2f}",
            font=ctk.CTkFont(family="Poppins", size=15),
            anchor="nw"
        ).pack(side="right", anchor="e")

    def insert_divider(self, master):
        divider = ctk.CTkFrame(master, border_width=0.8, fg_color="transparent", height=2, width=600)
        divider.pack(pady=(12, 0))
        divider.pack_propagate(False)