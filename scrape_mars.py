# Dependencies
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from splinter import browser
from selenium import webdriver

# Define the scrape function for web scrapping from the all the URL's 
def scrape():
    # Create a dict for mars data collected using web scrapping
    mars_results = {}
    ######################################################################################
    ## NASA MARS NEWS
    ######################################################################################
    
    # News URL
    url = "https://mars.nasa.gov/news"
    # Use selenium webdriver to retrieve the page information
    driver = webdriver.Firefox()
    driver.get(url)
    html = driver.page_source
    # Scrape the webpage using beautiful soup
    soup = bs(html, 'html.parser')
    driver. quit() 
    # Latest title and remove the new line 
    news_title = soup.find('div', class_ = 'content_title').get_text(strip=True)
    # Latest Paragraph
    news_p = soup.find('div', class_ = 'article_teaser_body').get_text()
    mars_results["News_title"] = news_title
    mars_results["News_p"] = news_p

    ######################################################################################
    #### Featured Image
    ######################################################################################

    # Featured Image URL
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    # Retrieve page with the requests module
    response = requests.get(image_url)
    # Scrape the webpage using beautiful soup
    soup = bs(response.text, 'html.parser')
    # Featured URL
    featured_url = soup.find("article", class_="carousel_item")["style"]
    featured_url = featured_url.strip("background-image: url('")
    featured_url = featured_url.strip("');")
    featured_image_url = "https://www.jpl.nasa.gov" + featured_url
    mars_results["featured_image_url"] = featured_image_url
    
    ######################################################################################
    #### Latest_weather
    ######################################################################################

    # Wether URL
    weather_url = "https://twitter.com/marswxreport?lang=en"
    # Use selenium webdriver to retrieve the page information
    response = requests.get(weather_url)
    driver = webdriver.Firefox()
    driver.get(weather_url)
    html = driver.page_source
    # Scrape the webpage using beautiful soup
    soup = bs(response.text, 'html.parser')
    driver. quit() 
    # Extract the tweet text
    mars_weather = soup.find(class_='tweet-text').text
    mars_results["mars_weather"] = mars_weather
    
    ######################################################################################
    #### Mars Facts
    ######################################################################################
    
    # Mars Facts URL
    facts_url = "http://space-facts.com/mars/"
    
    # Convert the data to html
    data = pd.read_html(facts_url)
    # Convet the html to the pandas DataFrame
    df = data[0]
    df.columns = ["Fact","Value"]
    # Get rid of trailing colon
    df["Fact"] = df["Fact"].str[:-1]
    df = df.set_index("Fact")
    # Convert he data to html to display the scraped info as an html table
    facts_html_table = df.to_html()
    facts_html_table = facts_html_table.replace('\n', '')
    mars_results['facts_html_table'] = facts_html_table
    
    ######################################################################################
    #### Hemisphere_info
    ######################################################################################

    # Mars Hemisphere URL 
    hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    # Retrieve page with the requests module
    response = requests.get(hemisphere_url)
    # Scrape the webpage using beautiful soup
    soup = bs(response.text, 'html.parser')
    
    # Create an empty list to get title and url details
    hemi_img_url_list = []
    title = []
    for item in soup.select("a.itemLink"):
        # title
        title.append(item.select("h3")[0].get_text())
        # URL for the image
        url_new = "https://astrogeology.usgs.gov"+item["href"]
        response_new = requests.get(url_new)
        soup_new = bs(response_new.text, 'html.parser')
        hemi_img_url_list.append("https://astrogeology.usgs.gov"+soup_new.select('img.wide-image')[0]['src'])
        hemisphere_image_urls = [{"Title":title[i],'img_url':hemi_img_url_list[i]} for i in range(len(title))]
        
    mars_results["hemisphere_image_urls"] = hemisphere_image_urls
    return mars_results
    