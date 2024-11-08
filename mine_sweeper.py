import tkinter as tk
import random

class Minesweeper:
    def __init__(self, master, rows=10, columns=10, mines=20):
        self.master = master
        self.rows = rows
        self.columns = columns
        self.mines = mines
        self.buttons = []
        self.mine_positions = set()
        self.create_widgets()
        self.place_mines()

    def create_widgets(self):
        self.toolbar = tk.Frame(self.master)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        self.restart_button = tk.Button(self.toolbar, text="Restart", command=self.restart)
        self.restart_button.pack(side=tk.LEFT)

        self.level_up_button = tk.Button(self.toolbar, text="Level Up", command=self.level_up)
        self.level_up_button.pack(side=tk.RIGHT)

        self.frame = tk.Frame(self.master)
        self.frame.pack()

        self.create_buttons()

    def create_buttons(self):
        for r in range(self.rows):
            row = []
            for c in range(self.columns):
                button = tk.Button(self.frame, width=2, height=1, command=lambda r=r, c=c: self.click(r, c))
                button.grid(row=r, column=c)
                row.append(button)
            self.buttons.append(row)

    def place_mines(self):
        while len(self.mine_positions) < self.mines:
            r = random.randint(0, self.rows - 1)
            c = random.randint(0, self.columns - 1)
            self.mine_positions.add((r, c))

    def click(self, r, c):
        if (r, c) in self.mine_positions:
            self.buttons[r][c].config(text='*', bg='red')
            self.game_over()
        else:
            self.reveal(r, c)

    def reveal(self, r, c):
        if self.buttons[r][c]['text'] == '':
            mines_count = self.count_mines(r, c)
            self.buttons[r][c].config(text=str(mines_count), state='disabled')
            if mines_count == 0:
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if 0 <= r + dr < self.rows and 0 <= c + dc < self.columns:
                            self.reveal(r + dr, c + dc)

    def count_mines(self, r, c):
        count = 0
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if (r + dr, c + dc) in self.mine_positions:
                    count += 1
        return count

    def game_over(self):
        for r, c in self.mine_positions:
            self.buttons[r][c].config(text='*', bg='red')
        for row in self.buttons:
            for button in row:
                button.config(state='disabled')

    def restart(self):
        for row in self.buttons:
            for button in row:
                button.destroy()
        self.buttons = []
        self.mine_positions = set()
        self.create_buttons()
        self.place_mines()

    def level_up(self):
        self.rows += 5
        self.columns += 5
        self.mines += 10
        self.restart()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Minesweeper")
    game = Minesweeper(root)
    root.mainloop()
