import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.patches as patches
from fractions import Fraction
import matplotlib.pyplot as plt

class App:
    def __init__(self, root):
        self.root = root
        self.root.title('Operation de Fractions')
        self.root.geometry('1200x600')  # Adjusted for better layout

        self.simplify = tk.BooleanVar(value=True)  # Variable to toggle simplification

        # Frame for operations
        operation_frame = tk.Frame(root)
        operation_frame.pack(side=tk.TOP, pady=10)

        # Frame for single fraction and percentage inputs
        input_frame = tk.Frame(root)
        input_frame.pack(side=tk.TOP, pady=10)

        # Simplification checkbox
        self.simplify_check = tk.Checkbutton(input_frame, text="Simplifier les fractions", var=self.simplify, onvalue=True, offvalue=False)
        #self.simplify_check.pack(side=tk.LEFT)

        # Operation inputs
        self.label_fraction1 = tk.Label(operation_frame, text="Entrez la première fraction (ex. : 1/4):")
        self.label_fraction1.pack(side=tk.LEFT)
        self.entry_fraction1 = tk.Entry(operation_frame, width=5)
        self.entry_fraction1.pack(side=tk.LEFT)

        self.label_fraction2 = tk.Label(operation_frame, text="Entrez la deuxième fraction (ex. : 3/5):")
        self.label_fraction2.pack(side=tk.LEFT)
        self.entry_fraction2 = tk.Entry(operation_frame, width=5)
        self.entry_fraction2.pack(side=tk.LEFT)

        self.operation = tk.StringVar(value="addition")
        self.oper_menu = ttk.Combobox(operation_frame, textvariable=self.operation, values=("addition", "soustraction"), width=10)
        self.oper_menu.pack(side=tk.LEFT)

        self.button_operate = tk.Button(operation_frame, text="Effectuer l'opération", command=self.perform_operation)
        self.button_operate.pack(side=tk.LEFT)

        # # Single fraction input
        # self.label_single_fraction = tk.Label(input_frame, text="Entrez une fraction (ex. : 3/6):")
        # self.label_single_fraction.pack(side=tk.LEFT)
        # self.entry_single_fraction = tk.Entry(input_frame, width=5)
        # self.entry_single_fraction.pack(side=tk.LEFT)
        # self.button_single_fraction = tk.Button(input_frame, text="Montrer la Fraction", command=self.show_single_fraction)
        # self.button_single_fraction.pack(side=tk.LEFT)

        # # Percentage input
        # self.label_percentage = tk.Label(input_frame, text="Entrez un pourcentage (ex. : 40):")
        # self.label_percentage.pack(side=tk.LEFT)
        # self.entry_percentage = tk.Entry(input_frame, width=5)
        # self.entry_percentage.pack(side=tk.LEFT)
        # self.button_percentage = tk.Button(input_frame, text="Montrer le Pourcentage", command=self.show_percentage)
        # self.button_percentage.pack(side=tk.LEFT)

        self.canvas = None

    def perform_operation(self):
        frac1 = self.entry_fraction1.get()
        frac2 = self.entry_fraction2.get()
        operation = self.operation.get()
        try:
            frac1 = Fraction(*map(int, frac1.split('/')))
            frac2 = Fraction(*map(int, frac2.split('/')))
            if operation == "addition":
                result = frac1 + frac2
            else:
                result = frac1 - frac2
            if not self.simplify.get():
                result = Fraction(result.numerator, result.denominator)  # Forces the display to show unsimplified fraction
            self.visualize_operation(frac1, frac2, result, operation)
        except ValueError:
            print("Veuillez entrer des fractions valides sous la forme numérateur/dénominateur")

    def show_single_fraction(self):
        frac_input = self.entry_single_fraction.get()
        try:
            frac = Fraction(*map(int, frac_input.split('/')))
            if not self.simplify.get():
                frac = Fraction(frac.numerator, frac.denominator)  # Forces the display to show the fraction unsimplified
            figure = self.draw_fraction(frac)
            self.update_canvas(figure)
        except ValueError:
            print("Veuillez entrer une fraction valide sous la forme numérateur/dénominateur")

    def show_percentage(self):
        try:
            percentage = float(self.entry_percentage.get()) / 100
            figure = self.draw_circle(percentage)
            self.update_canvas(figure)
        except ValueError:
            print("Veuillez entrer un nombre valide")

    def visualize_operation(self, frac1, frac2, result, operation):
        figure = Figure(figsize=(10, 4), dpi=100)
        subplot1 = figure.add_subplot(131)
        subplot2 = figure.add_subplot(132)
        subplot3 = figure.add_subplot(133)

        self.draw_fraction_subplot(subplot1, frac1, f"{frac1.numerator}/{frac1.denominator}")
        operation_symbol = '+' if operation == "addition" else '-'
        self.draw_fraction_subplot(subplot2, frac2, f"{frac2.numerator}/{frac2.denominator}")
        self.draw_fraction_subplot(subplot3, result, f"{result.numerator}/{result.denominator}", operation_symbol)

        self.update_canvas(figure)

    def draw_fraction_subplot(self, subplot, fraction, label, operation_symbol=None):
        subplot.axis('equal')
        full_circle = plt.Circle((0.5, 0.5), 0.5, edgecolor='black', facecolor='lightgray')
        subplot.add_artist(full_circle)

        angle_per_segment = 360 / fraction.denominator
        num_segments = fraction.numerator
        for i in range(fraction.denominator):
            start_angle = i * angle_per_segment
            end_angle = start_angle + angle_per_segment
            color = 'blue' if i < num_segments else 'none'
            wedge = patches.Wedge(center=(0.5, 0.5), r=0.5, theta1=start_angle, theta2=end_angle, facecolor=color, edgecolor='black')
            subplot.add_patch(wedge)

        subplot.text(0.5, 0.1, label, ha='center', va='center', fontsize=12, color='white')
        if operation_symbol:
            subplot.text(-3.0, 0.5, operation_symbol, ha='center', va='center', fontsize=18, color='red')
            subplot.text(-0.8, 0.5, '=', ha='center', va='center', fontsize=18, color='red')

        subplot.set_xlim(0, 2)
        subplot.set_ylim(0, 1)
        subplot.axis('off')

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
