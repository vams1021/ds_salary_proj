import pandas as pd

df = pd.read_csv("data_jobs_scraped_raw.csv")

# salary parsing
df['hourly'] = df['Salary Estimate'].apply(lambda x: 1 if 'per hour' in x.lower() else 0)
df['employer_provided'] = df['Salary Estimate'].apply(lambda x: 1 if 'employer provided salary:' in x.lower() else 0)
df = df[df['Salary Estimate'] != '-1']
df['Salary Estimate'] = df['Salary Estimate'].apply(lambda x: x.split('(')[0])
df['Salary Estimate'] = df['Salary Estimate'].replace('Employer Provided Salary:','',regex=True)
df['Salary Estimate'] = df['Salary Estimate'].apply(lambda x: x.replace('$','').replace('K',''))
df['Salary Estimate'] = df['Salary Estimate'].apply(lambda x: x.replace('Per Hour',''))
df[['min_salary','max_salary']] = df['Salary Estimate'].str.split('-',regex=True,expand=True)
df['min_salary'] = df['min_salary'].astype('float')
df['min_salary'] = df['min_salary'].astype('int')
df['max_salary'] = df['max_salary'].astype('float')
df['max_salary'] = df['max_salary'].fillna(df['min_salary'])
df['max_salary'] = df['max_salary'].astype('int')
df['avg_salary'] = (df['min_salary'] + df['max_salary'])/2

# company name text only



# state
# Age of company
# parsing of job description (skills)