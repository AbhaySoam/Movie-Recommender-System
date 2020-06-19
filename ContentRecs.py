
from MovieLens import MovieLens
from ContentKNNAlgorithm import ContentKNNAlgorithm

import random
import numpy as np

def LoadMovieLensData():
    ml = MovieLens()
    print("Loading movie ratings...")
    data = ml.getMLRatingsDataset()
    print("\nComputing movie popularity ranks so we can measure novelty later...")
    rankings = ml.getPopularityRanks()
    return (ml, data, rankings)


def BuildAntiTestSetForUser(testSubject, trainset):
    fill = trainset.global_mean

    anti_testset = []
    
    u = trainset.to_inner_uid(str(testSubject))
    
    user_items = set([j for (j, _) in trainset.ur[u]])
    anti_testset += [(trainset.to_raw_uid(u), trainset.to_raw_iid(i), fill) for
                             i in trainset.all_items() if
                             i not in user_items]
    return anti_testset

def getContentBasedRecs(testSubject, trainSet):
    np.random.seed(0)
    random.seed(0)
    
    # Load up common data set for the recommender algorithms
    #(ml, evaluationData, rankings) = LoadMovieLensData()
    
    #testSubject = 85
    contentKNN = ContentKNNAlgorithm()
    
    #dataset = evaluationData
    #trainSet = dataset.build_full_trainset()
    contentKNN.fit(trainSet)            
    
    testSet = BuildAntiTestSetForUser(testSubject, trainSet)
    
    predictions = contentKNN.test(testSet)
                
    recommendations = []
    
    print ("\nWe recommend:")
    for userID, movieID, actualRating, estimatedRating, _ in predictions:
        recommendations.append((int(movieID), estimatedRating))
    
    recommendations.sort(key=lambda x: x[1], reverse=True)
    return recommendations[:10]
    
