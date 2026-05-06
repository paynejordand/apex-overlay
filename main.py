import os
import tkinter as tk
import tk_async_execute as tae
from wss import WSServer
from PIL import Image, ImageTk, ImageDraw

class App:
    def __init__(self, root, base_image="media\\base.png"):
        self.root = root
        self.base_image = base_image

    def setup(self):
        self.root.title("Apex Legends Overlay")
        self.root.geometry("300x200")
        tk.Button(self.root, text="Start server", command=self.start_server_button, width=20).pack()
        tk.Button(self.root, text="Show meds", command=lambda: self.create_meds_display(self.base_image), width=20).pack()
        tk.Button(self.root, text="Preview respawn banner", command=lambda: self.create_respawn_banner(duration=0), width=20).pack()
        self.meds_window = None
        self.respawn_window = None
        self.wss = WSServer(respawn_callback=self.create_respawn_banner)

    def run(self):
        self.root.mainloop()

    async def start_server(self):
        # Call tkinter widget methods.
        print("Async function called!")
        await self.wss.start()

    def start_server_button(self):
        # Call async function
        tae.async_execute(self.start_server(), wait=False, master=self.root, 
                          show_progress_bar=False, window_title="Server Starting", 
                          window_resizable=(True, True), show_stdout=True)

    def update_counts(self):
        img = self.create_meds_image(self.base_image)
        self.meds_label.configure(image=img)
        self.meds_label.image = img
        self.meds_window.after(100, self.update_counts)

    def create_meds_window(self):
        img_window = tk.Toplevel(self.root)
        img_window.title("Meds")
        self.meds_window = img_window

    def create_meds_image(self, base_image, textFill=(255, 255, 255, 200), strokeWidth=2.5, strokeFill=(0, 0, 0, 255), fontSize=25):
        med_counts = self.wss.get_active_player_meds()
        image = Image.open(base_image)
        txt = Image.new("RGBA", image.size, (255, 255, 255, 0))
        d = ImageDraw.Draw(txt)
        d.text((5, 5), str(med_counts["syringes"]), fill=textFill, stroke_width=strokeWidth, stroke_fill=strokeFill, font_size=fontSize)
        d.text((138, 5), str(med_counts["medkits"]), fill=textFill, stroke_width=strokeWidth, stroke_fill=strokeFill, font_size=fontSize)
        d.text((271, 5), str(med_counts["phoenixKits"]), fill=textFill, stroke_width=strokeWidth, stroke_fill=strokeFill, font_size=fontSize)
        d.text((5, 138), str(med_counts["shieldCells"]), fill=textFill, stroke_width=strokeWidth, stroke_fill=strokeFill, font_size=fontSize)
        d.text((138, 138), str(med_counts["shieldBatteries"]), fill=textFill, stroke_width=strokeWidth, stroke_fill=strokeFill, font_size=fontSize)
        d.text((271, 138), str(med_counts["ultimateAccelerants"]), fill=textFill, stroke_width=strokeWidth, stroke_fill=strokeFill, font_size=fontSize)
        image = Image.alpha_composite(image, txt)
        image = ImageTk.PhotoImage(image)
        return image
                

    def create_meds_display(self, base_image):
        if self.meds_window is not None and tk.Toplevel.winfo_exists(self.meds_window):
            return
        self.create_meds_window()
        img = self.create_meds_image(base_image)
        self.meds_label = tk.Label(self.meds_window, image=img)
        self.meds_label.pack()
        self.meds_label.image = img
        self.meds_window.after(100, self.update_counts)

    def create_respawn_banner(self, duration=5000, team="RAH", players=["Stink", "Monty"], fontSize=24, bg="#90EE90", fg="#000000"):
        if not self.respawn_window or not tk.Toplevel.winfo_exists(self.respawn_window):
            self.respawn_window = tk.Toplevel(self.root)
            self.respawn_window.title("Respawn Banner")
        respawn_label = tk.Label(self.respawn_window, 
                                 text=f"{team} respawned {', and '.join(players)}", 
                                 font=("Arial", fontSize), bg=bg, fg=fg)
        respawn_label.pack()
        if duration:
            self.respawn_window.after(duration, lambda: self.respawn_delete(respawn_label))

    def respawn_delete(self, respawn_label):
        respawn_label.destroy()
        if not self.respawn_window.winfo_children():
            self.respawn_window.destroy()
            self.respawn_window = None
                

if __name__ == "__main__":
    bundle_dir = os.path.abspath(os.path.dirname(__file__))
    path_to_dat = os.path.join(bundle_dir, 'media\\base.png')
    app = App(root=tk.Tk(), base_image=path_to_dat)
    app.setup()  

    tae.start()  # Starts the asyncio event loop in a different thread.
    app.run()  # Main Tkinter loop
    tae.stop()  # Stops the event loop and closes it.