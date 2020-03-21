from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import pandas as pd
import time
# import pymongo


def scrape():
    # URL of page to be scraped
    nasa_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    # Retrieve page with the requests module
    response = requests.get(nasa_url)
    soup = bs(response.text, 'html.parser')
    titles = soup.find_all('div', class_="content_title")
    paragraphs = soup.find_all('div', class_="rollover_description_inner")
    # News
    news_title = titles[0].text.replace('\n','')
    news_p = paragraphs[0].text.replace('\n','').replace('\'''s','')

    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    JPL_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(JPL_url)
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(2)
    browser.click_link_by_partial_text('more info')
    browser.click_link_by_partial_text('.jpg')
    # featured image url
    featured_image_url = browser.url
    browser.quit()


    weather_url ="https://twitter.com/marswxreport?lang=en"
    weather_response = requests.get(weather_url)
    weather_soup = bs(weather_response.text, 'html.parser')
    twitters = weather_soup.find_all('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")
    weathers = []

    for twitter in twitters:
        if "sol" in str(twitter.text):
            weathers.append(twitter.text)
    # mars weather
    mars_weather = weathers[0]
    

    facts_url="https://space-facts.com/mars/"
    tables = pd.read_html(facts_url)

    for table in tables:
        try:
            df= table
            df.columns = ['Description','Value']
            # df = df.set_index('Description')
        except:
            pass
    # facts table 


    H_url ="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    H_response = requests.get(H_url)
    H_soup = bs(H_response.text, 'html.parser')
    # print(H_soup.prettify())
    Enhanceds = H_soup.find_all('h3')

    Enhanced_titles=[]
    for Enhanced in Enhanceds:
        Enhanced_titles.append(Enhanced.text)
    # Enhanced img url
    img_url=[]
    i = 1

    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    H_browser = Browser('chrome', **executable_path, headless=False)
    H_browser.visit(H_url)

    for Enhanced in Enhanced_titles:
        H_browser.click_link_by_partial_text(Enhanced)
        H_browser.click_link_by_partial_text('Sample')
        time.sleep(3)
        img_url.append(H_browser.windows[i].url)
        H_browser.back()
        i = i+1
    H_browser.quit()


    # hemisphere image urls
    hemisphere_image_urls = []

    for x in range(len(Enhanced_titles)): 
        dic = {"title":Enhanced_titles[x],"img_url":img_url[x]}
        hemisphere_image_urls.append(dic)

    factTable = df.to_html(header="true", index=False)


    scrape_data = {
        "news_title":news_title,
        "news_p":news_p,
        "featured_image_url" : featured_image_url,
        "mars_weather":mars_weather,
        "factTable":factTable,
        "img_url":img_url,
        "hemisphere_image_urls":hemisphere_image_urls
    }
    
    return scrape_data



        










