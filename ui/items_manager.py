import customtkinter as ctk

CATEGORY_COLORS = {
    "Label": "#9B59B6",
    "Scanner": "#E74C3C",
    "Wireless": "#3498DB",
    "Sticker": "#F39C12",
    "Solder": "#2ECC71"
}

# class ItemTile(ctk.CTkFrame):
#     def __init__(self, parent, name, description, category, command=None):
#         color = CATEGORY_COLORS.get(category, CATEGORY_COLORS["Default"])

#         super().__init__(
#             parent,
#             fg_color=color,
#             corner_radius=16,
#             height=90,
#             cursor="hand2"
#         )

#         self.grid_propagate(False)

#         name_lbl = ctk.CTkLabel(
#             self,
#             text=name,
#             font=ctk.CTkFont(size=16, weight="bold"),
#             text_color="white",
#             anchor="w"
#         )
#         name_lbl.pack(fill="x", padx=12, pady=(12, 2))

#         desc_lbl = ctk.CTkLabel(
#             self,
#             text=description,
#             font=ctk.CTkFont(size=13),
#             text_color="#F2F2F2",
#             anchor="w",
#             wraplength=200,
#             justify="left"
#         )
#         desc_lbl.pack(fill="x", padx=12)

#         if command:
#             self.bind("<Button-1>", lambda e: command())
#             name_lbl.bind("<Button-1>", lambda e: command())
#             desc_lbl.bind("<Button-1>", lambda e: command())







class ItemTile(ctk.CTkFrame):
    def __init__(
        self,
        parent,
        item,
        on_click
    ):
        """
        item = {
            id, name, description, category,
            price, stock, image_path
        }
        """

        color = CATEGORY_COLORS.get(item["category"], CATEGORY_COLORS["Solder"])

        super().__init__(
            parent,
            fg_color=color,
            corner_radius=18,
            height=110,
            cursor="hand2"
        )
        self.grid_propagate(False)

        self.item = item
        self.on_click = on_click


        # ================= TOP ROW =================
        top = ctk.CTkFrame(self, fg_color="transparent")
        top.pack(fill="x", padx=10, pady=(10, 4))

        thumb_lbl = ctk.CTkLabel(top, image=item["image"], text="")
        thumb_lbl.pack(side="top", padx=(0, 8), pady=10)

        hover_color = self.darken_color(color, 0.12)

        thumb_lbl.bind("<Enter>", lambda e: self.animate_color(thumb_lbl, color, hover_color))
        thumb_lbl.bind("<Leave>", lambda e: self.animate_color(thumb_lbl, hover_color, color))

        # Name + description
        text_frame = ctk.CTkFrame(top, fg_color="transparent")
        text_frame.pack(fill="x", expand=True)

        name_lbl = ctk.CTkLabel(
            text_frame,
            text=item["name"],
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color="white",
            anchor="w"
        )
        name_lbl.pack(fill="x")

        desc_lbl = ctk.CTkLabel(
            text_frame,
            text=item["description"],
            font=ctk.CTkFont(size=12),
            text_color="#EAEAEA",
            anchor="w",
            wraplength=180,
            justify="left"
        )
        desc_lbl.pack(fill="x")

        # ================= BOTTOM ROW =================
        bottom = ctk.CTkFrame(self, fg_color="transparent")
        bottom.pack(fill="x", padx=12, pady=(0, 8))

        price_lbl = ctk.CTkLabel(
            bottom,
            text=f"₱{item['price']:.2f}",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="white"
        )
        price_lbl.pack(side="left")

        stock_color = "#2ECC71" if item["stock"] > 0 else "#E74C3C"

        stock_lbl = ctk.CTkLabel(
            bottom,
            text=f"STOCK {item['stock']}",
            fg_color=stock_color,
            corner_radius=8,
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="white",
            width=70,
            height=24
        )
        stock_lbl.pack(side="right")

        # ================= CLICK BINDINGS =================
        for widget in (self, top, thumb_lbl, name_lbl, desc_lbl, bottom, price_lbl, stock_lbl):
            widget.bind("<Button-1>", self.handle_click)


    def handle_click(self, event):
        if self.item["stock"] <= 0:
            return
        self.on_click(self.item)

    # def handle_click(self, event):
    #     if self.item["stock"] <= 0:
    #         return
        # self.configure(scale=0.97)
        # self.after(80, lambda: self.configure(scale=1.0))
        # self.on_click(self.item)

    def on_hover(self, event):
        self.configure(fg_color=self.hover_color)

    def on_leave(self, event):
        self.configure(fg_color=self.default_color)

    def darken_color(self, hex_color, factor=0.12):
        hex_color = hex_color.lstrip("#")
        r, g, b = (int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        r = int(r * (1 - factor))
        g = int(g * (1 - factor))
        b = int(b * (1 - factor))
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def interpolate_color(self, c1, c2, t):
        return tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))

    def hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip("#")
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def rgb_to_hex(self, rgb):
        return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"
    
    def animate_color(self, widget, start, end, steps=8, delay=15):
        start_rgb = self.hex_to_rgb(start)
        end_rgb = self.hex_to_rgb(end)

        def step(i=0):
            if i > steps:
                return
            t = i / steps
            color = self.rgb_to_hex(self.interpolate_color(start_rgb, end_rgb, t))
            widget.configure(fg_color=color)
            widget.after(delay, step, i + 1)

        step()



