import os

class Tape:
    def __init__(self):
        self.tape = {}
        self.position = 0
        self.step_count = 0
        self.log_file = None
        self.log_filename = ""

    def load_tape(self, s):
        """Resets the tape, loads a new unary string, and opens a specific log file."""
        # Close any existing log file before starting a new one
        self.close_log()

        self.tape = {}
        self.position = 0
        self.step_count = 0
        
        # Create a specific filename for this input
        self.log_filename = f"log_{s}.txt"
        self.log_file = open(self.log_filename, "w")
        
        for i, c in enumerate(s):
            if c == "1":
                self.tape[i] = c
            else:
                raise ValueError("Invalid unary number")
        
        self._log_state(f"Input Loaded: {s}")

    def close_log(self):
        """Closes the log file if it is open."""
        if self.log_file:
            self.log_file.close()
            self.log_file = None

    def delete_log(self):
        """Closes and deletes the current log file."""
        self.close_log()
        if self.log_filename and os.path.exists(self.log_filename):
            os.remove(self.log_filename)

    def transition(self, r, w, direction):
        if self._read(r):
            self._write(w)
            if direction == "L":
                self._left()
            elif direction == "R":
                self._right()
            elif direction == "N":
                pass
            else: raise ValueError("direction is wrong")
            
            self._log_state(f"Transition: Read '{r}' -> Wrote '{w}' -> Moved {direction}")
            return True
        else:
            return False

    def move_not_value(self, r, direction):
        while not self._read(r):
            if direction == "L":
                self._left()
            elif direction == "R":
                self._right()
            else: raise ValueError("direction is wrong")
            self._log_state(f"Scanning: Moving {direction} looking for '{r}'")

    def _log_state(self, action):
        if self.log_file:
            entry = f"Step {self.step_count}: {action}\n{self}\n{'-' * 40}\n"
            self.log_file.write(entry)
            self.log_file.flush()
        self.step_count += 1

    def _read(self, r):
        symbol = self.tape.get(self.position, "_")
        return symbol == r

    def _write(self, w):
        if w == "_":
            self.tape.pop(self.position, None)
        else:
            self.tape[self.position] = w

    def _left(self):
        self.position -= 1

    def _right(self):
        self.position += 1

    def __str__(self):
        indices = list(self.tape.keys()) + [self.position]
        if not indices: return "Tape Empty"
        min_idx = min(indices)
        max_idx = max(indices)
        tape_str = ""
        cursor_str = ""
        for i in range(min_idx, max_idx + 1):
            tape_str += self.tape.get(i, "_")
            if i == self.position:
                cursor_str += "^"
            else:
                cursor_str += " "
        return f"{tape_str}\n{cursor_str}"


class Automaton(Tape):
    def init_workspace(self):
        self.transition("1", "$", "R")
        self.move_not_value("_", "R")
        self.transition("_", "#", "R")
        self.transition("_", "1", "L")
        self.move_not_value("$", "L")
        self.transition("$", "1", "R")
        while self.transition("1", "$", "R"):
            self.move_not_value("_", "R")
            self.transition("_", "1", "L")
            self.move_not_value("$", "L")
            self.transition("$", "1", "R")
        self.move_not_value("_", "R")
        self.transition("_", "_", "L")
        self.transition("1", "_", "L")
        self.move_not_value("#", "L")
        self.transition("#", "#", "R")
        self.transition("1", "%", "L")
        self.move_not_value("_", "L")
        self.transition("_", "_", "R")
        self.transition("1", "$", "N")

    def mod(self):
        self.transition("$", "1", "R")
        while self.transition("1", "$", "R"):
            self.move_not_value("%", "R")
            self.transition("%", "1", "R")
            if self.transition("_", "_", "L"):
                self.move_not_value("#", "L")
                self.transition("#", "#", "R")
                self.transition("1", "%", "L")
            else:
                self.transition("1", "%", "L")
            self.move_not_value("$", "L")
            self.transition("$", "1", "R")
        self.move_not_value("%", "R")
        self.transition("%", "1", "R")
        if self.transition("_", "_", "L"):
            return True 
        else:
            self.move_not_value("#", "L")
            self.transition("#", "#", "R")
            self.transition("1", "%", "L")
            self.move_not_value("_", "L")
            self.transition("_", "_", "R")
            self.transition("1", "$", "N")
            return False

    def check_and_subtract(self):
        self.move_not_value("_", "R")
        self.transition("_", "_", "L")
        self.transition("1", "_", "L")
        self.move_not_value("#", "L")
        self.transition("#", "#", "R") 
        self.transition("%", "%", "R")
        if self.transition("1", "1", "R"):
            self.move_not_value("$", "L")
            return False 
        else:
            return True 


def accept(A: Automaton, s: str):    
    try:
        # This will create log_{s}.txt
        A.load_tape(s)
    except ValueError as e:
        print(f"Error: {e}")
        return False

    A.init_workspace()
    
    # Run the Prime Checker Logic
    while not A.mod():
        if A.check_and_subtract():
            print("accept")
            A.close_log()
            return True       
    else:
        print("reject")
        A.delete_log()
        return False

if __name__ == "__main__":
    machine = Automaton()
    accept(machine, "1"*97)