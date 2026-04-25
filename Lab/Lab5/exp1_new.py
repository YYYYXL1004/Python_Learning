if __name__ == "__main__":                                    # 1
    # line.strip()  f.readlines()                             # 2
    with open('exp1.py', 'r', encoding='utf-8') as f:         # 3
        lines = [line.strip('\n') for line in f.readlines()]  # 4
                                                              # 5
    max_len = max([len(line) for line in lines], default=0)   # 6
                                                              # 7
    with open('exp1_new.py', 'w', encoding='utf-8') as f:     # 8
        # enumerate(lines, 1)                                 # 9
        for i, line in enumerate(lines, 1):                   # 10
            # line.ljust(max_len)                             # 11
            new_line = f"{line.ljust(max_len)}  # {i}\n"      # 12
            f.write(new_line)                                 # 13
                                                              # 14
                                                              # 15
