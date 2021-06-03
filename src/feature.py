import collections
import pandas as pd
from Bio.SeqUtils.ProtParam import ProteinAnalysis
from modlamp.descriptors import GlobalDescriptor
from modlamp.descriptors import PeptideDescriptor


def get_global_features(features):
    seq = features["sequence"]
    desc = GlobalDescriptor(seq)
    desc.calculate_MW(amide=False)
    features["molecular_weight"] = desc.descriptor[0][0]
    desc.calculate_charge(ph=7.0)
    features["charge"] = desc.descriptor[0][0]
    desc.charge_density(ph=7.0)
    features["charge_density"] = desc.descriptor[0][0]
    # desc.isoelectric_point(amide=False)
    # features['isoelectric_point'] = desc.descriptor[0][0]
    biop_analysis = ProteinAnalysis(seq)
    features["isoelectric_point"] = biop_analysis.isoelectric_point()
    # features['flexibility'] = biop_analysis.flexibility()
    features["gravy"] = biop_analysis.gravy()
    desc.instability_index()
    features["instability_index"] = desc.descriptor[0][0]
    desc.aromaticity()
    features["aromaticity"] = desc.descriptor[0][0]
    desc.aliphatic_index()
    features["aliphatic_index"] = desc.descriptor[0][0]
    desc.boman_index()
    features["boman_index"] = desc.descriptor[0][0]
    desc.hydrophobic_ratio()
    features["hydrophobic_ratio"] = desc.descriptor[0][0]
    return features


def get_features(seq):
    """This function receives a seqIO sequence container as input and returns a feature
    dictionary."""
    features = collections.OrderedDict()
    features["sequence"] = seq
    features["length"] = len(seq)
    features = get_global_features(features)
    return features


def get_features_dataframe(sequences, cls):
    features_0 = get_features("AAAAKAAALLLKLKKLLLKAAAAAAAAAAAAAAAA")
    columns = list(features_0.keys())
    columns.append("class")
    df = pd.DataFrame(columns=columns)
    errores = []
    # Secuencias positivas
    for i in range(len(sequences)):
        try:
            if i % 100 == 0:
                print(i)
            features = get_features(sequences[i])
            df.loc[i] = [features[feature] for feature in features.keys()] + [cls]
        except Exception as e:
            print(e)
            print(sequences[i], " error")
            errores.append((e, sequences[i]))
    return df


if __name__ == "__main__":
    seq = "AAAAAAKLA"
    feat = get_features(seq)
    print(feat)
