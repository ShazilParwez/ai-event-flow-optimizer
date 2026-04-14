import numpy as np
import pandas as pd 

VENUE_AREAS = [
    {"name": "Food Court", "x": 80, "y": 80, "radius": 15},
    {"name": "Male Restroom", "x": 20, "y": 85, "radius": 8},
    {"name": "Female Restroom", "x": 35, "y": 85, "radius": 8},
    {"name": "Merchandise Stand", "x": 50, "y": 20, "radius": 12},
    {"name": "Main Entrance", "x": 50, "y": 5, "radius": 15},
    {"name": "VIP Lounge", "x": 80, "y": 20, "radius": 10},
    {"name": "Waiting Room", "x": 15, "y": 50, "radius": 15},
    {"name": "Seating Block A", "x": 30, "y": 50, "radius": 18},
    {"name": "Seating Block B", "x": 70, "y": 50, "radius": 18},
]


def generate_crowd_data():
    points = []

    for area in VENUE_AREAS:
        num_people = np.random.randint(15, 90)

        xs = np.random.normal(area["x"], area["radius"] / 1.5, num_people)
        ys = np.random.normal(area["y"], area["radius"] / 1.5, num_people)

        xs = np.clip(xs, 0, 100)
        ys = np.clip(ys, 0, 100)

        for x, y in zip(xs, ys):
            points.append(
                {
                    "x": x,
                    "y": y,
                    "density": np.random.randint(1, 6),
                    "area_name": area["name"],
                }
            )

    ambient_n = np.random.randint(50, 150)
    for _ in range(ambient_n):
        points.append(
            {
                "x": np.random.uniform(0, 100),
                "y": np.random.uniform(0, 100),
                "density": 1,
                "area_name": "Walkways",
            }
        )

    return pd.DataFrame(points)
