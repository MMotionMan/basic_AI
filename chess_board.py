import tkinter as tk
from PIL import Image, ImageTk
from main import annealing, output_board
BOARDSIDE = 40
COLORS = ('black', 'white')
CELLSIZE = 40
SCREEN_HEIGHT = 1
SCREEN_WIDTH = 1
R = 30
#
# T = 100
# FINAL_TEMP = 0.05
# STEPS_PER_CHANGE = 100
# MAX_STEP = 10000
# ALPHA = 0.99
# LENGTH = 20


# output_board(ans)
# print(energy)


class Chessboard(tk.Frame):
    def __init__(self, parent, board, length):
        self.parent = parent
        tk.Frame.__init__(self, parent)
        self.make_board(board, length)


    def make_board(self, board, length):
        grid_list = []

        for i in range(length):
            self.rowconfigure(i, weight=1)
            self.columnconfigure(i, weight=1)
        self.pack()
        for i in range(length):
            grid_row = []
            for j in range(length):
                c = (i + j) & 1
                f = tk.Canvas(self, background=COLORS[c])

                f.grid(row=i, column=j, sticky=tk.N + tk.S + tk.W + tk.E)
                grid_row.append(f)
            grid_list.append(grid_row)
        self.update()
        for i in range(length):
            for j in range(length):
                if board[i][j] == 1:
                    grid_width = grid_list[i][j].winfo_width()
                    grid_height = grid_list[i][j].winfo_height()
                    grid_list[i][j].create_oval(grid_width/2-(grid_width*2/CELLSIZE),
                                             grid_height/2-(grid_height*2/CELLSIZE),
                                             grid_width/2+(grid_width*2/CELLSIZE),
                                             grid_height/2+(grid_height*2/CELLSIZE), outline="#f11", fill="#1f1")


class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.create_main_widgets()
        self.timer = 0
        self.board = None

    def start_compute(self, main_frame, T, FINAL_TEMP, STEPS_PER_CHANGE, MAX_STEP, ALPHA, LENGTH):
        ans, energy = annealing(float(T), float(FINAL_TEMP), int(STEPS_PER_CHANGE),
                                int(MAX_STEP), float(ALPHA), int(LENGTH))
        main_frame.pack()
        if self.timer != 0:
            self.board.destroy()
        print(energy)
        self.board = Chessboard(parent=main_frame, board=ans, length=int(LENGTH))

        self.board.pack(side=tk.LEFT)
        self.board.update()
        self.timer += 1

    def create_text_frame(self, frame):
        return tk.Text(frame, width=25, height=5)

    def create_label_frame(self, frame, text):
        return tk.Label(frame, text)

    def get_text(self, text_frame):
        return text_frame.get('1.0', tk.END)

    def create_main_widgets(self):
        main_frame = tk.Frame(self.root)
        main_frame.pack()
        text_frame = tk.LabelFrame(main_frame, width=10*6, height=2*6)
        temperature_label = tk.Label(text_frame, text='T')
        temperature_text = tk.Text(text_frame, width=10, height=2)

        final_temp_label = tk.Label(text_frame, text='FINAL TEMP')
        final_temp_text = tk.Text(text_frame, width=10, height=2)

        steps_per_change_label = tk.Label(text_frame, text='STEPS PER CHANGE')
        steps_per_change_text = tk.Text(text_frame, width=10, height=2)

        max_step_label = tk.Label(text_frame, text='MAX STEPS')
        max_step_text = tk.Text(text_frame, width=10, height=2)

        alpha_label = tk.Label(text_frame, text='ALPHA')
        alpha_text = tk.Text(text_frame, width=10, height=2)

        length_label = tk.Label(text_frame, text='length')
        length_text = tk.Text(text_frame, width=10, height=2)

        temperature_label.pack(side=tk.LEFT)
        temperature_text.pack(side=tk.LEFT)
        final_temp_label.pack(side=tk.LEFT)
        final_temp_text.pack(side=tk.LEFT)
        steps_per_change_label.pack(side=tk.LEFT)
        steps_per_change_text.pack(side=tk.LEFT)
        max_step_label.pack(side=tk.LEFT)
        max_step_text.pack(side=tk.LEFT)
        alpha_label.pack(side=tk.LEFT)
        alpha_text.pack(side=tk.LEFT)

        start_button = tk.Button(main_frame, text='Compute Solution', command=lambda: self.start_compute(main_frame,
            self.get_text(temperature_text), self.get_text(final_temp_text), self.get_text(steps_per_change_text),
            self.get_text(max_step_text), self.get_text(alpha_text), self.get_text(length_text)
        ))
        main_frame.update()
        start_button.pack()
        text_frame.update()
        length_label.pack(side=tk.LEFT)
        length_text.pack(side=tk.LEFT)
        text_frame.pack(side=tk.TOP)


app = MainWindow()
app.root.mainloop()
