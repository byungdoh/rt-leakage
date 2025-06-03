# The Inverse Scaling Effect of Pre-Trained Language Model Surprisal Is Not Due to Data Leakage

## Introduction
This is the code repository for the paper [The Inverse Scaling Effect of Pre-Trained Language Model Surprisal Is Not Due to Data Leakage](https://arxiv.org/pdf/2506.01172), including information about longest overlapping sequences between commonly used reading time corpora (Dundee, Brown, GECO, Provo, Natural Stories) and pre-training corpora (The Pile, OpenWebText).

## Setup
Install the following dependency:
- [HuggingFace Transformers](https://huggingface.co/docs/transformers/installation) (v4.47.0 used in this work)

## Longest Overlapping Sequences
The `overlaps` directory contains two `.tsv` files with information about longest overlapping sequences between the reading time corpora and the pre-training corpora.
All lengths and indices are based on subword tokens from Pythia LM's (`EleutherAI/pythia-70m`) BPE tokenizer with no special tokens appended to the beginning of the sequence.
The `.tsv` files do not contain any actual text sequences in an effort to prevent further data leakage.

The command `python get_rt_overlaps.py READING_TIME_CORPUS OVERLAP_TSV > OVERLAP_WITH_TEXT_TSV` (e.g. `python get_rt_overlaps.py rt_corpora/my_stimuli.sentitems overlaps/rt_overlap_the_pile.tsv > overlaps/rt_overlap_the_pile_with_text.tsv`) can be used to retrieve the overlapping text sequences.
The reading time corpus should be formatted such that an `!ARTICLE` delimiter comes between each article.

```
$ cat rt_corpora/my_stimuli.sentitems
!ARTICLE
This is the first sentence of the first article.
This is the second sentence of the first article.
...
!ARTICLE
This is the first sentence of the second article.
...
```

## Questions
For questions or concerns, please contact Byung-Doh Oh ([oh.b@nyu.edu](mailto:oh.b@nyu.edu)).
