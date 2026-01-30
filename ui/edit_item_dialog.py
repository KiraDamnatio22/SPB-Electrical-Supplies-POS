import customtkinter as ctk


class EditItemDialog(ctk.CTkToplevel):
    def __init__(self, master, item):
        super().__init__(master)
        self.result = None

        self.title("Edit Item")
        self.geometry("400x420")
        self.grab_set()

        ctk.CTkLabel(self, text="Edit Item", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)

        self.name = ctk.CTkEntry(self)
        self.name.insert(0, item["name"])
        self.name.pack(fill="x", padx=30, pady=5)

        self.category = ctk.CTkEntry(self)
        self.category.insert(0, item["category"])
        self.category.pack(fill="x", padx=30, pady=5)

        self.price = ctk.CTkEntry(self)
        self.price.insert(0, str(item["price"]))
        self.price.pack(fill="x", padx=30, pady=5)

        self.desc = ctk.CTkTextbox(self, height=120)
        self.desc.insert("1.0", item["description"] or "")
        self.desc.pack(fill="both", padx=30, pady=5)

        ctk.CTkButton(self, text="Save", command=self.save).pack(pady=15)

    def save(self):
        self.result = {
            "name": self.name.get().strip(),
            "category": self.category.get().strip(),
            "price": float(self.price.get()),
            "description": self.desc.get("1.0", "end").strip()
        }
        self.destroy()
