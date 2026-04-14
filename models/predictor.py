def predict_crowd_trend(density):
    # Handle single value (float/int)
    if isinstance(density, (int, float)):
        if density < 60:
            return "Fast clearing expected"
        elif density < 120:
            return "Moderate crowd movement"
        else:
            return "Slow clearing, congestion likely"

    # Handle list input (for tests)
    if not density or len(density) == 0:
        raise ValueError("Density data is empty")

    avg_density = sum(density) / len(density)

    if avg_density < 60:
        return "Fast clearing expected"
    elif avg_density < 120:
        return "Moderate crowd movement"
    else:
        return "Slow clearing, congestion likely"