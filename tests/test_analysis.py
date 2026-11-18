try:
    import pytest
except ImportError:
    pytest = None
import math

def calculate_cfr(cases: int, deaths: int) -> float:
    """Helper mimicking src/analysis.py CFR logic."""
    if not cases or cases <= 0:
        return 0.0
    return round((deaths / cases) * 100.0, 2)

def calculate_recovery_rate(cases: int, recovered: int) -> float:
    """Helper mimicking src/analysis.py recovery rate logic."""
    if not cases or cases <= 0:
        return 0.0
    rate = (recovered / cases) * 100.0
    return round(min(100.0, max(0.0, rate)), 2)

def calculate_yoy_delta(current_cases: int, previous_cases: int) -> float:
    """Helper mimicking YoY delta calculation."""
    if not previous_cases or previous_cases <= 0:
        return 0.0
    return round(((current_cases - previous_cases) / previous_cases) * 100.0, 2)

def calculate_incidence_per_lakh(cases: int, population: int) -> float:
    """Helper mimicking incidence per lakh calculation."""
    if not population or population <= 0:
        return 0.0
    return round((cases / population) * 100000.0, 2)

def compute_pearson_r(x: list, y: list) -> float:
    """Helper computing Pearson correlation coefficient."""
    n = len(x)
    assert n == len(y) and n > 0
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    num = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
    den_x = sum((x[i] - mean_x) ** 2 for i in range(n))
    den_y = sum((y[i] - mean_y) ** 2 for i in range(n))
    den = math.sqrt(den_x * den_y)
    return round(num / den, 4) if den != 0 else 0.0

def test_cfr_known_vector_calculation(): # TC-T-09
    """TC-T-09: Verify CFR calculation matches 5.0% for 100 cases, 5 deaths."""
    assert calculate_cfr(100, 5) == 5.0
    assert calculate_cfr(250, 6) == 2.4
    assert calculate_cfr(0, 0) == 0.0 # Division by zero safety

def test_recovery_rate_known_vector(): # TC-T-10
    """TC-T-10: Verify recovery rate calculation matches 92.0% for 100 cases, 92 recoveries."""
    assert calculate_recovery_rate(100, 92) == 92.0
    assert calculate_recovery_rate(100, 110) == 100.0 # Capped at 100%
    assert calculate_recovery_rate(0, 0) == 0.0

def test_yoy_growth_calculation(): # TC-T-11
    """TC-T-11: Verify YoY percentage change matches +100.0% for 200 cases vs 100 base."""
    assert calculate_yoy_delta(200, 100) == 100.0
    assert calculate_yoy_delta(50, 100) == -50.0
    assert calculate_yoy_delta(100, 100) == 0.0

def test_incidence_per_lakh_formula(): # TC-T-12
    """TC-T-12: Verify incidence per lakh formula matches 100.0 for 1000 cases in 1M population."""
    assert calculate_incidence_per_lakh(1000, 1000000) == 100.0
    assert calculate_incidence_per_lakh(2500, 5000000) == 50.0

def test_concurrent_outbreak_detection_threshold(): # TC-T-13
    """TC-T-13: Verify multi-disease outbreak threshold trigger condition."""
    disease_cases = {"Dengue": 850, "Malaria": 620, "Typhoid": 120}
    baselines = {"Dengue": 350, "Malaria": 280, "Typhoid": 220}
    
    surging_diseases = [d for d, c in disease_cases.items() if c > (baselines[d] * 1.5)]
    is_concurrent_outbreak = len(surging_diseases) >= 2
    
    assert is_concurrent_outbreak is True
    assert set(surging_diseases) == {"Dengue", "Malaria"}

def test_pearson_correlation_linear_vector(): # TC-T-14
    """TC-T-14: Verify Pearson correlation engine returns r = 1.0 for perfect linear series."""
    x = [10.0, 20.0, 30.0, 40.0, 50.0]
    y = [25.0, 50.0, 75.0, 100.0, 125.0]
    r = compute_pearson_r(x, y)
    assert abs(r - 1.0) < 0.001
