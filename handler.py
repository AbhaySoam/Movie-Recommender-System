from MovieLens import MovieLens
from surprise import SVD
from ContentRecs import getContentBasedRecs
from UserCFRecs import getUserCFRecs
import random

class RecSys:
    ml, data, testSubject = None, None, None
    def BuildAntiTestSetForUser(self, testSubject, trainset):
        fill = trainset.global_mean

        anti_testset = []
        
        u = trainset.to_inner_uid(str(testSubject))
        
        user_items = set([j for (j, _) in trainset.ur[u]])
        anti_testset += [(trainset.to_raw_uid(u), trainset.to_raw_iid(i), fill) for
                                i in trainset.all_items() if
                                i not in user_items]
        return anti_testset

    def getAllMovieNames(self):
        self.ml = MovieLens()
        return self.ml.getAllMovieNames()
    
    def loadMlData(self, newUserRatings):
        self.testSubject = 672   #change to new user

        print("Loading movie ratings...")
        self.ml.loadMovieLensLatestSmall()

        updatedUserRatings = []
        for ratingList in newUserRatings:
            ratingList = [self.testSubject, self.ml.getMovieID(ratingList[0]), ratingList[1], 0]
            updatedUserRatings.append(ratingList)
        self.ml.append_new_rating_list_as_row(updatedUserRatings)

        self.data = self.ml.getMLRatingsDataset()

        return self.ml


    def startRecSys(self):
        
        userRatings = self.ml.getUserRatings(self.testSubject)
        #print(userRatings[:10])  #remove
        loved = []
        hated = []
        for ratings in userRatings:
            if (float(ratings[1]) >= 3.0):
                loved.append(ratings)
            if (float(ratings[1]) < 3.0):
                hated.append(ratings)

        print("\nUser ", self.testSubject, " loved these movies:")
        for ratings in loved:
            print(self.ml.getMovieName(ratings[0]))
        print("\n...and didn't like these movies:")
        for ratings in hated:
            print(self.ml.getMovieName(ratings[0]))

        print("\nBuilding recommendation model...")
        trainSet = self.data.build_full_trainset()
        
        print("Computing recommendations...")
        #for top 10 recommendations using User-based Collaborative filtering
        userCFRecs = getUserCFRecs(str(self.testSubject), trainSet)

        #for top 10 recommendations using Content-based filtering
        #contentBasedRecs = getContentBasedRecs(self.testSubject, trainSet)    ##uncomment to use content-based filtering also
        
        #userCFRecs.extend(contentBasedRecs)               ##uncomment to use content-based filtering also
        recommendations = userCFRecs

        print ("\nRecommendations Ready:")
        print('\nBefore shuffling')
        for ratings in recommendations:
            print(self.ml.getMovieName(ratings[0]))
        
        random.shuffle(recommendations)
        print('\n\nAfter shuffling')
        for ratings in recommendations:
            print(self.ml.getMovieName(ratings[0]))
        return recommendations
        