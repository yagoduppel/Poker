import tkinter as tk
import sys

class UI:

    def __init__(self, game = None, *args, **kwargs):


        self.game = game
        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.args, self.kwargs = args, kwargs

        self.create_window()

        self.game.update()

        #Keep playing until only one player is left
        while self.game.players_num > 1:
            self.game.new_hand()



        self.root.mainloop()

    def create_window(self):
        #dimensions of the window
        width = self.kwargs.get("width", 600)
        height = self.kwargs.get("height", 800)

        #screen dimensions
        width_screen = self.root.winfo_screenwidth() # width of the screen
        height_screen = self.root.winfo_screenheight() # height of the screen

        #coordinates of top left window corner
        x = (width_screen/2) - (width/2)
        y = (height_screen/2) - (height/2)
        self.root.geometry(f"{width}x{height}+{int(x)}+{int(y)}")


        self.root.title(f"Poker Table - {self.game.players_num} People Playing")
        self.root.focus_force()


    def on_closing(self):
        if tk.messagebox.askokcancel("Quit", "Are you sure you want to quit?"):
            self.root.destroy()
            sys.exit()


