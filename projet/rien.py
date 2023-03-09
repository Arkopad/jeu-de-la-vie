import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class GameOfLife:
    def __init__(self, master):
        self.master = master
        self.master.title("Jeu de la vie")
        
        self.grid_size = 50
        self.cell_size = 10
        
        self.paused = False
        self.speed = 50
        
        self.create_widgets()
        
        self.grid = np.zeros((self.grid_size, self.grid_size), dtype=np.uint8)
        self.fig = plt.figure(figsize=(5, 5))
        self.ax = self.fig.add_subplot(111)
        self.im = self.ax.imshow(self.grid, cmap="binary", interpolation="nearest")
        self.anim = animation.FuncAnimation(self.fig, self.update, frames=self.evolve, interval=self.speed, blit=False)
        
    def create_widgets(self):
        # Zone d'affichage
        self.canvas = tk.Canvas(self.master, width=self.grid_size*self.cell_size, height=self.grid_size*self.cell_size, bg="white")
        self.canvas.pack(side=tk.LEFT)
        self.canvas.bind("<Button-1>", self.set_alive)
        self.canvas.bind("<B1-Motion>", self.set_alive)
        self.canvas.bind("<Button-3>", self.set_dead)
        self.canvas.bind("<B3-Motion>", self.set_dead)
        
        # Boutons de contrôle
        self.control_frame = tk.Frame(self.master)
        self.control_frame.pack(side=tk.LEFT, padx=10)
        self.start_button = tk.Button(self.control_frame, text="Start", command=self.start)
        self.start_button.pack(side=tk.TOP, pady=10)
        self.pause_button = tk.Button(self.control_frame, text="Pause", command=self.pause)
        self.pause_button.pack(side=tk.TOP, pady=10)
        self.speed_label = tk.Label(self.control_frame, text="Speed:")
        self.speed_label.pack(side=tk.TOP, pady=5)
        self.speed_slider = tk.Scale(self.control_frame, from_=1, to=100, orient=tk.HORIZONTAL, command=self.set_speed)
        self.speed_slider.pack(side=tk.TOP, pady=5)
        self.reset_button = tk.Button(self.control_frame, text="Reset", command=self.reset)
        self.reset_button.pack(side=tk.TOP, pady=10)
        self.quit_button = tk.Button(self.control_frame, text="Quit", command=self.master.quit)
        self.quit_button.pack(side=tk.TOP, pady=10)
        
        # Statistiques
        self.stats_frame = tk.Frame(self.master)
        self.stats_frame.pack(side=tk.LEFT, padx=10)
        self.cells_alive_label = tk.Label(self.stats_frame, text="Cells alive: 0")
        self.cells_alive_label.pack(side=tk.TOP, pady=5)
        self.cells_dead_label = tk.Label(self.stats_frame, text="Cells dead: 0")
        self.cells_dead_label.pack(side=tk.TOP, pady=5)
        self.generation_label = tk.Label(self.stats_frame, text="Generation: 0")
        self.generation_label.pack(side=tk.TOP, pady=5)
        
    def set_alive(self, event):
        x = event.x // self.cell_size
        y = event.y // self.cell_size
        self.grid[x, y] = 1
        self.draw_cell(x, y)
        
    def set_dead(self, event):
        x = event.x // self.cell_size
        y = event.y // self.cell_size
        self.grid[x, y] = 0

    def draw_cell(self, x, y):
        x0 = x*self.cell_size
        y0 = y*self.cell_size
        x1 = x0 + self.cell_size
        y1 = y0 + self.cell_size
        self.canvas.create_rectangle(x0, y0, x1, y1, fill="black", outline="white")
        
    def evolve(self):
        while True:
            yield self.grid
            new_grid = np.zeros_like(self.grid)
            for i in range(self.grid_size):
                for j in range(self.grid_size):
                    neighbors = self.grid[max(0, i-1):min(self.grid_size, i+2), max(0, j-1):min(self.grid_size, j+2)]
                    cell = self.grid[i, j]
                    count = np.count_nonzero(neighbors) - cell
                    if cell == 1 and count in (2, 3):
                        new_grid[i, j] = 1
                    elif cell == 0 and count == 3:
                        new_grid[i, j] = 1
            self.grid = new_grid
            self.cells_alive_label.config(text=f"Cells alive: {np.count_nonzero(self.grid)}")
            self.cells_dead_label.config(text=f"Cells dead: {self.grid_size**2 - np.count_nonzero(self.grid)}")
            self.generation_label.config(text=f"Generation: {self.anim.frame_seq[-1]+1}")
        
    def update(self, grid):
        self.im.set_data(grid)
        return [self.im]
        
    def start(self):
        if self.paused:
            self.anim.event_source.start()
            self.paused = False
            
    def pause(self):
        if not self.paused:
            self.anim.event_source.stop()
            self.paused = True
            
    def set_speed(self, speed):
        self.speed = int(speed)
        self.anim.event_source.interval = self.speed
            
    def reset(self):
        self.anim.event_source.stop()
        self.grid = np.zeros((self.grid_size, self.grid_size), dtype=np.uint8)
        self.im.set_data(self.grid)
        self.cells_alive_label.config(text="Cells alive: 0")
        self.cells_dead_label.config(text=f"Cells dead: {self.grid_size**2}")
        self.generation_label.config(text="Generation: 0")
        self.anim = animation.FuncAnimation(self.fig, self.update, frames=self.evolve, interval=self.speed, blit=False)
        self.paused = False
        
if __name__ == "__main__":
    root = tk.Tk()
    game = GameOfLife(root)
    root.mainloop()
