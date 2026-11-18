"""
Zero-dependency test runner for Disease Trend Analysis project.
Executes all test functions in tests/ without requiring pytest.
Can also be executed with: pytest tests/ -v
"""
import sys
import os
import time

# Ensure root directory is on python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import tests.test_data as td
import tests.test_analysis as ta
import tests.test_app as tp

def main():
    modules = [
        ("Database & Schema Tests (tests/test_data.py)", td),
        ("Analysis & Math Formula Tests (tests/test_analysis.py)", ta),
        ("App Smoke & Structure Tests (tests/test_app.py)", tp),
    ]

    total_passed = 0
    total_failed = 0
    start_time = time.time()

    print("=" * 70)
    print("  DISEASE TREND ANALYSIS - AUTOMATED VERIFICATION SUITE")
    print("=" * 70)

    for mod_name, mod in modules:
        print(f"\n--> Running {mod_name}:")
        test_funcs = [
            getattr(mod, fn) for fn in sorted(dir(mod))
            if fn.startswith("test_") and callable(getattr(mod, fn))
        ]
        for fn in test_funcs:
            doc = fn.__doc__.strip().split("\n")[0] if fn.__doc__ else fn.__name__
            try:
                fn()
                print(f"  [PASS] {fn.__name__} - {doc}")
                total_passed += 1
            except AssertionError as e:
                print(f"  [FAIL] {fn.__name__}: {e}")
                total_failed += 1
            except Exception as e:
                print(f"  [ERROR] {fn.__name__}: {type(e).__name__}: {e}")
                total_failed += 1

    duration = time.time() - start_time
    print("\n" + "=" * 70)
    print(f"RESULTS: {total_passed} Passed, {total_failed} Failed in {duration:.3f}s")
    print("=" * 70)

    if total_failed > 0:
        sys.exit(1)
    else:
        print("STATUS: ALL TESTS PASSED SUCCESSFULLY (100% SUCCESS RATE)\n")
        sys.exit(0)

if __name__ == "__main__":
    main()
