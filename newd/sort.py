def shellSort(seq, key):
    n = len(seq)
    gap = n // 2

    # Do a gapped insertion sort for this gap size.
    # The first gap elements a[0..gap-1] are already in gapped
    # order keep adding one more element until the entire array
    # is gap sorted

    while gap > 0:
        for i in range(gap, n):
            # add a[i] to the elements that have been gap sorted
            # save a[i] in temp and make a hole at position i
            temp = seq[i]

            # shift earlier gap-sorted elements up until the correct
            # location for a[i] is found
            j = i
            while j >= gap and key(seq[j - gap], temp) is False:
                seq[j] = seq[j - gap]
                j -= gap

                # put temp (the original a[i]) in its correct location
            seq[j] = temp
        gap //= 2

    return seq
