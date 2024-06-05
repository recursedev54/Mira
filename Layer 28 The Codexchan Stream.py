import os
import tkinter as tk
from tkinter import ttk

def print_clipped_tree(startpath):
    tree_structure = []
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * level
        tree_structure.append('{}{}'.format(indent, ''.join([word[0] for word in os.path.basename(root).split()])))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            tree_structure.append('{}{}'.format(subindent, ''.join([word[0] for word in f.split()])))
    return tree_structure

def display_tree_in_tkinter(tree_structure):
    root = tk.Tk()
    root.title("Directory Tree")
    root.attributes('-fullscreen', True)
    root.configure(bg='cyan')

    main_frame = ttk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=1)

    canvas = tk.Canvas(main_frame, bg='cyan')
    scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas, style="Custom.TFrame")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((root.winfo_screenwidth() // 2, 0), window=scrollable_frame, anchor="n")
    canvas.configure(yscrollcommand=scrollbar.set)

    style = ttk.Style()
    style.configure("Custom.TLabel", background="cyan", foreground="black", font=("Courier", 14))
    style.configure("Custom.TFrame", background="cyan")

    for line in tree_structure:
        label = ttk.Label(scrollable_frame, text=line, style="Custom.TLabel")
        label.pack(anchor='center')

    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Mousewheel scrolling
    def on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    root.bind_all("<MouseWheel>", on_mousewheel)

    # Auto-scrolling
    def auto_scroll():
        canvas.yview_scroll(1, 'units')
        root.after(100, auto_scroll)

    root.after(100, auto_scroll)

    root.bind("<Escape>", lambda e: root.destroy())

    root.mainloop()

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current script
    tree_structure = print_clipped_tree(base_dir)
    display_tree_in_tkinter(tree_structure)
