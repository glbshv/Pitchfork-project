"""**Libraries for the project:**"""

from bs4 import BeautifulSoup
import urllib.request
from urllib.error import URLError, HTTPError
import pandas as pd
from time import sleep

"""**Review page URL constructor:**"""

base_url = 'https://pitchfork.com/reviews/albums/?page='
links_to_review_pages = list()

for i in range(1, 1866):
    links_to_review_pages.append(base_url + str(i))
print('Pages to scrape: ' + str(len(links_to_review_pages)))

"""**This script extracts all Pitchfork review pages:**"""

reviews = []
unscraped_pages = []
failed_pages = []

for link in links_to_review_pages:

  try:
      
    page_reader = urllib.request.urlopen(link).read()

  except HTTPError as error:

        print(link + ' - page scraper failed. Error: ' + str(error.code) + '.')
        unscraped_pages.append(link)

  else:

    print(link + ' - page scraped successfully.')
    output_soup = BeautifulSoup(page_reader, 'lxml')

    filtered_objects = output_soup.find('div', class_='fragment-list')
    
    for review_page in filtered_objects.find_all('a', class_='review__link'):
        string_converter = review_page.get('href')
        result = str(string_converter)
        reviews.append('http://pitchfork.com' + result)  

sleep(30)

if len(unscraped_pages) > 0:
  print('Not all pages were scraped! Re-scraping...')
  for unscraped_link in unscraped_pages:

    try:

      unscraped_page_reader = urllib.request.urlopen(unscraped_link).read()

    except HTTPError as error:

      print(unscraped_link + ' - page scraper failed. Error: ' + str(error.code) + '.')
      failed_pages.append(unscraped_link)

    else:

      print(unscraped_link + '  page scraped successfully.')
      unscraped_soup = BeautifulSoup(unscraped_page_reader, 'lxml')

      filtered_unscraped_objects = unscraped_soup.find('div', class_='fragment-list')

      for review_page in filtered_unscraped_objects.find_all('a', class_='review__link'):
        string_converter = review_page.get('href')
        result = str(string_converter)
        reviews.append('http://pitchfork.com' + result)

print('Scraping completed!')

if len(failed_pages) > 0:
  print('There are failed pages. Please check the failed pages list')
  print(failed_pages)

else:
  print('All pages were scraped.')
  print('Review pages scraped: ' + str(len(reviews)))
  print('Re-scraped pages: ' + str(len(unscraped_pages)))
  print('Pages in error: ' + str(len(failed_pages)))

"""**This part of the program extracts all main variables for the construction of the dataframe:**"""

Artist_Name = []
Album_Name = []
Review_Score = []
Best_New = []
Genre = []
Date_Published = []
Written_by = []
Review_link = []

unscraped_reviews = []
failed_reviews = []

for review in reviews:

    try:
  
      album_review_url = urllib.request.urlopen(review).read()

    except HTTPError as error:

      print(review + ' - page scraper failed. Error: ' + str(error.code) + ".")
      unscraped_reviews.append(review)

    else:

      review_variables = BeautifulSoup(album_review_url,'lxml')


      Artist = review_variables.find('ul', attrs={'class': 'artist-links artist-list single-album-tombstone__artist-links'})
      if Artist is None:
          Artist_Name.append('Not found')
      else:
          artists = []
          for artist_item in Artist.find_all('li'):
            artists.append(artist_item.text)
          artists_to_string = ' / '.join(str(artist_element) for artist_element in artists)
          Artist_Name.append(artists_to_string)
          
      Album = review_variables.find('h1', attrs={'class': 'single-album-tombstone__review-title'})
      if Album is None:
        Album_Name.append('Not found')
      else:
        Album_Name.append(review_variables.find('h1', attrs={'class': 'single-album-tombstone__review-title'}).text)

      Score = review_variables.find('span', attrs={'class': 'score'})
      if Score is None:
        Review_Score.append('')
      else:
        Review_Score.append(float(review_variables.find('span', attrs={'class': 'score'}).text))

      Best_New_Check = review_variables.find('p', attrs={'class': 'bnm-txt'})
      if Best_New_Check is None:
        Best_New.append('')
      else:
        Best_New.append(review_variables.find('p', attrs={'class': 'bnm-txt'}).text)

      Genre_analysis = review_variables.find('ul', attrs={'class': 'genre-list genre-list--before'})
      if Genre_analysis is None:
          Genre.append('Not found')
      else:
        genres = []
        for genre_item in Genre_analysis.find_all('li'):
          genres.append(genre_item.text)
        genres_to_string = ' / '.join(str(genre_element) for genre_element in genres)
        Genre.append(genres_to_string)
      
      Date = review_variables.time
      if Date is None:
        Date_Published.append(Date_Published[-1])
      else:
        Review_Date = review_variables.time['datetime']
        Date_Published.append(Review_Date)

      Author = review_variables.find('a', attrs={'authors-detail__display-name'})
      if Author is None:
        Written_by.append('Not found')
      else:
        Written_by.append(review_variables.find('a', attrs={'authors-detail__display-name'}).text)

      Review_link.append(review)

      print('Review from ' + str(Review_Date)[:10] + ' about artist ' + str(artists_to_string) + ' scraped successfully.')

