def my_filter(func, seq):
    i = 0
    while i < len(seq):
        if not func(seq[i]):
            seq.pop(i)
            i -= 1
        i += 1
    return seq