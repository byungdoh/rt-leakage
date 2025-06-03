"""
Converts overlapping token span indices into text sequences
Overlaps were identified using the "EleutherAI/pythia-70m" tokenizer
The indices do not assume an <s> token at the beginning of each RT article
"""

import sys
from transformers import AutoTokenizer


def process_overlaps(fn):
    overlaps = []
    with open(fn) as f:
        lines = f.readlines()
    for line in lines[1:]:
        corpus, artid, artlen, overlaplen, overlaploc, overlapfreq, logprob, threshold = line.strip().split("\t")
        overlaps.append([corpus, int(artid), int(artlen), int(overlaplen), int(overlaploc), int(overlapfreq), float(logprob), int(threshold)])
    return overlaps


def process_rt_articles(fn):
    articles = []
    f = open(fn)
    first_line = f.readline()
    assert first_line.strip() == "!ARTICLE"
    curr_article = ""

    for line in f:
        sentence = line.strip()
        if sentence == "!ARTICLE":
            articles.append(curr_article[:-1])
            curr_article = ""
        else:
            curr_article += line.strip() + " "

    articles.append(curr_article[:-1])
    return articles


def main():
    articles = process_rt_articles(sys.argv[1])
    tokenizer = AutoTokenizer.from_pretrained("EleutherAI/pythia-70m")

    batches = []
    for article in articles:
        tokenizer_output = tokenizer(article)
        ids = tokenizer_output.input_ids
        batches.append(ids)

    curr_corpus = sys.argv[1].split("/")[-1].split(".")[0]
    overlaps = process_overlaps(sys.argv[2])
    print(f"corpus\tarticle_num\tarticle_len\toverlap_len\toverlap_last_token\toverlap_freq\t5gram_logprob\tbelow_threshold\toverlap_text")

    for overlap in overlaps:
        corpus, artid, artlen, overlaplen, overlaploc, overlapfreq, logprob, threshold = overlap
        if corpus == curr_corpus:
            assert len(batches[artid]) == artlen
            overlap_tokens = batches[artid][(overlaploc-overlaplen+1):(overlaploc+1)]
            assert(len(overlap_tokens) == overlaplen)
            overlap_text = tokenizer.decode(overlap_tokens)
            print(f"{corpus}\t{artid}\t{artlen}\t{overlaplen}\t{overlaploc}\t{overlapfreq}\t{logprob}\t{threshold}\t{overlap_text}")


if __name__ == "__main__":
    main()
