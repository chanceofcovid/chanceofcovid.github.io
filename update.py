import os

import datetime

import pandas as pd


def p_any_infected(p_anyone_infected, num_people):
    p_all_not_infected = (1 - p_anyone_infected) ** num_people
    return 1 - p_all_not_infected

def write_us_state(df, state_name, state_slug):

    if not os.path.exists('us'):
        os.makedirs('us')

    if not os.path.exists(f'us/{state_slug}'):
        os.makedirs(f'us/{state_slug}')

    # Write a file for each county US/{state_name}/{county_name}
    for index, row in df.iterrows():
        html = f"""
# {state_name} / {row["Name"]}

According to [MicroCOVID.org](http://microcovid.org),
the "Estimated Prevalence" of COVID in this county is {row["Estimated prevalence"]:.1%}

If you interact with a certain number of people in this location
(all at once in a group, or spread out across the day), what is the chance that
1 or more of them has COVID?

- 1 person: {row["Estimated prevalence"]:.1%}
- 2 people: {row["Chance anyone has COVID in group of 2"]:.1%}
- 3 people: {row["Chance anyone has COVID in group of 3"]:.1%}
- 5 people: {row["Chance anyone has COVID in group of 5"]:.1%}
- 10 people: {row["Chance anyone has COVID in group of 10"]:.1%}
- 25 people: {row["Chance anyone has COVID in group of 25"]:.1%}
- 100 people: {row["Chance anyone has COVID in group of 100"]:.1%}


Last updated: {datetime.datetime.utcnow()} UTC
"""
        if not os.path.exists(f'us/{state_slug}/{row["County Slug"]}'):
            os.makedirs(f'us/{state_slug}/{row["County Slug"]}')
        f = open(f'US/{state_slug}/{row["County Slug"]}/index.md', "w")
        f.write(html)
        f.close()

    # TODO: Write a state level file US/{state_name}

def add_columns(df):
    df['Chance anyone has COVID in group of 2'] = df['Estimated prevalence'].apply(lambda x: p_any_infected(x, 2))
    df['Chance anyone has COVID in group of 3'] = df['Estimated prevalence'].apply(lambda x: p_any_infected(x, 3))
    df['Chance anyone has COVID in group of 5'] = df['Estimated prevalence'].apply(lambda x: p_any_infected(x, 5))
    df['Chance anyone has COVID in group of 10'] = df['Estimated prevalence'].apply(lambda x: p_any_infected(x, 10))
    df['Chance anyone has COVID in group of 25'] = df['Estimated prevalence'].apply(lambda x: p_any_infected(x, 25))
    df['Chance anyone has COVID in group of 100'] = df['Estimated prevalence'].apply(lambda x: p_any_infected(x, 100))
    return df

def main():


    df_index = pd.read_csv("https://github.com/microcovid/microcovid/raw/423ec100160f0c1de3d1330e3a807fa1db29f301/public/prevalence_data/index.csv", error_bad_lines=False)
    for index, row in df_index.iterrows():
        # Skip non-US for now
        if row["Slug"][:2]!='US':
            continue
        state_name = row["Location"]
        state_slug = state_name.lower().replace(' ',"-")
        df = pd.read_csv(f'https://github.com/microcovid/microcovid/raw/main/public/prevalence_data/{row["Slug"]}.csv')
        df["County Slug"] = df["Name"].apply(lambda x: x.lower().replace(' ',"-"))
        df["State Slug"] = state_slug
        df = add_columns(df)

        write_us_state(df, state_name, state_slug)
    return True

if __name__ == '__main__':
    main()