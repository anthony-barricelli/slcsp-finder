import os

import pandas as pd


def find_slcsp():
    script_dir = os.path.dirname(__file__)

    plans = pd.read_csv(os.path.join(script_dir, 'data', 'plans.csv'))
    zips = pd.read_csv(os.path.join(script_dir, 'data', 'zips.csv'), dtype={'zipcode': str})
    slcsp = pd.read_csv(os.path.join(script_dir, 'data', 'slcsp.csv'), dtype={'zipcode': str})

    # Filter out non-silver metal level plans
    plans = plans[plans['metal_level'] == 'Silver']

    # Group plans on state rate area, and store second-highest cost if >= 2 rates, else store ''
    plans = plans.groupby(['state', 'rate_area'])['rate'].apply(
        lambda x: sorted(x.unique())[1] if len(x) >= 2 else ''
    )

    #print(plans)

    # Filter all zipcodes based on whether they are
    #   1. in multiple rate areas
    #   2. in multiple states (thus multiple rate areas)
    # Either of these conditions make SLCSP indeterminate
    zips = zips.groupby('zipcode').filter(
        lambda x: len(x['state'].unique()) == 1 and len(x['rate_area'].unique()) == 1
    )
    zips = zips.groupby('zipcode').agg({'state': 'first', 'rate_area': 'first'})

    print(zips)


if __name__ == '__main__':
    find_slcsp()
