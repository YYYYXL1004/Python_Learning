if __name__ == "__main__":
    # line.strip()  f.readlines()
    with open('exp1.py', 'r', encoding='utf-8') as f:
        lines = [line.strip('\n') for line in f.readlines()]

    max_len = max([len(line) for line in lines], default=0)

    with open('exp1_new.py', 'w', encoding='utf-8') as f:
        # enumerate(lines, 1)
        for i, line in enumerate(lines, 1):
            # line.ljust(max_len)
            new_line = f"{line.ljust(max_len)}  # {i}\n"
            f.write(new_line)


