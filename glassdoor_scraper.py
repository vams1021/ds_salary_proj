from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import time
import pandas as pd

def get_jobs(keyword, num_jobs, verbose):
    '''Gathers jobs as a dataframe, scraped from Glassdoor'''

    # Initializing the webdriver
    options = webdriver.ChromeOptions()

    # Uncomment the line below if you'd like to scrape without a new Chrome window every time.
    # options.add_argument('headless')

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    driver.set_window_size(1120, 1000)

    url = "https://www.glassdoor.com/Job/jobs.htm?sc.keyword=" + keyword + "&clickSource=searchBox"
    driver.get(url)
    jobs = []

    while len(jobs) < num_jobs:  # If true, should be still looking for new jobs.

        # Let the page load. Change this number based on your internet speed.
        # Or, wait until the webpage is loaded, instead of hardcoding it.
        time.sleep(4)

        # Test for the "Sign Up" prompt and get rid of it.
        try:
            driver.find_element(By.CLASS_NAME, "selected").click()
        except ElementClickInterceptedException:
            pass

        time.sleep(.1)

        try:
            driver.find_element(By.XPATH, '//div[@id="LoginModal"]/div/div/div[2]/button').click()  # clicking to the X.
        except NoSuchElementException:
            pass

        # Going through each job in this page
        job_buttons = driver.find_elements(By.XPATH, "//ul[@class='hover p-0 my-0  css-7ry9k1 exy0tjh5']/li")
        for job_button in job_buttons:
            # print(job_button.text)
            print("Progress: {}".format("" + str(len(jobs)) + "/" + str(num_jobs)))
            if len(jobs) >= num_jobs:
                break

            job_button.click()  # You might
            time.sleep(1)
            collected_successfully = False

            while not collected_successfully:
                try:
                    company_name = driver.find_element(By.XPATH, './/div[@data-test="employerName"]').text
                    location = driver.find_element(By.XPATH, './/div[@data-test="location"]').text
                    job_title = driver.find_element(By.XPATH, './/div[@data-test="jobTitle"]').text
                    job_description = driver.find_element(By.XPATH, './/div[@class="jobDescriptionContent desc"]').text
                    collected_successfully = True
                except:
                    time.sleep(5)

            try:
                salary_estimate = driver.find_element(By.XPATH, './/span[@data-test="detailSalary"]').text
            except NoSuchElementException:
                salary_estimate = -1  # You need to set a "not found value. It's important."

            try:
                rating = driver.find_element(By.XPATH, './/span[@data-test="detailRating"]').text
            except NoSuchElementException:
                rating = -1  # You need to set a "not found value. It's important."

            # Printing for debugging
            if verbose:
                print("Job Title: {}".format(job_title))
                print("Salary Estimate: {}".format(salary_estimate))
                print("Job Description: {}".format(job_description[:500]))
                print("Rating: {}".format(rating))
                print("Company Name: {}".format(company_name))
                print("Location: {}".format(location))


            try:
                size = driver.find_element(By.XPATH, '//div[@class="d-flex justify-content-start css-rmzuhb e1pvx6aw0" and ./span[contains(.,"Size")]]/span[2]').text
            except NoSuchElementException:
                size = -1

            try:
                founded = driver.find_element(By.XPATH, '//div[@class="d-flex justify-content-start css-rmzuhb e1pvx6aw0" and ./span[contains(.,"Founded")]]/span[2]').text
            except NoSuchElementException:
                founded = -1

            try:
                type_of_ownership = driver.find_element(By.XPATH, '//div[@class="d-flex justify-content-start css-rmzuhb e1pvx6aw0" and ./span[contains(.,"Type")]]/span[2]').text
            except NoSuchElementException:
                type_of_ownership = -1

            try:
                industry = driver.find_element(By.XPATH, '//div[@class="d-flex justify-content-start css-rmzuhb e1pvx6aw0" and ./span[contains(.,"Industry")]]/span[2]').text
            except NoSuchElementException:
                industry = -1

            try:
                sector = driver.find_element(By.XPATH, '//div[@class="d-flex justify-content-start css-rmzuhb e1pvx6aw0" and ./span[contains(.,"Sector")]]/span[2]').text
            except NoSuchElementException:
                sector = -1

            try:
                revenue = driver.find_element(By.XPATH, '//div[@class="d-flex justify-content-start css-rmzuhb e1pvx6aw0" and ./span[contains(.,"Revenue")]]/span[2]').text
            except NoSuchElementException:
                revenue = -1

            if verbose:
                # print("Headquarters: {}".format(headquarters))
                print("Size: {}".format(size))
                print("Founded: {}".format(founded))
                print("Type of Ownership: {}".format(type_of_ownership))
                print("Industry: {}".format(industry))
                print("Sector: {}".format(sector))
                print("Revenue: {}".format(revenue))
                print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

            jobs.append({"Job Title": job_title,
                         "Salary Estimate": salary_estimate,
                         "Job Description": job_description,
                         "Rating": rating,
                         "Company Name": company_name,
                         "Location": location,
                         # "Headquarters": headquarters,
                         "Size": size,
                         "Founded": founded,
                         "Type of ownership": type_of_ownership,
                         "Industry": industry,
                         "Sector": sector,
                         "Revenue": revenue,
                         # "Competitors": competitors
                         })

        # Clicking on the "next page" button
        try:
            driver.find_element(By.XPATH, './/button[@class="nextButton job-search-opoz2d e13qs2072"]').click()
        except NoSuchElementException:
            print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(num_jobs,len(jobs)))
            break

    return pd.DataFrame(jobs)  # This line converts the dictionary object into a pandas DataFrame.