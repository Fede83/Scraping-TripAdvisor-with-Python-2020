import sys
import csv
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from random import randint


# default path to file to store data
path_to_file = "reviews.csv"

# default number of scraped pages
num_pages = 1

# default tripadvisor website of hotel or things to do (attraction/monument) 
url = "https://www.tripadvisor.it/Attraction_Review-g187786-d195477-Reviews-Pompeii_Archaeological_Park-Pompeii_Province_of_Naples_Campania.html"
#url = "https://www.tripadvisor.com/Attraction_Review-g187791-d192285-Reviews-Colosseum-Rome_Lazio.html"

# default language
language = "en"

# if you pass the inputs in the command line
if len(sys.argv) == 5:
    path_to_file = sys.argv[1]
    num_pages = int(sys.argv[2])
    url = sys.argv[3]
    language = sys.argv[4]

# import the webdriver
driver = webdriver.Safari()

# open the file to save the review
csvFile = open(path_to_file, 'w', encoding="utf-8")
csvWriter = csv.writer(csvFile)
csvWriter.writerow(["date", "rating", "title", "review"])

# change the value inside the range to save more or less reviews
for i in range(0, num_pages):

    # Get the url
    print("URL:", url)
    driver.get(url)

    # Wait few seconds
    time.sleep(randint(2, 7))

    # Define the javascript for select language
    select_language_js = """
        document.evaluate(".//input[@type='radio'][@value='__LANGUAGE__']", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click();
        """.replace("__LANGUAGE__", language)

    # Run the script
    driver.execute_script(select_language_js)

    # Wait for response
    time.sleep(2)

    # expand the review
    driver.find_element_by_xpath(".//div[contains(@data-test-target, 'expand-review')]").click()

    # get the reviews
    reviews = driver.find_elements_by_xpath("//div[@data-reviewid]")

    # get the number of reviews per page
    reviews_per_page = len(reviews)

    # get the container of the dates
    dates = driver.find_elements_by_xpath(".//div[@class='_2fxQ4TOx']")

    # for each review...
    for j in range(reviews_per_page):

        # Get the rating
        rating = reviews[j].find_element_by_xpath(".//span[contains(@class, 'ui_bubble_rating bubble_')]").get_attribute("class").split("_")[3]

        # Get the title
        title = reviews[j].find_element_by_xpath(".//div[contains(@data-test-target, 'review-title')]").text

        # Get the review body
        review = reviews[j].find_element_by_xpath(".//q[@class='IRsGHoPm']").text.replace("\n", "  ")

        # Get the review date
        date = " ".join(dates[j].text.split(" ")[-2:])

        print(date, rating, title)
        csvWriter.writerow([date, rating, title, review])
        
    # get the next url
    url = driver.find_element_by_xpath('.//a[@class="ui_button nav next primary "]').get_attribute("href")

driver.quit()
