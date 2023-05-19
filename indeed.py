import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://www.indeed.com/jobs?q=python&limit={LIMIT}"


def get_last_page():
    pages = []  #list -> mutable
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")
    links = soup.find("div", {"class": "pagination"}).find_all('a')
    for link in links[:-1]:
        pages.append(int(link.string))
    max_page = pages[-1]
    return max_page


def extract_job(html):
    #Extract title
    title = html.find("h2", {"class": "title"}).find("a")["title"]
    #Extract company's name
    company = html.find("span", {"class": "company"})
    if company:
      company_anchor = company.find("a")
      if company_anchor is not None:
          company = str(company_anchor.string)
      else:
          company = str(company.string)
    else:
      company = None      
    #Extract company's location
    location = html.find("div", {"class": "recJobLoc"})["data-rc-loc"]
    #Extract detail link
    job_id = html["data-jk"]
    return {
        'title': title,
        'company': company,
        'location': location,
        "link": f"https://www.indeed.com/viewjob?jk={job_id}"
    }


def extract_jobs(last_page):
  jobs = []
  for page in range(last_page):
    print(f"Scrapping indeed: page: {page}")
    result = requests.get(f"{URL}&start={page*LIMIT}")
    #print(result.status_code)
    #status_code가 200이면 request가 잘 작동했다는 의미
    soup = BeautifulSoup(result.text, "html.parser")
    results = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})
    for result in results:
        job = extract_job(result)
        jobs.append(job)
  return jobs


def get_jobs():
  last_page = get_last_page()
  jobs = extract_jobs(2)
  return jobs