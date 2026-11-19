import json
from pathlib import Path
import unittest
from planner import allocate, simulate

class PlannerTests(unittest.TestCase):
    def test_allocation_never_loses_units(self):
        mix = {'a': .4, 'b': .15, 'c': .15, 'd': .3}
        for total in [0, 1, 3, 13, 4799]:
            self.assertEqual(sum(allocate(total, mix).values()), total)

    def test_scenario_capacity_and_flow(self):
        scenario = json.loads((Path(__file__).resolve().parents[1] / 'data/scenario.json').read_text())
        result = simulate(scenario)
        for week in result['weeks']:
            self.assertLessEqual(week['production'], 7000)
            self.assertEqual(sum(week['transport_units'].values()), week['shipped'])
            self.assertEqual(sum(week['returns_processed'].values()),
                             scenario['weeks'][week['week'] - 1]['returns'])
            self.assertEqual(week['demand'], week['shipped'] + week['shortage'])

    def test_capacity_limited_shortage(self):
        result = simulate({'max_weekly_capacity': 10, 'target_ending_inventory': 0,
                           'starting_inventory': 0, 'transport_mix': {'x': 1},
                           'returns_mix': {'rework': 1},
                           'weeks': [{'week': 1, 'demand': 15, 'returns': 0}]})
        self.assertEqual(result['weeks'][0]['shortage'], 5)

if __name__ == '__main__':
    unittest.main()
