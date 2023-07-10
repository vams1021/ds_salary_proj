import glassdoor_scraper_func as gs
import pandas as pd

df = gs.get_jobs("'data scientist'", 140, False)
df.to_csv(r"C:\Users\vams\OneDrive\Desktop\My files\Masters stuff\STUDY\PROJECTS\Data science salary\ds_salary_proj\data_jobs_scraped_raw.csv")