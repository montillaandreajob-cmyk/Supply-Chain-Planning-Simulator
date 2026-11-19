"""Simple production and reverse-logistics planning simulation."""
import argparse
import json
import math
from pathlib import Path


def allocate(total, proportions):
    """Distribute an integer total using largest-remainder allocation."""
    if not isinstance(total, int) or total < 0:
        raise ValueError("total must be a nonnegative integer")
    if not proportions or any(v < 0 for v in proportions.values()):
        raise ValueError("Invalid proportions")
    if not math.isclose(sum(proportions.values()), 1.0, abs_tol=1e-8):
        raise ValueError("Proportions must total 1")
    raw = {k: total * v for k, v in proportions.items()}
    values = {k: math.floor(v) for k, v in raw.items()}
    remainder = total - sum(values.values())
    order = sorted(proportions, key=lambda k: (- (raw[k] - values[k]), k))
    for key in order[:remainder]:
        values[key] += 1
    return values


def simulate(scenario):
    capacity = scenario["max_weekly_capacity"]
    target = scenario["target_ending_inventory"]
    inventory = scenario["starting_inventory"]
    if not all(isinstance(n, int) and n >= 0 for n in (capacity, target, inventory)):
        raise ValueError("Capacity, inventory and target must be nonnegative integers")
    incoming_rework = 0
    results = []
    for week in scenario["weeks"]:
        demand, returns = week["demand"], week["returns"]
        if not all(isinstance(x, int) and x >= 0 for x in (demand, returns)):
            raise ValueError("Demand and returns must be nonnegative integers")
        available_before_production = inventory + incoming_rework
        production = min(capacity, max(0, demand + target - available_before_production))
        usable = available_before_production + production
        shipped = min(demand, usable)
        shortage = demand - shipped
        inventory = usable - shipped
        reverse_logistics = allocate(returns, scenario["returns_mix"])
        incoming_rework = reverse_logistics["rework"]
        results.append({
            "week": week["week"], "demand": demand, "production": production,
            "shipped": shipped, "shortage": shortage, "ending_inventory": inventory,
            "transport_units": allocate(shipped, scenario["transport_mix"]),
            "returns_processed": reverse_logistics,
            "rework_available_next_week": incoming_rework,
        })
    total_demand = sum(w["demand"] for w in results)
    total_shipped = sum(w["shipped"] for w in results)
    return {
        "weeks": results,
        "totals": {"demand": total_demand, "shipped": total_shipped,
                   "production": sum(w["production"] for w in results),
                   "service_level_pct": round(100 * total_shipped / total_demand, 2) if total_demand else 100.0}
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scenario", default="data/scenario.json")
    parser.add_argument("--output", default="results.json")
    args = parser.parse_args()
    scenario = json.loads(Path(args.scenario).read_text(encoding="utf-8"))
    result = simulate(scenario)
    Path(args.output).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print("week | demand | produced | shipped | shortage | ending inventory")
    for w in result["weeks"]:
        print(f"{w['week']:>4} | {w['demand']:>6} | {w['production']:>8} | {w['shipped']:>7} | {w['shortage']:>8} | {w['ending_inventory']:>16}")
    print(f"Service level: {result['totals']['service_level_pct']}%")
    print(f"Results saved to: {args.output}")


if __name__ == "__main__":
    main()
