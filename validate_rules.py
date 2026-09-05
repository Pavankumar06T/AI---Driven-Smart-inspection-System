from rules_data import RULES

print(f"Total rules loaded: {len(RULES)}")
by_scenario = {}
for r in RULES:
    by_scenario.setdefault(r.scenario, []).append(r.check_id)

for scenario, ids in by_scenario.items():
    print(f"{scenario}: {len(ids)} checks -> {ids}")

assert len(RULES) == 15, "You should have exactly 15 verified checks before moving on."
print("All rules structurally valid")