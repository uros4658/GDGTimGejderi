import pandas as pd
import json
from pulp import LpProblem, LpVariable, LpMinimize, LpBinary, lpSum, LpStatus, value

# Load vessel calls and berths
vessels = pd.read_csv("data/vessel_calls.csv")
berths = pd.DataFrame([
    {"name": "A1", "length_m": 350, "depth_m": 15},
    {"name": "B2", "length_m": 250, "depth_m": 13},
    {"name": "C3", "length_m": 220, "depth_m": 11},
    {"name": "D4", "length_m": 400, "depth_m": 16},
])

# Decision variables: x[vessel_idx, berth_idx] = 1 if vessel assigned to berth
x = {}
prob = LpProblem("BerthAssignment", LpMinimize)

for vi, v in vessels.iterrows():
    for bi, b in berths.iterrows():
        # Only allow assignment if vessel fits
        if v["loa_m"] <= b["length_m"] and v["draft_m"] <= b["depth_m"]:
            x[(vi, bi)] = LpVariable(f"x_{vi}_{bi}", cat=LpBinary)
        else:
            x[(vi, bi)] = None  # Not feasible

# Objective: (dummy, minimize total berth index for demo)
prob += lpSum(x[(vi, bi)] for (vi, bi) in x if x[(vi, bi)] is not None)

# Each vessel assigned to exactly one berth
for vi in vessels.index:
    prob += lpSum(x[(vi, bi)] for bi in berths.index if x[(vi, bi)] is not None) == 1

# No two vessels at same berth at same time (using ETA and 8h stay)
vessels["eta_dt"] = pd.to_datetime(vessels["eta"])
vessels["etd_dt"] = vessels["eta_dt"] + pd.Timedelta(hours=8)

for bi in berths.index:
    for vi1 in vessels.index:
        for vi2 in vessels.index:
            if vi1 >= vi2:
                continue  # avoid duplicate/self-pairs
            eta1, etd1 = vessels.loc[vi1, "eta_dt"], vessels.loc[vi1, "etd_dt"]
            eta2, etd2 = vessels.loc[vi2, "eta_dt"], vessels.loc[vi2, "etd_dt"]
            overlap = not (etd1 <= eta2 or etd2 <= eta1)
            if overlap:
                var1 = x.get((vi1, bi))
                var2 = x.get((vi2, bi))
                if var1 is not None and var2 is not None:
                    prob += var1 + var2 <= 1

# Solve
prob.solve()

# Output plan
berth_plan = []
for vi, v in vessels.iterrows():
    assigned_berth = None
    for bi, b in berths.iterrows():
        var = x.get((vi, bi))
        if var is not None and value(var) == 1:
            assigned_berth = b["name"]
            break
    berth_plan.append({
        "vessel": v.get("vessel_name", f"Vessel-{vi+1}"),
        "eta": v["eta"],
        "berth": assigned_berth
    })

with open("berth_plan_mip.json", "w") as f:
    json.dump(berth_plan, f, indent=2)

print(json.dumps(berth_plan, indent=2))