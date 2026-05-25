import os
import time
import sys
import random
import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog, scrolledtext


# Node class for Trie Tree (DSA - Trie Node)

class Node:
    def __init__(self):
        self.children = [None] * 26  # Each node can have 26 children (for a-z)
        self.is_end_of_word = False  # Marks the end of a valid word


# WordTree class representing Trie (DSA - Trie)

class WordTree:
    def __init__(self):
        self.root = Node()
        self.total_words = 0

    # DSA: Trie Insertion
    def insert(self, word):
        node = self.root
        for char in word.lower():
            if not char.isalpha():
                continue
            index = ord(char) - ord('a')  # Mapping a-z to 0-25
            if not node.children[index]:
                node.children[index] = Node()  # Create new node if path doesn't exist
            node = node.children[index]
        if not node.is_end_of_word:
            node.is_end_of_word = True
            self.total_words += 1

    # DSA: Trie Deletion using Recursion
    def delete(self, word):
        def _delete(node, word, depth):
            if not node:
                return False
            if depth == len(word):
                if node.is_end_of_word:
                    node.is_end_of_word = False
                    # If no children, node can be deleted
                    return all(child is None for child in node.children)
                return False
            index = ord(word[depth]) - ord('a')
            if _delete(node.children[index], word, depth + 1):
                node.children[index] = None
                # If current node is not end of another word and has no children, delete it
                return not node.is_end_of_word and all(child is None for child in node.children)
            return False
        _delete(self.root, word.lower(), 0)

    # DSA: Combination of deletion + insertion = update
    def update(self, old_word, new_word):
        self.delete(old_word)
        self.insert(new_word)

    # DSA: Recursive DFS search to collect all words starting with given letter
    def search_by_letter(self, node, letter, path, level, results):
        if node.is_end_of_word:
            word = ''.join(path[:level])
            if word.startswith(letter.lower()):
                results.append(word)
        for i in range(26):
            if node.children[i]:
                path[level] = chr(i + ord('a'))
                self.search_by_letter(node.children[i], letter, path, level + 1, results)

    # Wrapper for collecting words that start with a specific letter
    def get_words_starting_with(self, letter):
        results = []
        path = [''] * 50  # Used for backtracking the path
        self.search_by_letter(self.root, letter, path, 0, results)
        return results

    # Collect all words from Trie
    def get_all_words(self):
        results = []
        self.search_by_letter(self.root, '', [''] * 50, 0, results)
        return sorted(results)  # DSA: Sorting applied to words list

    # DSA: Frequency count by letter (Basic Hash Mapping)
    def get_word_count_by_letter(self):
        counts = {}
        for c in range(26):
            letter = chr(c + ord('a'))
            words = self.get_words_starting_with(letter)
            counts[letter] = len(words)
        return counts

