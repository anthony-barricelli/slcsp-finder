import argparse
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
        lambda x: '{:.2f}'.format(sorted(x.unique())[1]) if len(x) >= 2 else ''
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


def find_slcsp(plans_data, zips_data, slcsp_data):
    """
    :param plans_data: Path to the CSV file containing plan data.
    :param zips_data: Path to the CSV file containing zip code data.
    :param slcsp_data: Path to the CSV file containing slcsp data.
    :return: None

    Find the Second Least Cost Silver Plan (SLCSP) for the given zipcodes in slcsp_data and
    display them as comma separated values, in order that they were given. Indeterminable
    SLCSP rates are displayed as an empty string.
    """

    plans = pd.read_csv(plans_data)
    zips = pd.read_csv(zips_data, dtype={'zipcode': str})
    slcsp = pd.read_csv(slcsp_data, dtype={'zipcode': str})

    # Filter out non-silver metal level plans
    plans = filter_silver_plans(plans)

    # Group plans on state rate area, and store second-highest cost if >= 2 rates, else store ''
    plans = get_rate_area_to_slcsp(plans)

    # Filter all zipcodes based on whether they are
    #   1. in multiple rate areas
    #   2. in multiple states (thus multiple rate areas)
    # Either of these conditions make SLCSP indeterminable
    zips = get_zipcode_to_rate_area(zips)

    # Merge filtered zipcodes onto SLCSP DF. Now we can use state rate areas in plans DF to get rate
    slcsp = slcsp.merge(zips, on='zipcode', how='left')
    slcsp['rate_area'] = slcsp['rate_area'].fillna(-1).astype('Int64')

    # Print out results as specified by assignment
    print('zipcode, rate')
    for index, row in slcsp.iterrows():
        if (row['state'], row['rate_area']) in plans:
            print(row['zipcode'] + ',' + plans[row['state'], row['rate_area']])
        else:
            print(row['zipcode'] + ',')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    script_dir = os.path.dirname(__file__)
    default_plans_data = os.path.join(script_dir, 'data', 'plans.csv')
    default_zips_data = os.path.join(script_dir, 'data', 'zips.csv')
    default_slcsp_data = os.path.join(script_dir, 'data', 'slcsp.csv')

    parser.add_argument('--plans', help='Path to custom "plans.csv" file', default=default_plans_data)
    parser.add_argument('--zips', help='Path to custom "zips.csv" file', default=default_zips_data)
    parser.add_argument('--slcsp', help='Path to custom "slcsp.csv" file', default=default_slcsp_data)

    args = parser.parse_args()
    find_slcsp(args.plans, args.zips, args.slcsp)
