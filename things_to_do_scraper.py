import sys
import csv
from selenium import webdriver
import time

# default path to file to store data
path_to_file = "reviews_Pompeii_3.csv"

# default number of scraped pages
num_pages = 120

# default tripadvisor website of hotel or things to do (attraction/monument)
url = "https://www.tripadvisor.it/Attraction_Review-g187786-d195477-Reviews-Pompeii_Archaeological_Park-Pompeii_Province_of_Naples_Campania.html"

# default language
language = "en"

# default rating
rating = 3

# if you pass the inputs in the command line
if len(sys.argv) == 6:
    path_to_file = sys.argv[1]
    num_pages = int(sys.argv[2])
    url = sys.argv[3]
    language = sys.argv[4]
    rating = sys.argv[5]

# import the webdriver
driver = webdriver.Safari()


def set_rating(rating):
    # Define the javascript to select rating
    select_rating_js = """
                document.evaluate(".//input[@type='checkbox'][@value='__RATING__']", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click();
                """.replace("__RATING__", str(rating))

    # Run the script
    driver.execute_script(select_rating_js)


def set_language(language):
    # Define the javascript to select language
    select_language_js = """
               document.evaluate(".//input[@type='radio'][@value='__LANGUAGE__']", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click();
               """.replace("__LANGUAGE__", language)

    # Run the script
    driver.execute_script(select_language_js)


def next_page():
    # Define the javascript to select language
    next_page_js = """
               document.evaluate(".//a[@class='ui_button nav next primary ']", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click();
               """

    # Run the script
    driver.execute_script(next_page_js)


def check_autotranslate():
    # Define check javascript
    check_autoTranslate_js = """
    let autoTranslate=document.evaluate(".//input[@id='autoTranslateNo']", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
    if (autoTranslate!=null) {
        autoTranslate.click();
        return true;
    }
    """

    # Run the script
    return driver.execute_script(check_autoTranslate_js)


def show_more():

    # Define the show more javascript
    show_more_js = """
    document.evaluate(".//div[contains(@data-test-target, 'expand-review')]", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click();
    """

    # Run the script
    driver.execute_script(show_more_js)

# open the file to save the review
csvFile = open(path_to_file, 'w', encoding="utf-8")
csvWriter = csv.writer(csvFile)
csvWriter.writerow(["date", "rating", "title", "review"])

# Get the url
print("URL:", url)
driver.get(url)

# change the value inside the range to save more or less reviews
for num_page in range(0, num_pages):
    print("Exploring:", num_page)
    # Wait few seconds
    time.sleep(10)

    if num_page == 0:
        set_rating(rating)
        set_language(language)


    if check_autotranslate() is True:
        time.sleep(10)
        break

    # go to the next page
    next_page()


# change the value inside the range to save more or less reviews
for num_page in range(0, num_pages):

    print("Downloading:",num_page)

    # Wait few seconds
    time.sleep(10)

    if check_autotranslate() is True:
        # Wait few seconds
        time.sleep(20)

    # Wait for response
    time.sleep(10)

    # expand the review
    show_more()
    time.sleep(5)

    # get the reviews
    reviews = driver.find_elements_by_xpath("//div[@data-reviewid]")

    # get the number of reviews per page
    reviews_per_page = len(reviews)

    # get the container of the dates
    dates = driver.find_elements_by_xpath(".//div[@class='_2fxQ4TOx']")

    # for each review...
    for j in range(reviews_per_page):
        # Get the rating
        rating = reviews[j].find_element_by_xpath(".//span[contains(@class, 'ui_bubble_rating bubble_')]").get_attribute(
            "class").split("_")[3]

        # Get the title
        title = reviews[j].find_element_by_xpath(".//div[contains(@data-test-target, 'review-title')]").text

        # Get the review body
        review = reviews[j].find_element_by_xpath(".//q[@class='IRsGHoPm']").text.replace("\n", "  ")

        # Get the review date
        date = " ".join(dates[j].text.split(" ")[-2:])

        print(date, rating, title)
        csvWriter.writerow([date, rating, title, review])

    # go to the next page
    next_page()

driver.quit()