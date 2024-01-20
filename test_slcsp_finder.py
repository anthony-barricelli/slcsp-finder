import unittest
import pandas as pd
import slcsp_finder


class TestSlcspFinder(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.plans_df = pd.DataFrame(
            [
                {'metal_level': 'Silver', 'rate': 100, 'state': 'NY', 'rate_area': 1},
                {'metal_level': 'Bronze', 'rate': 80, 'state': 'NY', 'rate_area': 1},
                {'metal_level': 'Silver', 'rate': 90, 'state': 'NY', 'rate_area': 1},
                {'metal_level': 'Silver', 'rate': 90, 'state': 'NY', 'rate_area': 2},
            ]
        )

        cls.silver_plans_df = pd.DataFrame(
            [
                {'metal_level': 'Silver', 'rate': 100, 'state': 'NY', 'rate_area': 1},
                {'metal_level': 'Silver', 'rate': 90, 'state': 'NY', 'rate_area': 1},
                {'metal_level': 'Silver', 'rate': 90, 'state': 'NY', 'rate_area': 1},
                {'metal_level': 'Silver', 'rate': 80, 'state': 'NY', 'rate_area': 2},
                {'metal_level': 'Silver', 'rate': 90, 'state': 'MA', 'rate_area': 1},
                {'metal_level': 'Silver', 'rate': 95, 'state': 'MA', 'rate_area': 2},
            ]
        )

        cls.zips_df = pd.DataFrame(
            [
                {'zipcode': '10001', 'state': 'NY', 'rate_area': 1},
                {'zipcode': '10002', 'state': 'NY', 'rate_area': 1},
                {'zipcode': '10003', 'state': 'NY', 'rate_area': 2},
            ]
        )

    def test_filter_silver_plans(self):
        result = slcsp_finder.filter_silver_plans(self.plans_df)
        self.assertEqual(3, len(result))
        self.assertTrue(all(result['metal_level'] == 'Silver'))

    def test_get_rate_area_to_slcsp(self):
        result = slcsp_finder.get_rate_area_to_slcsp(self.silver_plans_df)
        self.assertEqual('100.00', result[('NY', 1)])
        self.assertEqual('', result[('MA', 1)])

    def test_get_zipcode_to_rate_area(self):
        result = slcsp_finder.get_zipcode_to_rate_area(self.zips_df)
        self.assertTrue('10002' in result.index)
        self.assertEqual('NY', result['state']['10001'])


if __name__ == '__main__':
    unittest.main()
