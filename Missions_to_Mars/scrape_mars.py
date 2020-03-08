# Dependencies
import pandas as pd
import requests as req
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pymongo
import time

def init_browser():
   
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
   
    browser = init_browser()

# NASA Mars New
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(3)
    html=browser.html

    soup=bs(html, 'html.parser')

    news_title=soup.find('div',class_="list_text").find('div',class_="content_title").text
    print(news_title)
    news_p=soup.find('div',class_="list_text").find('div',class_="article_teaser_body").text
    print(news_p)


# JPL Mars Sapce Image
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    time.sleep(3)
    html=browser.html

    soup=bs(html, 'html.parser')

    main_url='https://www.jpl.nasa.gov'

    path_url=browser.find_by_xpath('//*[@id="page"]/section[1]/div/div/article')['style']
    path_url.find('("') #len:21
    path_url.find('")') #len:75
    featured_url=path_url[21+len('("'):75]

    featured_image_url=f'{main_url}{featured_url}'
    print(featured_image_url)

# Mars Weather
    url = "https://twitter.com/marswxreport?lang=en"
    html_content = req.get(url).text

    soup = bs(html_content, "lxml")
    twitter_list = soup.find_all('div', class_="js-tweet-text-container")

    weather_data = []
    for item in twitter_list: 
        body_text = item.find('p').text
        if 'InSight' and 'sol' in body_text:
            weather_data.append(body_text)        
        break
    mars_twitter=weather_data[0]

# Mars Facts
    url="https://space-facts.com/mars/"
    browser.visit(url)
    time.sleep(3)

    tables = pd.read_html(url)
    df = tables[0]
    mars_table = df.to_html(buf=None, columns=None, col_space=None, header=False, index=False, na_rep='NaN', index_names=False, justify='right', bold_rows=True, classes=None, escape=True, max_rows=None, max_cols=None, show_dimensions=False, notebook=False, decimal='.', border=1)

# Mars Hemispheres
    cerberus_url="https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced"
    schiaparelli_url="https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced"
    syrtis_major="https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced"
    valles_marineris="https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced"
   
    list_urls=[cerberus_url,schiaparelli_url,syrtis_major,valles_marineris]

    hemisphere_image_urls_list=[]

    for img_url in list_urls:
        browser.visit(img_url)
        html=browser.html
        soup=bs(html, 'html.parser')
   
        raw_title=soup.find('h2',class_='title').text
        title=raw_title.replace("Enhanced","")
    
        img=soup.find('img',class_='wide-image')["src"]
        img_url=f'https:astrogeology.usgs.gov{img}'
    
        hemisphere_image_urls={}
        hemisphere_image_urls['title']=title
        hemisphere_image_urls['img_url']=img_url    
        hemisphere_image_urls_list.append(hemisphere_image_urls)
       
    hemisphere_image_urls_list
# Create a dictionary to hold all scraped values
    mars_dict={}
    mars_dict["news_title"]=news_title
    mars_dict["news_p"]=news_p
    mars_dict["mars_twitter"]=mars_twitter
    mars_dict['table']=mars_table
    mars_dict['featured_image_url']=featured_image_url
    mars_dict['hemispher_image_url_list']=hemisphere_image_urls_list


    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_dict 


