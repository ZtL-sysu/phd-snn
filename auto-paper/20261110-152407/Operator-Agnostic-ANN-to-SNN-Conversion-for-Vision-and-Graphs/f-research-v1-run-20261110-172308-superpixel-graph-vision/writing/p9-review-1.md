# Reviewer 1 (method/theory lens)

The paper transfers a conversion-error identity from node classification to graph-level visual classification. The identity is exact and the derivation is short and correct; the float64 verification with a discussion of the float32 accumulation artefact is a useful credibility detail. The observation that the closed-form bias is redundant under deterministic two-phase spiking is the most interesting technical point and is supported by a paired ablation.

Concerns: (1) teacher accuracy is low and could be read as an accuracy claim; (2) the energy numbers are op-count estimates, not measurements; (3) the MNIST conversion loss is far from the 1.5pp target mentioned in earlier internal documents.

Verdict: the manuscript is honest about all three. The explicit accuracy-energy frontier and the negative scaling result address (3) directly. Recommend acceptance pending a clear statement that no 1.5pp attainment is claimed.
