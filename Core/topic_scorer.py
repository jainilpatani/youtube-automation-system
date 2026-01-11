def score_topics(google, reddit):
    scores = {}

    for g in google:
        scores[g] = scores.get(g, 0) + 5

    for r in reddit:
        for word in r.lower().split():
            if len(word) > 4:
                scores[word] = scores.get(word, 0) + 1

    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return ranked[:5]  # [(topic, score)]
