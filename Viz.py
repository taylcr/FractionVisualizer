import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.patches as patches
import numpy as np
import matplotlib.pyplot as plt

class App:
    def __init__(self, root):
        self.root = root
        self.root.title('Fraction Viz ')

         # Set a fixed window size
        self.root.geometry('1200x600')  # Width x Height in pixels

        # Fraction input
        self.label_fraction = tk.Label(root, text="Entre une fraction (e.g., 3/6):")
        self.label_fraction.pack()

        self.entry_fraction = tk.Entry(root)
        self.entry_fraction.pack()

        self.button_fraction = tk.Button(root, text="Montre Fraction", command=self.show_fraction)
        self.button_fraction.pack()

        # Percentage input
        self.label_percentage = tk.Label(root, text="Entre une Pourcentage (e.g., 40):")
        self.label_percentage.pack()

        self.entry_percentage = tk.Entry(root)
        self.entry_percentage.pack()

        self.button_percentage = tk.Button(root, text="Montre Pourcentage", command=self.show_percentage)
        self.button_percentage.pack()

        self.canvas = None

    def show_fraction(self):
        fraction_input = self.entry_fraction.get()
        try:
            numerator, denominator = map(int, fraction_input.split('/'))
            figure = self.draw_fraction(numerator, denominator)
            self.update_canvas(figure)
        except ValueError:
            print("Entre une fraction : Numerateur/ Denominateur")

    def show_percentage(self):
        try:
            percentage = float(self.entry_percentage.get()) / 100
            figure = self.draw_circle(percentage)
            self.update_canvas(figure)
        except ValueError:
            print("Stp entre un chiffre valide :) ")

    def draw_fraction(self, numerator, denominator):
        figure = Figure(figsize=(6, 6), dpi=100)
        subplot = figure.add_subplot(111)
        subplot.axis('equal')

        full_circle = plt.Circle((0.5, 0.5), 0.5, edgecolor='black', facecolor='lightgray')
        subplot.add_artist(full_circle)

        angle_per_segment = 360 / denominator
        for i in range(denominator):
            start_angle = i * angle_per_segment
            end_angle = start_angle + angle_per_segment
            color = 'blue' if i < numerator else 'none'
            wedge = patches.Wedge(center=(0.5, 0.5), r=0.5, theta1=start_angle, theta2=end_angle, facecolor=color, edgecolor='black')
            subplot.add_patch(wedge)

        subplot.set_xlim(0, 1)
        subplot.set_ylim(0, 1)
        subplot.axis('off')

        return figure

    def draw_circle(self, percentage):
        figure = Figure(figsize=(6, 6), dpi=100)
        subplot = figure.add_subplot(111)
        subplot.axis('equal')

        full_circle = plt.Circle((0.5, 0.5), 0.5, edgecolor='black', facecolor='lightgray')
        subplot.add_artist(full_circle)

        angle = percentage * 360
        wedge = patches.Wedge(center=(0.5, 0.5), r=0.5, theta1=0, theta2=angle, color='blue')
        subplot.add_patch(wedge)

        subplot.set_xlim(0, 1)
        subplot.set_ylim(0, 1)
        subplot.axis('off')

        return figure

    def update_canvas(self, figure):
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
        self.canvas = FigureCanvasTkAgg(figure, master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
