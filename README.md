# Supply Chain Planning Simulator | Python + JSON

A small teaching simulator that forecasts weekly production, tracks inventory and shortages, and allocates returned units to rework, recycling, donations, and disposal.

## Context
Inspired by a university supply-chain simulation and studies in international business. **This is an independent educational reconstruction, not an exact export from a graded simulation or a real company's production system.** Demand numbers in `data/scenario.json` are illustrative.

## Scenario assumptions
- Maximum internal production of 7,000 units per week
- No overtime or outsourced production
- Base safety-stock target of 500 units
- Four delivery channels split 40%, 15%, 15%, and 30%
- Returns directed to rework 65%, recycle 20%, donate 10%, dispose 5%
- Reworked returns enter next week's usable inventory (a simplifying assumption)

## Run
```bash
python planner.py --scenario data/scenario.json --output results.json
python -m unittest discover -s tests -v
```

Python 3.10+ and no external packages. `results.json` is generated and excluded from Git.

## What this demonstrates
Demand planning, capacity constraints, inventory carryover, reverse logistics, rounding without losing units, JSON data handling and automated tests.

## Transparency
Created as a standalone learning and portfolio implementation with AI assistance. Parameters are examples for demonstrating the model, not employer information.
