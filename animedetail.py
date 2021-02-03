from jikanpy import Jikan
jikan = Jikan()

mushishi = jikan.anime(39617)
mushishi_with_eps = jikan.anime(21, extension='episodes', page=10)

search_result = jikan.search('anime', 'One Piece', page=1)

winter_2018_anime = jikan.season(year=2021, season='winter')

archive = jikan.season_archive()

print(archive)
print(winter_2018_anime)
print(search_result)

# Check isStarting date passed
# if true
# check is present in downloads or not 
# if yes
# check its download date and from that date to present
# else
# check for prequel:
# if yes:
# then download from airing_day-1 till present day
# else:

# check the dir logs 
# if name exists 
# then long running and get last episode prsent
#else: 
#new series and download it from airing date

