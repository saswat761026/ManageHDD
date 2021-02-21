from jikanpy import Jikan
jikan = Jikan()

mushishi = jikan.anime(39617)
mushishi_with_eps = jikan.anime(21, extension='episodes', page=10)

search_result = jikan.search('anime', 'One Piece', page=1)

winter_2018_anime = jikan.season(year=2021, season='winter')

archive = jikan.season_archive()

for anime in winter_2018_anime['anime']:
    if anime['title'] == 'One Piece':
        print(anime)


print(archive)
print(winter_2018_anime)
print(search_result)

