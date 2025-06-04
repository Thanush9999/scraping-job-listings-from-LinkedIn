import requests as rq
from bs4 import BeautifulSoup as bs
import csv
import json

# Define LinkedIn job search URL and parameters
linkedin_url = "https://www.linkedin.com/jobs/search"
query_string = {
    "keywords": "Python Developer",  # Updated Job Title
    "location": "Bangalore",         # Updated Location
    "trk": "public_jobs_jobs-search-bar_search-submit"  # LinkedIn Tracking
}

# Sending GET request to LinkedIn
response = rq.get(linkedin_url, params=query_string)

# Verify response status
if response.status_code == 200:  # Checks if request was successful
    content = bs(response.content, 'html.parser')

    # Extract job listings
    vacancy_list = content.select(".jobs-search__results-list li")

    vacancies_list = []
    
    # Loop through extracted job postings
    for vacancy in vacancy_list:
        try:
            title = vacancy.select_one(".base-search-card__title").text.strip()
            company = vacancy.select_one(".base-search-card__subtitle").text.strip()
            location = vacancy.select_one(".job-search-card__location").text.strip()
            url = vacancy.select_one(".base-card__full-link")['href']
            date = vacancy.select_one("time")["datetime"]
            
            # Store extracted details in a dictionary
            info = {
                "Title": title,
                "Company": company,
                "Location": location,
                "URL": url,
                "Date": date
            }
            vacancies_list.append(info)
        
        except AttributeError:
            print("Skipping an entry due to missing data.")

    # Save data to JSON file
    with open("vacancies.json", "w", encoding="utf-8") as json_archive:
        json.dump(vacancies_list, json_archive, ensure_ascii=False, indent=4)

    # Save data to CSV file
    with open("vacancies.csv", mode="w", encoding="utf-8", newline="") as csv_file:
        header = ["Title", "Company", "Location", "URL", "Date"]
        generator_csv = csv.DictWriter(csv_file, fieldnames=header)
        generator_csv.writeheader()
        generator_csv.writerows(vacancies_list)

else:
    print(f"Failed to retrieve page. Status code: {response.status_code}")
