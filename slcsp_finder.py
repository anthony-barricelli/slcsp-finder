import os

import pandas as pd
def find_slcsp():
    script_dir = os.path.dirname(__file__)

    plans = pd.read_csv(os.path.join(script_dir, 'data', 'plans.csv'))
    zips = pd.read_csv(os.path.join(script_dir, 'data', 'zips.csv'), dtype={'zipcode': str})
    slcsp = pd.read_csv(os.path.join(script_dir, 'data', 'slcsp.csv'), dtype={'zipcode': str})

    print(plans)
    print(zips)
    print(slcsp)

if __name__ == '__main__':
    find_slcsp()
