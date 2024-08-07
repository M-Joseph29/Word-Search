import tkinter as tk
import random
import string

# Define constants
GRID_SIZE = 10
DIRECTIONS = [(0, 1), (1, 0), (1, 1), (-1, 1)]  # Right, Down, Down-Right, Up-Right

def create_grid(size):
    return [[' ' for _ in range(size)] for _ in range(size)]

def can_place_word(grid, word, row, col, direction):
    d_row, d_col = direction
    end_row = row + d_row * (len(word) - 1)
    end_col = col + d_col * (len(word) - 1)
    
    if end_row < 0 or end_row >= len(grid) or end_col < 0 or end_col >= len(grid[0]):
        return False
    
    for i in range(len(word)):
        r, c = row + d_row * i, col + d_col * i
        if grid[r][c] not in (' ', word[i]):
            return False
            
    return True

def place_word(grid, word, row, col, direction):
    d_row, d_col = direction
    for i in range(len(word)):
        r, c = row + d_row * i, col + d_col * i
        grid[r][c] = word[i]

def fill_grid(grid):
    letters = string.ascii_uppercase
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == ' ':
                grid[row][col] = random.choice(letters)

def add_word_to_grid(grid, word):
    random.shuffle(DIRECTIONS)
    for direction in DIRECTIONS:
        for _ in range(100):  # Try up to 100 times to place the word
            row = random.randint(0, len(grid) - 1)
            col = random.randint(0, len(grid[0]) - 1)
            if can_place_word(grid, word, row, col, direction):
                place_word(grid, word, row, col, direction)
                return True
    return False

def generate_word_search(words):
    grid = create_grid(GRID_SIZE)
    
    for word in words:
        if not add_word_to_grid(grid, word):
            print(f"Could not place word: {word}")
    
    fill_grid(grid)
    return grid

class WordSearchGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Word Search Game")
        self.grid_size = GRID_SIZE
        
        self.word_entry = tk.Entry(self, width=50)
        self.word_entry.pack(pady=10)
        
        self.generate_button = tk.Button(self, text="Generate", command=self.generate_grid)
        self.generate_button.pack(pady=5)
        
        self.grid_frame = tk.Frame(self)
        self.grid_frame.pack(pady=10)
        
        self.grid_labels = []

    def generate_grid(self):
        words = self.word_entry.get().strip().upper().split()
        grid = generate_word_search(words)
        
        # Clear previous grid
        for widget in self.grid_frame.winfo_children():
            widget.destroy()
        
        self.grid_labels = []
        for r, row in enumerate(grid):
            row_labels = []
            for c, letter in enumerate(row):
                label = tk.Label(self.grid_frame, text=letter, padx=5, pady=5, borderwidth=1, relief="solid", width=3)
                label.grid(row=r, column=c)
                row_labels.append(label)
            self.grid_labels.append(row_labels)

if __name__ == "__main__":
    app = WordSearchGame()
    app.mainloop()
