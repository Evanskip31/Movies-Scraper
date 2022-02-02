# importing the required libraries
import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import re



# url to the landing page of the site
movie_website_url = 'https://yts.mx/browse-movies'

# set the headers, this will make the site think that requests are being made from a web browser
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36'}

page = requests.get(movie_website_url, headers=headers)

soup = BeautifulSoup(page.content, 'html.parser')

# getting the number of pages to be scraped
number_of_pages = soup.find('ul', {'class':'tsc_pagination tsc_paginationA tsc_paginationA06'})
page_save = []
for items in number_of_pages:
    page_number = items.find('a')
    if type(page_number) == int or not page_number:
        continue
    else:
        page_save.append(items.get_text())

# we now have the list of pages, in it the very last page
page_numbers = int(page_save[-3])
print(range(1, page_numbers+1))

# we need to save the link to each movie, because we'll open each to get more details
# we will need a dictionary for this. where we can append the links, movie titles and other details
movie_details = {}

#creating a loop that will parse through each of the pages
for page in range(1, page_numbers+1):
    #setting url to the current page number
    new_website_url = f'https://yts.mx/browse-movies?page={page}'
    print(new_website_url)
    new_page = requests.get(new_website_url, headers=headers)
    
    soup = BeautifulSoup(new_page.content, 'html.parser')
    
    # getting the total number of uploaded movies
    number_of_movies = soup.find_all('h2')
    # other options to consider
    # total_movies = soup.find_all('div', {'class':'browse-content'})
    # total_movies_text = total_movies[0].find('h2')
    
    movie_wrap = soup.find_all('div',{'class':"browse-movie-wrap"})
    
    
    for item in movie_wrap:
        movie_link = item.find('a', {'class':'browse-movie-link'})
        movie_link = movie_link['href']
        
    
    # looping through the elements to obtain movie title and year
    for each in movie_wrap:
        # getting title
        link = each.find('a', {'class':'browse-movie-title'})
        movie_name_raw = link.get_text()
        format_text  = re.findall(r'\[.*?\]', movie_name_raw)
        new_text = str(format_text).strip('[""]')
        new_text = new_text.strip("''")
        language = new_text.strip('[]')
        print(language)
        if language in movie_name_raw:
            movie_name = movie_name_raw.replace(language, '')
            if '[]' in movie_name:
                movie_name = movie_name.replace('[]', '')
                movie_name = movie_name[1:]
            if not language:
                language = 'ENG'
            print(movie_name, language)
        
        # getting year from its bs4 element
        year_element = each.find('div', {'class':'browse-movie-year'})
        year = year_element.get_text()
        
        # getting the movie link from bs4 element
        movie_link = each.find('a', {'class':'browse-movie-link'})
        movie_link = movie_link['href']
        
        # obtaining the rating and genre
        movie_type = each.find('figcaption')
        movie_type_all = movie_type.find_all('h4')
        genre = ''
        rating = ''
        for every in movie_type_all:
            if '/' in every.get_text():
                rating = every.get_text()
            else:
                if not genre:
                    genre += every.get_text()
                else:
                    genre += ' / ' + every.get_text()
        if not rating:
            rating = ''
        
        # opening the page link for more details
        details_page = requests.get(movie_link, headers=headers)
        
        page_soup = BeautifulSoup(details_page.content, 'html.parser')
        
        #verifying the present details
        movie_info = page_soup.find_all('div', {'id': 'movie-info'})
        
        for each in movie_info:
            verify = each.find('div', {'class':'hidden-xs'})
        
        # just to verify the year and genre of the movie if all were added well
        movie_info = verify.find_all('h2')
        year_verify = movie_info[0].get_text()
        genre_verify = movie_info[1].get_text()
        
        # getting the trailer link
        trailer_link = page_soup.find_all('div', {'id':'screenshots'})
        
        for trailer in trailer_link:
            youtube_links = trailer.find('div',{'class':'screenshot'})
        
        youtube_link = youtube_links.find('a', {'class':'youtube'})
        trailer_link = youtube_link['href']
        
        # obtaining the synopsis of the movie / short story and date uploaded
        synopsis = page_soup.find_all('div', {'id':'synopsis'})
        
        for synopses in synopsis:
            synopsis_text = synopses.find('p', {'class':"hidden-xs"})
            date_uploaded = synopses.find('span', {"itemprop":"dateCreated"})
            
        synopsis_text = synopsis_text.get_text()
        date_uploaded_raw = date_uploaded.get_text()
        
        #clean the date_uploaded_raw to get the date and time separately
        z = 0
        for i,m in enumerate(date_uploaded_raw):
            if date_uploaded_raw[z] == 'a' and date_uploaded_raw[i] == 't':
                k = z
            z = i
        date_uploaded = date_uploaded_raw[:k-1]
        time_uploaded = date_uploaded_raw[k+3:]
        
        # let's get the director and actors of the movie
        all_cast = page_soup.find_all('div', {'id':'crew'})
        for cast in all_cast:
            director = cast.find('div', {'class':'directors'})
            actors = cast.find('div', {'class':'actors'})
        
        # get the list of director names - make a list to save them in case they are more than one 
        director_list = []
        for each in director.find_all('div', {'class':'list-cast-info'}):
            director_name = each.get_text()
            director_list.append(director_name)
        
        # let's remove new lines added director_list
        new_director_list = []
        for i in director_list:
            if '\n' in i:
                new_director = i.replace('\n', '')
                new_director_list.append(new_director)
        
        # strip the list to get strings concatenated together
        all_director = ''
        for director in new_director_list:
            if len(new_director_list) == 1:
                all_director += new_director_list[0]
            else:
                if not all_director:
                    all_director += director
                else:
                    all_director += ' / ' + director
        
        # get the list of director names - make a list to save them in case they are more than one 
        actor_list = []
        for actor in actors.find_all('div', {'class':'list-cast-info'}):
            actor_name = actor.get_text()
            actor_list.append(actor_name)
        
        # let's remove new lines added actor_list
        new_actor_list = []
        for i in actor_list:
            if '\n' in i:
                new_actor = i.replace('\n', '')
                new_actor_list.append(new_actor)
            
        # let's make things even more interesting by separating the actor names
        all_cast = ''
        all_actors = ''
        for item in new_actor_list:
            x = 0
            for i,m in enumerate(item):
                if item[x] == 'a' and item[i] == 's':
                    j = x
                    l = i
                    print(x, i)
                x = i
            # getting cast name and concatenating all of them
            cast_name = item[l+2:]
            if not all_cast:
                all_cast += cast_name
            else:
                all_cast += ' / ' + cast_name
                
            # getting the real names and concatenating all of them
            real_name = item[:k-1]
            if not all_actors:
                all_actors += real_name
            else:
                all_actors += ' / ' + real_name
            print(cast_name, real_name)
            
        # concatenate year and name to get the movie title which will be our primary key
        movie_title = movie_name+' - '+year
        movie_details[movie_title] = defaultdict(list)
        movie_details[movie_title]['Properties'].append({'Year': year,'language': language, 'Genre': genre, 'Rating': rating, 'Movie Link': movie_link})
        
        
    print(f'{page} finished!')
    print('\n')
    
# we now have the basic details. we need to get into each link and obtain more details
# since we saved the link to each movie, we can easily do that
for item in movie_details.keys():
    item_properties = movie_details[item]['Properties']
    for each in item_properties:
        new_properties_url = each['Movie Link']
    # we now use the link we obtained above to access its page
    details_page = requests.get(new_properties_url, headers=headers)