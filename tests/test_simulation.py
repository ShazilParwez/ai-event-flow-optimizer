from utils.simulation import generate_crowd_data

def test_generate_data_not_empty():
    data = generate_crowd_data()
    assert not data.empty

def test_generate_data_columns():
    data = generate_crowd_data()
    assert set(["x", "y", "density"]).issubset(data.columns)

def test_density_range():
    data = generate_crowd_data()
    assert data["density"].min() >= 0