# ------------------------
# GUI and Application Logic
# ------------------------
class WordPuzzleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Word Guesser Tool")
        self.root.geometry("900x700")
        self.root.configure(bg="#f0f4f7")
        self.tree = WordTree()  # Our Trie-based DSA object
        self.word_list = []     # Linear list (DS) to keep raw words for random puzzle
        self.filename = "unsorted.txt"
        self.setup_gui()

    def setup_gui(self):
        self.frame = tk.Frame(self.root, bg="#f0f4f7", padx=20, pady=20)
        self.frame.pack(fill='both', expand=True)

        title = tk.Label(self.frame, text="Word Finder", font=("Helvetica", 22, "bold"), bg="#f0f4f7", fg="#2c3e50")
        title.pack(pady=10)

        search_label = tk.Label(self.frame, text="Type to Search:", font=("Arial", 12, "bold"), bg="#f0f4f7")
        search_label.pack(pady=(10, 0))

        self.search_entry = tk.Entry(self.frame, font=("Arial", 12), width=30)
        self.search_entry.pack(pady=5)
        self.search_entry.bind("<KeyRelease>", self.search_by_typing)

        btn_frame = tk.Frame(self.frame, bg="#f0f4f7")
        btn_frame.pack(pady=10)

        btns = [
            ("Load Words File", self.load_words_gui),
            ("Insert New Word", self.insert_word),
            ("Delete Word", self.delete_word),
            ("Update Word", self.update_word),
            ("Search Words by Letter", self.search_by_letter),
            ("Display All Words", self.display_all_words),
            ("Word Count Summary", self.word_count_summary),
            ("Play Random Puzzle", self.random_puzzle),
            ("Sort and Save File", self.sort_and_save_file),
            ("Exit", self.root.quit)
        ]

        for i, (txt, cmd) in enumerate(btns):
            tk.Button(btn_frame, text=txt, command=cmd, width=28, height=2, bg="#3498db", fg="white", font=("Arial", 10, "bold"), bd=0, relief="flat", activebackground="#2980b9").grid(row=i//2, column=i%2, padx=10, pady=6)

        self.output = scrolledtext.ScrolledText(self.frame, height=20, font=("Consolas", 12), wrap='word', bg="white", fg="black")
        self.output.pack(pady=20, fill='both', expand=True)

    def load_words_gui(self):
        filename = filedialog.askopenfilename(title="Select word file", filetypes=[("Text files", "*.txt")])
        if filename:
            try:
                with open(filename, 'r') as file:
                    for line in file:
                        word = line.strip()
                        if word.isalpha():
                            self.tree.insert(word)       # DSA: Insert into Trie
                            self.word_list.append(word)  # DS: Append into List
                self.output.insert(tk.END, f"Loaded words from {filename}\n")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def insert_word(self):
        word = simpledialog.askstring("Insert Word", "Enter new word:")
        if word and word.isalpha():
            self.tree.insert(word)       # DSA: Insert into Trie
            self.word_list.append(word)  # DS: Append into List
            with open(self.filename, "a") as f:
                f.write(word + "\n")
            self.output.insert(tk.END, f"Inserted '{word}'\n")
        else:
            messagebox.showerror("Invalid Input", "Only alphabets allowed.")

    def delete_word(self):
        word = simpledialog.askstring("Delete Word", "Enter word to delete:")
        if word and word.isalpha():
            self.tree.delete(word)  # DSA: Delete using recursive Trie traversal
            self.output.insert(tk.END, f"Deleted '{word}' if it existed\n")

    def update_word(self):
        old = simpledialog.askstring("Update Word", "Enter old word:")
        new = simpledialog.askstring("Update Word", "Enter new word:")
        if old and new and old.isalpha() and new.isalpha():
            self.tree.update(old, new)  # DSA: Update = delete + insert
            with open(self.filename, "a") as f:
                f.write(new + "\n")
            self.output.insert(tk.END, f"Updated '{old}' to '{new}'\n")

    def search_by_letter(self):
        letter = simpledialog.askstring("Search", "Enter starting letter:")
        if letter and len(letter) == 1 and letter.isalpha():
            results = self.tree.get_words_starting_with(letter.lower())  # DSA: Trie prefix search
            formatted = '\n'.join([f"{i+1}. {w}" for i, w in enumerate(results)])
            self.output.insert(tk.END, f"Words starting with '{letter}':\n{formatted}\n")

    def display_all_words(self):
        words = self.tree.get_all_words()  # DSA: DFS traversal
        formatted = '\n'.join([f"{i+1}. {w}" for i, w in enumerate(words)])
        self.output.insert(tk.END, f"\nAll Words:\n{formatted}\n")

    def word_count_summary(self):
        counts = self.tree.get_word_count_by_letter()  # DSA: Frequency count via Trie
        summary = "\n".join(f"{k.upper()}: {v}" for k, v in counts.items() if v > 0)
        self.output.insert(tk.END, f"\nWord Count Summary:\n{summary}\n")

    def sort_and_save_file(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                words = sorted(word.strip() for word in f if word.strip())  # DSA: Sorting
            with open("Sorted.txt", "w") as f:
                for w in words:
                    f.write(w + "\n")
            self.output.insert(tk.END, "Words sorted and saved to 'Sorted.txt'\n")
        else:
            messagebox.showerror("File Error", f"'{self.filename}' not found.")

    def random_puzzle(self):
        if not self.word_list:
            self.output.insert(tk.END, "No words loaded for puzzle.\n")
            return
        word = random.choice(self.word_list)  # DS: Random pick from list
        scrambled = ''.join(random.sample(word, len(word)))  # DSA: Shuffle letters (Permutation)
        guess = simpledialog.askstring("Puzzle", f"Unscramble this: {scrambled}")
        if guess == word:
            messagebox.showinfo("Correct!", "\u2705 You guessed it!")
        else:
            messagebox.showinfo("Wrong", f"\u274C Correct word was: {word}")

    def search_by_typing(self, event=None):
        query = self.search_entry.get().lower()
        if not query.isalpha():
            return

        results = []
        all_words = self.tree.get_all_words()  # DSA: Trie traversal to get all words
        for word in all_words:
            if word.startswith(query):        # DSA: Prefix match
                results.append(word)

        self.output.delete(1.0, tk.END)
        if results:
            formatted = '\n'.join([f"{i+1}. {w}" for i, w in enumerate(results)])
            self.output.insert(tk.END, f"Words starting with '{query}':\n{formatted}\n")
        else:
            self.output.insert(tk.END, f"No words found starting with '{query}'\n")

# Main app launcher
if __name__ == "__main__":
    root = tk.Tk()
    app = WordPuzzleApp(root)
    root.mainloop()
