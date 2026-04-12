def predict_crowd_trend(density):
    """
    Simple heuristic:
    Higher density → longer time to clear
    Lower density → faster clearing
    """

    if density > 8:
        return "Will take ~20-30 minutes to clear"
    elif density > 5:
        return "Will take ~10-20 minutes to normalize"
    elif density > 3:
        return "Likely to clear in ~5-10 minutes"
    else:
        return "Area is already low density / near empty"
