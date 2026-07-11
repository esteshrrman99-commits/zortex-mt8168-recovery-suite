# ZORTEX Policy Objectives and Simulation Milestone
Commands:
- `python scripts/zortex_policy.py list`
- `python scripts/zortex_policy.py simulate flash`
- `python scripts/zortex_policy.py simulate unlock`
- `python scripts/zortex_policy.py plan`
Validation:
- `python -m pip install -e .`
- `pytest -q tests/test_policy_simulation.py`
- `pytest -q --maxfail=1`
