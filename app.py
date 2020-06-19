from flask import Flask, render_template, request, session
from flask_session import Session
from handler import RecSys
from MovieLens import MovieLens

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

recSys = RecSys()
allMovieNames = recSys.getAllMovieNames()

@app.route('/')
def welcome():
    return render_template('welcome_to.html')

@app.route("/index", methods=["GET", "POST"])
def index():

	if request.method == "GET":
		session["userRatings"] = []
	if request.method == "POST":
		name = request.form.get("movieName")
		rating = float(request.form.get("rating"))
		session["userRatings"].append([name, rating])
	return render_template("index.html", userRatings=session["userRatings"], allMovieNames=allMovieNames)

@app.route("/yourRecommendations", methods=["POST"])
def usersRecommendations():
	
	ml = recSys.loadMlData(session['userRatings'])
	print(session['userRatings'])  #remove
	
	recommendations = recSys.startRecSys()

	count, maxMoviesOnPage = 0, 15
	moviesList = []
	for ratings in recommendations:
		movieName = ml.getMovieName(ratings[0])
		movieName = movieName[ : movieName.rfind('(')-1]
		### remove , The at the end of name   **important
		if movieName.endswith(", The"):
			movieName = "The " + movieName[: len(movieName)-5]
		youtubeId = ml.getYoutubeId(ratings[0])  
		movieDetails = ml.getMovieDetailsFromOMDB(movieName)
		if movieDetails['Title'] == 'key not found!':  #if movie details not found on omdb continue
			continue
		movieDetails['YoutubeID'] = youtubeId   # add 'youtubeId to movieDetails Dict
		#update Ratings list to only imdb rating
		ratingsList = movieDetails['Ratings']
		imdbDict = ratingsList[0]
		movieDetails['Ratings'] = imdbDict['Value']
		#update genre to max 2 and director to 1 only
		allGenre = movieDetails['Genre']
		secondCommaPos = allGenre.find(',', allGenre.find(',')+1)
		if(secondCommaPos != -1):
			movieDetails['Genre'] = allGenre[: secondCommaPos]
		commaPos = movieDetails['Director'].find(',')
		if(commaPos != -1):
			movieDetails['Director'] = movieDetails['Director'][: commaPos]
		
		moviesList.append(movieDetails)
		count += 1
		if count == maxMoviesOnPage:
			break

	session["movies"] = moviesList
	
	return render_template("usersPage.html",movies=session["movies"])


