from math import log


def precision_at_k(k, ground_truth, predictions):
    result = [0] * k
    if len(ground_truth) == 0:
        return [float('nan')] * k
    if len(predictions) == 0:
        return result
    else:
        i = 0
        count = 0
        while i < k:
            if i < len(predictions) and predictions[i] in ground_truth:
                count += 1
            result[i] = count / (i + 1)
            i += 1
    return result


def recall_at_k(k, ground_truth, predictions):
    result = [0] * k
    size = len(ground_truth)
    if size == 0:
        return [float('nan')] * k
    if len(predictions) == 0:
        return result
    else:
        i = 0
        count = 0
        while i < k:
            if i < len(predictions) and predictions[i] in ground_truth:
                count += 1
            result[i] = count / size
            i += 1
    return result


def f1_score_at_k(precision, recall):
    length = len(precision)
    result = [0] * length
    if all(precision_k == 0 for precision_k in precision) and all(recall_k == 0 for recall_k in recall):
        return result
    for i, (precision_k, recall_k) in enumerate(zip(precision, recall, strict=True)):
        if recall_k == 0 and precision_k == 0:
            result[i] = 0
        else:
            result[i] = 2 * (precision_k * recall_k) / (precision_k + recall_k)
    return result


def average_precision_at_k(k, ground_truth, predictions):
    result = [0] * k
    size = len(ground_truth)
    if size == 0:
        return [float('nan')] * k
    if len(predictions) == 0:
        return result
    else:
        i = 0
        count = 0
        precision_sum = 0.0
        while i < k:
            if i < len(predictions) and predictions[i] in ground_truth:
                count += 1
                precision_sum += count / (i + 1)
            result[i] = precision_sum / count if count != 0 else 0.0
            i += 1
    return result


def reciprocal_rank_at_k(k, ground_truth, predictions):
    result = [0] * k
    size = len(ground_truth)
    if size == 0:
        return [float('nan')] * k
    if len(predictions) == 0:
        return result
    else:
        i = 0
        top_ranked_item = False
        top_item_rank = k + 1
        while i < k and not top_ranked_item:
            if i < len(predictions) and predictions[i] in ground_truth:
                top_item_rank = i
                top_ranked_item = True
            i += 1
        result = [1 / (top_item_rank + 1) if (index >= top_item_rank) else 0 for index, _ in enumerate(result)]
    return result


def ndcg_at_k(k, ground_truth, predictions):
    result = [0] * k
    size = len(ground_truth)
    if size == 0:
        return [float('nan')] * k
    if len(predictions) == 0:
        return result
    else:
        i = 0
        ideal_count = 0
        dcg = 0.0
        ideal_dcg = 0
        while i < k:
            relevance = 0
            if i < len(predictions):
                if predictions[i] in ground_truth:
                    relevance = 1
                    ideal_dcg += 1.0 / log(ideal_count + 2)
                    ideal_count += 1
                dcg += (pow(2, relevance) - 1) / log(i + 2)
            result[i] = dcg / ideal_dcg if ideal_dcg != 0 else 0.0
            i += 1
    return result