sleep(30)

if len(unscraped_reviews) > 0:
  print('Not all reviews were scraped! Re-scraping...')

  for unscraped_review in unscraped_reviews:

    try:
  
      unscraped_album_review_url = urllib.request.urlopen(unscraped_review).read()

    except HTTPError as error:

      print(unscraped_review + ' - page scraper failed. Error: ' + str(error.code) + ".")
      failed_reviews.append(review)

    else:

      unscraped_review_variables = BeautifulSoup(unscraped_album_review_url,'lxml')


      Artist = unscraped_review_variables.find('ul', attrs={'class': 'artist-links artist-list single-album-tombstone__artist-links'})
      if Artist is None:
          Artist_Name.append('Not found')
      else:
          artists = []
          for artist_item in Artist.find_all('li'):
            artists.append(artist_item.text)
          artists_to_string = ' / '.join(str(artist_element) for artist_element in artists)
          Artist_Name.append(artists_to_string)
          
      Album = unscraped_review_variables.find('h1', attrs={'class': 'single-album-tombstone__review-title'})
      if Album is None:
        Album_Name.append('Not found')
      else:
        Album_Name.append(unscraped_review_variables.find('h1', attrs={'class': 'single-album-tombstone__review-title'}).text)

      Score = unscraped_review_variables.find('span', attrs={'class': 'score'})
      if Score is None:
        Review_Score.append('')
      else:
        Review_Score.append(float(unscraped_review_variables.find('span', attrs={'class': 'score'}).text))

      Best_New_Check = unscraped_review_variables.find('p', attrs={'class': 'bnm-txt'})
      if Best_New_Check is None:
        Best_New.append('')
      else:
        Best_New.append(unscraped_review_variables.find('p', attrs={'class': 'bnm-txt'}).text)

      Genre_analysis = unscraped_review_variables.find('ul', attrs={'class': 'genre-list genre-list--before'})
      if Genre_analysis is None:
          Genre.append('Not found')
      else:
        genres = []
        for genre_item in Genre_analysis.find_all('li'):
          genres.append(genre_item.text)
        genres_to_string = ' / '.join(str(genre_element) for genre_element in genres)
        Genre.append(genres_to_string)

      Date = unscraped_review_variables.time
      if Date is None:
        Date_Published.append('')
      else:
        Review_Date = unscraped_review_variables.time['datetime']
        Date_Published.append(Review_Date)

      Author = unscraped_review_variables.find('a', attrs={'authors-detail__display-name'})
      if Author is None:
        Written_by.append('Not found')
      else:
        Written_by.append(unscraped_review_variables.find('a', attrs={'authors-detail__display-name'}).text)

      Review_link.append(unscraped_review)

      print('Review from ' + str(Review_Date)[:10] + ' about ' + str(artists_to_string) + ' scraped successfully.')

print('Scraping completed!')

if len(failed_reviews) > 0:
  print('There are failed reviews. Please check the failed review list')
  print(failed_reviews)

else:
  print('All reviews were scraped.')

  print('Reviews scraped: ' + str(len(Review_link)))
  print('Re-scraped pages: ' + str(len(unscraped_reviews)))
  print('Pages in error: ' + str(len(failed_reviews)))
  if len(failed_reviews) > 0:
    print(failed_reviews)

print('SCRIPT TERMINATED')

"""**Creates the Pitchfork review dataframe:**"""

All_review_data = pd.DataFrame({
    'Artist Name': Artist_Name,
    'Album Name': Album_Name,
    'Review Score': Review_Score,
    'Best New Music': Best_New,
    'Genre': Genre,
    'Date Published': Date_Published,
    'Written By': Written_by,
    'Review link': Review_link
})

All_review_data['Date Published'] = All_review_data['Date Published'].str[:10]
All_review_data.set_index('Artist Name', inplace=True)
All_review_data.to_csv('Pitchfork.csv')

print('Report saved')