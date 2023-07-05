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
df['company text'] = df.apply(lambda x: x['Company Name'] if x['Rating'] < 0 else x['Company Name'][:-3], axis = 1)

# state
df['job_state'] = df['Location'].str.split(',',regex=True,expand=True)[1]
df.job_state.value_counts()

# Age of company
df['age'] = df['Founded'].apply(lambda x: (2023 - x) if x>0 else -1)

# parsing of job description (skills)
# python
df['python'] = df['Job Description'].apply(lambda x: 1 if 'python' in x.lower() else 0)
# R
df['R'] = df['Job Description'].apply(lambda x: 1 if ' R ' in x else 0)
# spark
df['spark'] = df['Job Description'].apply(lambda x: 1 if 'spark' in x.lower() else 0)
# aws
df['aws'] = df['Job Description'].apply(lambda x: 1 if 'aws' in x.lower() else 0)
# excel
df['excel'] = df['Job Description'].apply(lambda x: 1 if 'excel' in x.lower() else 0)
# SQL
df['sql'] = df['Job Description'].apply(lambda x: 1 if 'SQL' in x else 0)

df.columns
df_out = df.drop(['Unnamed: 0'], axis = 1)

df_out.to_csv("data_jobs_cleaned.csv", index = False)
