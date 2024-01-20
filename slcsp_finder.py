import os

import pandas as pd


def filter_silver_plans(df):
    """
    Filter silver plans from a DataFrame.

    :param df: DataFrame containing plan information.
    :return: DataFrame containing only Silver plans.
    """
    return df[df['metal_level'] == 'Silver']


def get_rate_area_to_slcsp(df):
    """
    Returns a DataFrame with the second least cost rate for each state and rate area.

    :param df: A pandas DataFrame containing the rates for each state and rate area.
    :return: A pandas DataFrame with the second least rate for each state and rate area.
    """
    return df.groupby(['state', 'rate_area'])['rate'].apply(
        lambda x: sorted(x.unique())[1] if len(x) >= 2 else ''
    )


def get_zipcode_to_rate_area(df):
    """
    Filters the given DataFrame to include only zipcodes that have a single state and a single rate area.

    :param df: The DataFrame containing the data.
    :return: A new DataFrame with only the zipcodes that have a single state and a single rate area.
    """
    df = df.groupby('zipcode').filter(
        lambda x: len(x['state'].unique()) == 1 and len(x['rate_area'].unique()) == 1
    )
    return df.groupby('zipcode').agg({'state': 'first', 'rate_area': 'first'})


def find_slcsp():
    script_dir = os.path.dirname(__file__)

    plans = pd.read_csv(os.path.join(script_dir, 'data', 'plans.csv'))
    zips = pd.read_csv(os.path.join(script_dir, 'data', 'zips.csv'), dtype={'zipcode': str})
    slcsp = pd.read_csv(os.path.join(script_dir, 'data', 'slcsp.csv'), dtype={'zipcode': str})

    # Filter out non-silver metal level plans
    plans = filter_silver_plans(plans)

    # Group plans on state rate area, and store second-highest cost if >= 2 rates, else store ''
    plans = get_rate_area_to_slcsp(plans)

    # Filter all zipcodes based on whether they are
    #   1. in multiple rate areas
    #   2. in multiple states (thus multiple rate areas)
    # Either of these conditions make SLCSP indeterminate
    zips = get_zipcode_to_rate_area(zips)

    # Merge filtered zipcodes onto SLCSP DF. Now we can use state rate areas in plans DF to get rate
    slcsp = slcsp.merge(zips, on='zipcode', how='left')
    slcsp['rate_area'] = slcsp['rate_area'].fillna(-1).astype('Int64')

    for index, row in slcsp.iterrows():
        if (row['state'], row['rate_area']) in plans:
            print(row['zipcode'] + ',' + str(plans[row['state'], row['rate_area']]))
        else:
            print(row['zipcode'] + ',')


if __name__ == '__main__':
    find_slcsp()
