import json
import sys
import re

def load_board():
    try:
        with open('board_state.json', 'r') as f:
            return json.load(f)
    except:
        # Initial board position
        return {
            'turn': 'white',
            'history': [],
            'board': {
                '8': {'A': '♜', 'B': '♞', 'C': '♝', 'D': '♛', 'E': '♚', 'F': '♝', 'G': '♞', 'H': '♜'},
                '7': {'A': '♟', 'B': '♟', 'C': '♟', 'D': '♟', 'E': '♟', 'F': '♟', 'G': '♟', 'H': '♟'},
                '6': {'A': '', 'B': '', 'C': '', 'D': '', 'E': '', 'F': '', 'G': '', 'H': ''},
                '5': {'A': '', 'B': '', 'C': '', 'D': '', 'E': '', 'F': '', 'G': '', 'H': ''},
                '4': {'A': '', 'B': '', 'C': '', 'D': '', 'E': '', 'F': '', 'G': '', 'H': ''},
                '3': {'A': '', 'B': '', 'C': '', 'D': '', 'E': '', 'F': '', 'G': '', 'H': ''},
                '2': {'A': '♙', 'B': '♙', 'C': '♙', 'D': '♙', 'E': '♙', 'F': '♙', 'G': '♙', 'H': '♙'},
                '1': {'A': '♖', 'B': '♘', 'C': '♗', 'D': '♕', 'E': '♔', 'F': '♗', 'G': '♘', 'H': '♖'}
            }
        }

def save_board(board_state):
    with open('board_state.json', 'w') as f:
        json.dump(board_state, f, indent=2)

def update_readme(board_state):
    with open('README.md', 'r') as f:
        content = f.read()
    
    # Build board table
    board_table = "|     | A | B | C | D | E | F | G | H |\n"
    board_table += "|-----|---|---|---|---|---|---|---|---|\n"
    
    for row in ['8', '7', '6', '5', '4', '3', '2', '1']:
        board_table += f"| **{row}** |"
        for col in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']:
            piece = board_state['board'][row][col]
            board_table += f" {piece if piece else ' '} |"
        board_table += "\n"
    
    # Update the board section
    pattern = r'(\|[\s\S]*?\|\s*\n\s*\|\s*8\s*\|[\s\S]*?\|\s*1\s*\|)'
    content = re.sub(pattern, board_table.rstrip('\n'), content)
    
    # Update turn indicator
    turn_text = "🟡 White's Turn" if board_state['turn'] == 'white' else "⚫ Black's Turn"
    content = re.sub(r'Current Turn:.*', f'Current Turn: {turn_text}', content)
    
    # Update move history
    history_html = "<details>\n<summary><b>📜 Move History</b></summary>\n\n"
    if board_state['history']:
        for move in board_state['history'][-10:]:
            history_html += f"- {move}\n"
    else:
        history_html += "- Game started!\n"
    history_html += "\n</details>"
    
    content = re.sub(r'<details>[\s\S]*?</details>', history_html, content)
    
    with open('README.md', 'w') as f:
        f.write(content)

def parse_move(title, body):
    # Extract move from issue title or body
    match = re.search(r'Move ([A-H][1-8]) to ([A-H][1-8])', f"{title} {body}")
    if match:
        return match.group(1), match.group(2)
    return None, None

def main():
    if len(sys.argv) < 3:
        print("No move provided")
        return
    
    title = sys.argv[1]
    body = sys.argv[2] if len(sys.argv) > 2 else ""
    
    from_sq, to_sq = parse_move(title, body)
    
    if not from_sq or not to_sq:
        print("Invalid move format")
        return
    
    board_state = load_board()
    
    # Parse squares
    from_col = from_sq[0]
    from_row = from_sq[1]
    to_col = to_sq[0]
    to_row = to_sq[1]
    
    piece = board_state['board'][from_row][from_col]
    
    if not piece:
        print(f"No piece at {from_sq}")
        return
    
    # Check if it's correct turn
    is_white_piece = piece in ['♙', '♖', '♘', '♗', '♕', '♔']
    if (is_white_piece and board_state['turn'] != 'white') or (not is_white_piece and board_state['turn'] != 'black'):
        print(f"Not {board_state['turn']}'s turn!")
        return
    
    # Make the move
    board_state['board'][to_row][to_col] = piece
    board_state['board'][from_row][from_col] = ''
    
    # Record move
    move_text = f"{piece} from {from_sq} to {to_sq} ({board_state['turn']})"
    board_state['history'].append(move_text)
    
    # Change turn
    board_state['turn'] = 'black' if board_state['turn'] == 'white' else 'white'
    
    # Save and update
    save_board(board_state)
    update_readme(board_state)
    
    print(f"Move processed: {move_text}")

if __name__ == "__main__":
    main()