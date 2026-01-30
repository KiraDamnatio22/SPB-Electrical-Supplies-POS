import customtkinter as ctk
from sympy import product


class InputDialog(ctk.CTkToplevel):
    def __init__(self, master, title="Input", entry_width=250):
        super().__init__(master)

        self.result = None

        self.title(title)
        self.geometry("350x120+480+215")
        self.grab_set()
        self.resizable(False, False)

        self.entry = ctk.CTkEntry(self, width=entry_width)
        self.entry.pack(padx=20, pady=(30, 10))
        self.after(100, self.set_focus)

        ctk.CTkButton(self, text="OK", command=self.close, width=100).pack(pady=10)

        self.protocol("WM_DELETE_WINDOW", self.close)

    def set_focus(self):
        self.deiconify()
        self.lift()
        self.focus_force()
        self.entry.focus_set()

    def close(self):
        self.result = self.entry.get()
        self.grab_release()
        self.destroy()


class InfoDialog(ctk.CTkToplevel):
    def __init__(self, master, title="Info", header="None", info="None"):
        super().__init__(master)

        self.title(title)
        self.geometry("360x180+475+180")
        self.grab_set()
        self.resizable(False, False)
        self.configure(fg_color="white")

        # self.dialog_value = None

        ctk.CTkLabel(self, text=header, text_color="black", font=ctk.CTkFont(size=18, weight="bold")).pack(padx=20, pady=(25, 5))
        ctk.CTkLabel(self, text=info, text_color="black", font=ctk.CTkFont(size=16)).pack(padx=20, pady=10)

        ctk.CTkButton(self, text="OK", command=self.close, width=70).pack(pady=10)

        self.protocol("WM_DELETE_WINDOW", self.close)

    def close(self):
        # self.grab_release()
        self.destroy()


class InOutDialog(ctk.CTkToplevel):
    def __init__(self, master, product_name="None"):
        super().__init__(master)

        self.product_name = product_name
        self.result = None

        self.title("Action")
        self.geometry("360x180+475+180")
        self.grab_set()
        self.resizable(False, False)
        self.configure(fg_color="white")

        # self.dialog_value = None

        ctk.CTkLabel(self, text=product_name, text_color="black", font=ctk.CTkFont(size=22, weight="bold")).pack(padx=20, pady=(35, 10))

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=(30, 10))

        ctk.CTkButton(btn_frame, text="In", width=100, command=self.increment).pack(side="left", padx=10)

        ctk.CTkButton(btn_frame, text="Out", width=100, command=self.decrement).pack(side="left", padx=10)

    def increment(self):
        self.result = True
        self.grab_release()
        self.destroy()

    def decrement(self):
        self.result = False
        self.grab_release()
        self.destroy()





















# class CustomMessageBox(ctk.CTkToplevel):
#     def __init__(self, parent, title, message, on_confirm, msg1="Cancel", msg2="Yes, Delete", title_fg="#218838", msg1_fgcolor="#979da2", msg1_hovercolor="#7a7f85", msg2_fgcolor="#E63946", msg2_hovercolor="#C92A3F", message_pady=20, btn_pady=10, toplvl_width=400, toplvl_height=200, toplvl_posx=890, toplvl_posy=465, msg_font=("Poppins", 14)):
#         super().__init__(parent)
#         self.title(title)
#         self.geometry(f"{toplvl_width}x{toplvl_height}+{toplvl_posx}+{toplvl_posy}")
#         self.resizable(False, False)
#         self.configure(fg_color="#F0F0F0")
#         self.grab_set()
#         self.overrideredirect(True)

#         # Title label
#         title_label = ctk.CTkLabel(
#             self, 
#             text=title, 
#             font=("Poppins", 18, "bold"),
#             text_color="white", 
#             fg_color=title_fg, 
#             corner_radius=5, 
#             pady=10,
#             bg_color=title_fg
#         )
#         title_label.pack(fill="x")

#         # Message label
#         message_label = ctk.CTkLabel(
#             self, text=message, font=msg_font,
#             text_color="black", wraplength=350, pady=0
#         )
#         message_label.pack(pady=message_pady)

#         # Buttons frame
#         button_frame = ctk.CTkFrame(self, fg_color="#F0F0F0")
#         button_frame.pack(pady=btn_pady)

#         ctk.CTkButton(
#             button_frame, text=msg1,
#             fg_color=msg1_fgcolor, hover_color=msg1_hovercolor,
#             font=("Poppins", 13, "bold"),
#             text_color="white",
#             bg_color="#F0F0F0",
#             command=self.destroy
#         ).grid(row=0, column=0, padx=8)

#         ctk.CTkButton(
#             button_frame, text=msg2,
#             fg_color=msg2_fgcolor, hover_color=msg2_hovercolor,
#             font=("Poppins", 13, "bold"),
#             text_color="white",
#             bg_color="#F0F0F0",
#             command=on_confirm
#         ).grid(row=0, column=1, padx=8)