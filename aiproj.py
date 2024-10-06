import tkinter as tk
from tkinter import filedialog, font
import matplotlib.pyplot as plt
import networkx as nx

class TSP:
    def __init__(self):
        self.graph = None
        self.cities = []
        self.distances = {}

    def load_graph(self, filepath):
        self.graph = nx.read_weighted_edgelist(filepath, nodetype=int)
        self.cities = list(self.graph.nodes)
        self.distances = nx.get_edge_attributes(self.graph, 'weight')

    def visualize(self):
        pos = nx.spring_layout(self.graph)
        nx.draw(self.graph, pos, with_labels=True, node_color='#a78bfa', node_size=700, font_size=10, font_color='white')
        labels = nx.get_edge_attributes(self.graph, 'weight')
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=labels, font_color='#f43f5e')
        plt.show()

    def is_valid_tour(self, tour):
        return set(tour) == set(self.cities) and len(tour) == len(self.cities)

    def calc_tour_cost(self, tour):
        if not self.is_valid_tour(tour):
            return float('inf')
        cost = 0
        for i in range(len(tour)):
            start, end = tour[i], tour[(i + 1) % len(tour)]
            if (start, end) in self.distances:
                cost += self.distances[(start, end)]
            elif (end, start) in self.distances:
                cost += self.distances[(end, start)]
        return cost

class TSPApp:
    def __init__(self, root):
        self.tsp = TSP()
        self.root = root
        self.root.title("TSP Solver")
        self.root.geometry("500x500")
        self.root.configure(bg="#f3e8ff")  # Light purple background

        # Custom fonts
        self.title_font = font.Font(family='Helvetica', size=16, weight='bold')
        self.button_font = font.Font(family='Helvetica', size=12)
        self.label_font = font.Font(family='Helvetica', size=10)

        # Frame for content
        self.frame = tk.Frame(self.root, bg="#f3e8ff")
        self.frame.pack(expand=True)

        # Title Label
        self.title = tk.Label(self.frame, text="TSP Solver", bg="#f3e8ff", fg="#2c2e33", font=self.title_font)
        self.title.pack(pady=20)

        # Upload TSP Graph File Button
        self.upload_graph_btn = tk.Button(self.frame, text="Upload TSP Graph File", command=self.upload_graph, bg="#6366f1", fg="white", font=self.button_font)
        self.upload_graph_btn.pack(pady=10)

        # Instruction Text for Heuristic File
        self.heuristic_instruction = tk.Label(self.frame, text="Upload a file containing Start Node, End Node, and Heuristic Value for each path.", bg="#f3e8ff", fg="#2c2e33", font=self.label_font)
        self.heuristic_instruction.pack(pady=5)

        # Visualize Button
        self.visualize_btn = tk.Button(self.frame, text="Visualize Graph", command=self.visualize_graph, state=tk.DISABLED, bg="#6366f1", fg="white", font=self.button_font)
        self.visualize_btn.pack(pady=10)

        # Tour Check
        self.tour_label = tk.Label(self.frame, text="Enter Tour (space-separated):", bg="#f3e8ff", fg="#2c2e33", font=self.label_font)
        self.tour_label.pack(pady=5)
        self.tour_entry = tk.Entry(self.frame, bg="#ffffff", fg="#1f2937", font=self.label_font)
        self.tour_entry.pack(pady=5)

        self.check_tour_btn = tk.Button(self.frame, text="Check Tour", command=self.check_tour, bg="#6366f1", fg="white", font=self.button_font)
        self.check_tour_btn.pack(pady=10)

        # Tour Cost Button
        self.cost_btn = tk.Button(self.frame, text="Calculate Tour Cost", command=self.calc_cost, bg="#6366f1", fg="white", font=self.button_font)
        self.cost_btn.pack(pady=10)

        # Output Label
        self.output = tk.Label(self.frame, text="", bg="#f3e8ff", fg="#2c2e33", font=self.label_font)
        self.output.pack(pady=10)

    def upload_graph(self):
        filepath = filedialog.askopenfilename(title="Select TSP Graph File", filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
        if filepath:
            self.tsp.load_graph(filepath)
            self.output.config(text="Graph uploaded successfully.")
            self.visualize_btn.config(state=tk.NORMAL)

    def visualize_graph(self):
        if self.tsp.graph:
            self.tsp.visualize()

    def check_tour(self):
        tour = list(map(int, self.tour_entry.get().split()))
        if self.tsp.is_valid_tour(tour):
            self.output.config(text="Valid Tour!")
        else:
            self.output.config(text="Invalid Tour!")

    def calc_cost(self):
        tour = list(map(int, self.tour_entry.get().split()))
        cost = self.tsp.calc_tour_cost(tour)
        if cost == float('inf'):
            self.output.config(text="Invalid tour, can't calculate cost.")
        else:
            self.output.config(text=f"Tour cost: {cost}")

# Run the GUI
root = tk.Tk()
app = TSPApp(root)
root.mainloop()
