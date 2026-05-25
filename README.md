# Word Finder Project with Puzzle Tool 

An interactive, performance-oriented desktop application built in Python using Tkinter. At its core, the application implements a custom **Trie Data Structure** from scratch to manage dictionary words efficiently, allowing sub-millisecond prefix searches and real-time autocomplete results as you type.

## Core Data Structures & Algorithms (DSA)

Instead of relying on basic linear lookups, this project explores key algorithmic concepts:
* **Trie (Prefix Tree):** Optimized for memory and fast retrieval. Each letter maps dynamically via an alphabet index array (`a-z`).
* **Recursive DFS Traversals:** Leveraged for custom prefix matching, alphabet frequency analysis, and alphabetical word collection.
* **Trie Deletion with Backtracking:** Implements a clean, recursive deletion mechanism that trims unneeded nodes without losing shared path prefixes.
* **String Permutations:** Powers an integrated mini-game by generating randomized anagram shuffles for user puzzles.

##  Features

* **Real-Time Autocomplete:** Type in the live search bar to get instant matching suggestions as you press keys.
* **File Processing:** Load raw word files (`.txt`), process them into the Trie, or organize and export them cleanly into sorted dictionary files.
* **Full CRUD on Trie:** Graphically insert, delete, and update dictionary entries on the fly.
* **Analytics Engine:** Generates a quick data summary mapping alphabetical distribution across your current word bank.
* **Mini-Game Mode:** Includes an algorithmic scrambled-word puzzle generator to test vocabulary.

## Tech Stack

* **Language:** Python 3.x
* **GUI Framework:** Tkinter (Standard Library)
* **Algorithmic Base:** Native OOP-based Trie Data Structure (No external heavy dependencies)
