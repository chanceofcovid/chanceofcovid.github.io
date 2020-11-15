import os

import datetime

import pandas as pd


def p_any_infected(p_anyone_infected, num_people):
    p_all_not_infected = (1 - p_anyone_infected) ** num_people
    return 1 - p_all_not_infected

def write_us_state(df, state_name):

    if not os.path.exists('us'):
        os.makedirs('us')

    if not os.path.exists(f'us/{state_name}'):
        os.makedirs(f'us/{state_name}')

    # Write a file for each county US/{state_name}/{county_name}
    for index, row in df.iterrows():
        html = f"""
<html>
<head>
<body>
<title>{state_name} / {row["Name"]} - Chance of COVID</title>
</body>
<h1>{state_name} / {row["Name"]}</h1>
<p>
According to <a href="http://microcovid.org">MicroCOVID.org</a>,
the "Estimated Prevalence" of COVID in this county is {row["Estimated prevalence"]:.1%}
</p>

<p>If you interact with a certain number of people in this location
(all at once in a group, or spread out across the day), what is the chance that
1 or more of them has COVID?</p>

<ul>
<li>1 person: {row["Estimated prevalence"]:.1%}</li>
<li>2 people: {row["Chance anyone has COVID in group of 2"]:.1%}</li>
<li>3 people: {row["Chance anyone has COVID in group of 3"]:.1%}</li>
<li>5 people: {row["Chance anyone has COVID in group of 5"]:.1%}</li>
<li>10 people: {row["Chance anyone has COVID in group of 10"]:.1%}</li>
<li>25 people: {row["Chance anyone has COVID in group of 25"]:.1%}</li>
<li>100 people: {row["Chance anyone has COVID in group of 100"]:.1%}</li>
</ul>


Last updated: {datetime.datetime.utcnow()} UTC
"""
        f = open(f"US/{state_name}/{row['Name']}.html", "w")
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



df_va = pd.read_csv('https://github.com/microcovid/microcovid/raw/main/public/prevalence_data/US_51.csv')
df_va = add_columns(df_va)

write_us_state(df_va, 'va')
