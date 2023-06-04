from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import project

url = "https://www.imdb.com/chart/top"
req = Request(
    url, 
    headers={'User-Agent': 'Mozilla/109.0'}
)
webpage = urlopen(req).read()

soup = BeautifulSoup(webpage,features="lxml")

movies = soup.select("td.titleColumn")
# create query
createQuery = f'create table imdb (title string,rank int,budget int,imdb_rating float,year int,director string,voters int,genre string,cast string,country string,language string)'
project.handle_input(project.split(createQuery))
for idx, movie in enumerate(movies):
    try:
        title = movie.select_one("a").text
        link = movie.select_one("a").get("href")
        rank = idx + 1
        print(rank,title)
        # open the link and get 
        movie_url = "https://www.imdb.com" + link
        request = Request(movie_url, headers={'User-Agent': 'Mozilla/109.0'})
        movie_response = urlopen(request).read()
        movie_soup = BeautifulSoup(movie_response, features="lxml")
        title = movie_soup.select_one("div h1").text
        # rating with classes sc-7ab21ed2-1 eUYAaq
        imdb_rating = movie_soup.select_one("span.sc-7ab21ed2-1.eUYAaq").text
        print("IMDB rating:",imdb_rating)
        year = movie_soup.find("a",class_="ipc-link ipc-link--baseAlt ipc-link--inherit-color sc-8c396aa2-1 iOtMms").text
        print("Year:",year)
        # get the director
        director = movie_soup.find("a",class_="ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link").text
        print("Director:",director)
        voters = movie_soup.find("div",class_="sc-7ab21ed2-3 iDwwZL").text
        print("Voters Count:",voters)
        genre = movie_soup.select_one("span.ipc-chip__text").text
        print("Genre",genre)
        cast = movie_soup.select("a.sc-bfec09a1-1.fUguci")
        castList = [x.text for x in cast]

        print("Cast:",*castList)
        budget = movie_soup.find("li",{"data-testid":"title-boxoffice-budget"}).find("label",class_="ipc-metadata-list-item__list-content-item").text
        print("Budget:",budget)
        country = movie_soup.find("li",{"data-testid":"title-details-origin"}).find("a",class_="ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link").text
        print("Country:",country)
        language = movie_soup.find("li",{"data-testid":"title-details-languages"}).find("a",class_="ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link").text
        print("Language:",language)
        # budget to int
        budget = budget.replace(",","")
        try:
            budget = int(budget.split()[0][1:])
            # voters to int (2M)
            if voters[-1] == "M":
                voters = int(float(voters[:-1])*1000000)
            elif voters[-1] == "K":
                voters = int(float(voters[:-1])*1000)
            else:
                voters = int(voters)

        except:
            pass
        
        # insert query
        insertQuery = f'insert into imdb values ("{title}",{rank},{budget},{imdb_rating},{year},"{director}",{voters},"{genre}","{castList}","{country}","{language}")'
        project.handle_input(project.split(insertQuery))
    except:
        print("Error in movie:",title)