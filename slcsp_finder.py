import os

import pandas as pd


def find_slcsp():
    script_dir = os.path.dirname(__file__)

    plans = pd.read_csv(os.path.join(script_dir, 'data', 'plans.csv'))
    zips = pd.read_csv(os.path.join(script_dir, 'data', 'zips.csv'), dtype={'zipcode': str})
    slcsp = pd.read_csv(os.path.join(script_dir, 'data', 'slcsp.csv'), dtype={'zipcode': str})

    # Filter out non-silver metal level plans
    plans = plans[plans['metal_level'] == 'Silver']

    print(plans)


if __name__ == '__main__':
    find_slcsp()
