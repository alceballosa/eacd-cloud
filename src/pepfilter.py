def amp_filter(seq, valid_aas, min_aas=6, max_aas=300, min_unique_aas=2, verbose=False):
    """
    Input:
        -seq: aminoacid sequence.
        -min_aas: minimum number of aas for sequence.
        -max_aas: maximum number of aas for sequence.
        -valid_aas: a list with the aminoacids to be included.
        -min_unique_aas = minimum number of unique aas for sequence.

    Output:
        >False if 'seq' does not comply with any of the criteria.
        >True if 'seq' complies with all of the criteria.
    """

    if len(seq) > max_aas or len(seq) < min_aas:
        if verbose:
            print("Discarded ", seq, " due to length ", len(seq))
        return False
    set_diff = set(seq) - valid_aas
    if len(set_diff) > 0:
        if verbose:
            print("Discarded ", seq, " due to ", set_diff)
        return False

    if len(set(seq)) < min_unique_aas:
        if verbose:
            print("Discarded ", seq, " due to low number of different aas")
        return False
    return True
