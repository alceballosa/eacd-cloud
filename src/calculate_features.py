from Bio import SeqIO

import feature

if __name__ == "__main__":
    positive_sequences = []
    negative_sequences = []

    for record in SeqIO.parse("./data/POSITIVO_CDHIT09_6-35_sinX.fa", "fasta"):
        positive_sequences.append(str(record.seq))

    for record in SeqIO.parse(
        "./data/NEGATIVOS_FINAL_RANDOMTAILS_SINREPES.fa", "fasta"
    ):
        negative_sequences.append(str(record.seq))

    df_pos = feature.get_features_dataframe(positive_sequences, 1)
    df_neg = feature.get_features_dataframe(negative_sequences, 0)

    df_pos.to_csv("./data/pos.csv", index=False)
    df_neg.to_csv("./data/neg.csv", index=False)
