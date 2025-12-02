# make tapes dicts and find ways to make sure you can do negative input
# this allows for infinite in the positive direction, assume any non real input is blank
input_tape = [1, 1, 1, 1, 1]
dup_tape = ['' for _ in range(len(input_tape))]
sr_tape = ['' for _ in range(len(input_tape))]
tmp_tape = ['' for _ in range(len(input_tape))]
pos_input = 0
pos_dup = 0
pos_sr = 0
pos_tmp = 0

# duplicate the input
def dup():
    global input_tape, dup_tape, sr_tape, tmp_tape, pos_input, pos_dup, pos_sr, pos_tmp
    while input_tape[pos_input] == 1 and pos_input < len(input_tape): # loop till head is not on a 1 and add 1s to the dup tape
        dup_tape[pos_dup] = 1
        pos_input += 1
        pos_dup += 1
    pos_dup -= 1

# sr the dup
def sr():
    global input_tape, dup_tape, sr_tape, tmp_tape, pos_input, pos_dup, pos_sr, pos_tmp
    while dup_tape[pos_dup] != '':
        # makes tmp_tape
        tmp_tape[pos_tmp] = 1 # starts at 1
        pos_tmp += 1
        while sr_tape[pos_sr] == 1: # adds 2 for every 1 in sr_tape
            if len(tmp_tape) - pos_tmp < 2:
                tmp_tape.append('')
                tmp_tape.append('')
            tmp_tape[pos_tmp] = 1
            pos_tmp += 1
            tmp_tape[pos_tmp] = 1
            pos_tmp += 1
            pos_sr += 1
        pos_sr -= 1
        while sr_tape[pos_sr] == 1 and pos_sr >= 0:
            pos_sr -= 1
        
        # subtract tmp_tape
        while sr_tape[pos_sr] == 1 and pos_sr < len(sr_tape) and pos_dup >= 0:
            dup_tape[pos_dup] = ''
            tmp_tape[pos_tmp] = ''
            pos_dup -= 1
            pos_tmp -= 1
            if pos_sr >= len(sr_tape):
                sr_tape.append('')
            sr_tape[pos_sr] = 1
            pos_sr += 1
    pos_sr -= 1

    # clear dup
    while pos_dup >= 0:
        dup_tape[pos_dup] = ''
        pos_dup -= 1

    dup() # recreate dup

# n mod m
def mod():
    global input_tape, dup_tape, sr_tape, tmp_tape, pos_input, pos_dup, pos_sr, pos_tmp
    while pos_dup >= 0:
        if (pos_sr < 0):
            while pos_sr < len(sr_tape):
                pos_sr += 1
        pos_dup -= 1 
        pos_sr -= 1

def main():
    global input_tape, dup_tape, sr_tape, tmp_tape, pos_input, pos_dup, pos_sr, pos_tmp
    dup()
    sr()
    while sr_tape[pos_sr] == '':
        mod()
        if pos_sr == 0: # check previous pos on the tape
            print("not a prime number")
            quit()
        else:
            while pos_sr <= len(sr_tape):
                pos_sr += 1
            sr_tape[pos_sr] = ''
            pos_sr -= 1
    print("prime")

main()