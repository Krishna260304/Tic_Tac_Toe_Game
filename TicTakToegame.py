import tkinter as tk
import random

def check_winner():
    global winner
    for combo in [[0,1,2], [3,4,5], [6,7,8], [0,3,6], [1,4,7], [2,5,8], [0,4,8], [2,4,6]]:
        if buttons[combo[0]]["text"] == buttons[combo[1]]["text"] == buttons[combo[2]]["text"] != "":
            for i in combo:
                buttons[i].config(bg="green")
            winner = True
            show_result_popup(f"Player {buttons[combo[0]]['text']} wins!")
            return
    if all(button["text"] != "" for button in buttons) and not winner:
        winner = True
        show_result_popup("It's a tie!")

def button_click(index):
    global winner
    if buttons[index]["text"] == "" and not winner:
        buttons[index]["text"] = "X"
        check_winner()
        if not winner:
            toggle_player()
            root.after(500, ai_move)

def toggle_player():
    global current_player
    current_player = "X" if current_player == "O" else "O"
    label.config(text=f"Player {current_player}'s turn")

def ai_move():
    global winner
    if winner:
        return
    move = find_best_move()
    if move is not None:
        buttons[move]["text"] = "O"
        check_winner()
        if not winner:
            toggle_player()

def is_winning_move(index, symbol):
    buttons[index]["text"] = symbol
    for combo in [[0,1,2], [3,4,5], [6,7,8], [0,3,6], [1,4,7], [2,5,8], [0,4,8], [2,4,6]]:
        if buttons[combo[0]]["text"] == buttons[combo[1]]["text"] == buttons[combo[2]]["text"] == symbol:
            buttons[index]["text"] = ""
            return True
    buttons[index]["text"] = ""
    return False

def find_best_move():
    for i in range(9):
        if buttons[i]["text"] == "":
            if is_winning_move(i, "O"):
                return i
    for i in range(9):
        if buttons[i]["text"] == "":
            if is_winning_move(i, "X"):
                return i
    if buttons[4]["text"] == "":
        return 4
    available = [i for i in range(9) if buttons[i]["text"] == ""]
    return random.choice(available) if available else None

def reset_game():
    global winner, current_player
    for button in buttons:
        button.config(text="", bg="SystemButtonFace")
    winner = False
    current_player = "X"
    label.config(text=f"Player {current_player}'s turn")

def stop_game():
    root.destroy()

def show_result_popup(message):
    popup = tk.Toplevel()
    popup.title("Game Over")
    popup.geometry("250x120")
    popup.resizable(False, False)

    msg = tk.Label(popup, text=message, font=("normal", 14))
    msg.pack(pady=10)

    btn_frame = tk.Frame(popup)
    btn_frame.pack(pady=5)

    reset_btn = tk.Button(btn_frame, text="Play Again", width=10, command=lambda: [popup.destroy(), reset_game()])
    reset_btn.pack(side=tk.LEFT, padx=5)

    stop_btn = tk.Button(btn_frame, text="Stop Game", width=10, command=stop_game)
    stop_btn.pack(side=tk.LEFT, padx=5)

root = tk.Tk()
root.title("Tic-Tac-Toe (Player vs AI)")

buttons = [tk.Button(root, text="", font=("normal", 25), width=6, height=2,
                     command=lambda i=i: button_click(i)) for i in range(9)]

for i, button in enumerate(buttons):
    button.grid(row=i // 3, column=i % 3)

current_player = "X"
winner = False
label = tk.Label(root, text=f"Player {current_player}'s turn", font=("normal", 16))
label.grid(row=3, column=0, columnspan=3)

root.mainloop()