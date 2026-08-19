import sys

def run(prog, data=b""):
    tape = [0] * 30000
    ptr = 0
    jumps = {}
    stack = []
    for i, c in enumerate(prog):
        if c == '[':
            stack.append(i)
        elif c == ']':
            if not stack:
                raise ValueError(f"unmatched ] at {i}")
            j = stack.pop()
            jumps[i] = j
            jumps[j] = i
    if stack:
        raise ValueError(f"unmatched [ at {stack.pop()}")
    di = 0
    out = []
    i = 0
    steps = 0
    while i < len(prog):
        steps += 1
        if steps > 100_000_000:
            raise RuntimeError("step cap exceeded (infinite loop?)")
        c = prog[i]
        if c == '>':
            ptr = (ptr + 1) % len(tape)
        elif c == '<':
            ptr = (ptr - 1) % len(tape)
        elif c == '+':
            tape[ptr] = (tape[ptr] + 1) % 256
        elif c == '-':
            tape[ptr] = (tape[ptr] - 1) % 256
        elif c == '.':
            out.append(chr(tape[ptr]))
        elif c == ',':
            if di < len(data):
                tape[ptr] = data[di]
                di += 1
            else:
                tape[ptr] = 0
        elif c == '[':
            if tape[ptr] == 0:
                i = jumps[i]
        elif c == ']':
            if tape[ptr] != 0:
                i = jumps[i]
        i += 1
    return ''.join(out)

if __name__ == "__main__":
    src = open(sys.argv[1]).read()
    data = sys.stdin.buffer.read() if not sys.stdin.isatty() else b""
    print(repr(run(src, data)))
