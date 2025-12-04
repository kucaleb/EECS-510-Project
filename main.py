# This file is meant to simulate a Turing machine that determines if a unary input is prime.
# The machine is not meant to be efficient, just simple. Therefore there will not be many tricks to cut down on the computation.

# Tape represents a Turing machine tape. Several functions are included to simulate the behavior of a turing machine on its tape.
class Tape:
    def __init__(self):
        self.tape = {}
        self.position = 0
        self.step_count = 0
        
        # Open a log file for writing
        self.log_file = open("turing_log.txt", "w")
        
        num = input("Enter a number in unary: ")
        for i, c in enumerate(num):
            if c == "1":
                self.tape[i] = c
            else:
                raise ValueError("Invalid unary number")
        
        # Log the starting state
        self._log_state("Initial State")

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
            
            # Log successful transition
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
            
            # Log every scan step
            self._log_state(f"Scanning: Moving {direction} looking for '{r}'")

    def _log_state(self, action):
        """Writes the current state to the log file."""
        # construct the log entry string
        entry = f"Step {self.step_count}: {action}\n{self}\n{'-' * 40}\n"
        
        # Write to file
        self.log_file.write(entry)
        
        # Force write to disk immediately (helpful if script crashes)
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

tape = Tape()

# initialize the tape to the proper working condition (n#m) where n in the input in unary and m is n - 1
# ex. $...1#%...1
# you can assume that the tape only has n on it and the head is at the beginning of n
def init_workspace():
    global tape
    # start with setting the marker in n
    tape.transition("1", "$", "R")

    # go to where n is and start to create it
    tape.move_not_value("_", "R")
    tape.transition("_", "#", "R")
    tape.transition("_", "1", "L")
    
    # go back to the start of n
    tape.move_not_value("$", "L")

    # move the marker 1
    tape.transition("$", "1", "R")

    # start loop to make m = n - 1
    while tape.transition("1", "$", "R"):
        tape.move_not_value("_", "R")
        tape.transition("_", "1", "L")
        tape.move_not_value("$", "L")
        tape.transition("$", "1", "R")
    
    # should be at # by now
    # subtract 1 from m
    tape.move_not_value("_", "R")
    tape.transition("_", "_", "L")
    tape.transition("1", "_", "L")

    # go to the delimeter
    tape.move_not_value("#", "L")

    # set up the m marker
    tape.transition("#", "#", "R")
    tape.transition("1", "%", "L")

    # move back to start of n
    tape.move_not_value("_", "L")
    tape.transition("_", "_", "R")
    tape.transition("1", "$", "N")

# n mod m
# given the read/write head is at the $ and the tape is formatted like $...1#1...1
# given that n > m
# $ is the placeholder variable for n
# returns true if n % m == 0
# else return false
def mod():
    global tape
    tape.transition("$", "1", "R")
    
    # loop till $ is at the end of n
    while tape.transition("1", "$", "R"):
        # move %
        tape.move_not_value("%", "R")
        tape.transition("%", "1", "R")

        if tape.transition("_", "_", "L"):
            # if we are at a blank loop back to beginning of m
            tape.move_not_value("#", "L")
            tape.transition("#", "#", "R")
            tape.transition("1", "%", "L")
        else:
            # else just move it
            tape.transition("1", "%", "L")
        # move to $ and move it
        tape.move_not_value("$", "L")
        tape.transition("$", "1", "R")

    # should be at #
    # check if % is at the end
    tape.move_not_value("%", "R")
    tape.transition("%", "1", "R")
    if tape.transition("_", "_", "L"):
        return True # the machine is done
    else:
        # clean up $ and %
        tape.move_not_value("#", "L")
        tape.transition("#", "#", "R")
        tape.transition("1", "%", "L")
        tape.move_not_value("_", "L")
        tape.transition("_", "_", "R")
        tape.transition("1", "$", "N")
        return False
    
# subtracts 1 from m
# checks if m > 2
# if m <= 2 return true
# else return false
# given the head is at $
def check_and_subtract():
    global tape
    # subtract 1 from m
    tape.move_not_value("_", "R")
    tape.transition("_", "_", "L")
    tape.transition("1", "_", "L")

    # move to #
    tape.move_not_value("#", "L")
    tape.transition("#", "#", "R")

    # checking that m > 1
    tape.transition("%", "%", "R")
    if tape.transition("1", "1", "R"):
        tape.move_not_value("$", "L")
        return False
    else:
        return True # the machine is done

def main():
    global tape
    init_workspace()
    while not mod():
        if check_and_subtract():
            print("Your input is a prime number")
            break
    else:
        print("Your input is not a prime number")

main()