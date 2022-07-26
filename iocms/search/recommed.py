from math import sqrt
import pandas as pd
import numpy as np

from classroom.models import Classroom, Rating


class ComputeRecommendation:
    def generateRecommendation(request):
        classroom=Classroom.objects.values_list('id', 'class_name', 'class_description')
        rating=Rating.objects.values_list('classroom', 'rated_by', 'rating')
        # x=[] 
        # y=[]
        # A=[]
        # B=[]
        C=[]
        D=[]

        # for item in classroom:
        #     x=[item.id,item.title,item.movieduration,item.image.url,item.genres] 
        #     y+=[x]
        # movies_df = pd.DataFrame(y,columns=['movieId','title','movieduration','image','genres'])
        classroom_df = pd.DataFrame(classroom, columns=['classroom_id','classroom_name','classroom_description'])

        # for item in rating:
        #     A=[item.user.id,item.movie,item.rating]
        #     B+=[A]
        # rating_df=pd.DataFrame(B,columns=['userId','movieId','rating'])
        rating_df=pd.DataFrame(rating, columns=['classroom_id','rated_by', 'rating'])
        rating_df['classroom_id']=rating_df['classroom_id'].astype(str).astype(np.int64)
        rating_df['rated_by']=rating_df['rated_by'].astype(str).astype(np.int64)
        rating_df['rating']=rating_df['rating'].astype(str).astype(np.float)

        if request.user.is_authenticated:
            userid=request.user.id
            #select related is join statement in django.It looks for foreign key and join the table
            #inner join of rating with classsroom on classroom
            #then filter the table such that it has ratings given by the logged in user
            userInput=Rating.objects.select_related('classroom').filter(rated_by=userid)
            if userInput.count()== 0:
                recommenderQuery=None
                userInput=None
            else:
                for item in userInput:
                    C=[item.classroom.class_name,item.rating]
                    D+=[C]
                input_classes=pd.DataFrame(D,columns=['classroom_name','rating'])
                # input_classes -> df of all the ratings given by him/her
                input_classes['rating']=input_classes['rating'].astype(str).astype(np.float)
                # print(input_classes.dtypes)

                #Filtering out the classrooms by classname
                input_id = classroom_df[
                    classroom_df['classroom_name'].isin(input_classes['classroom_name'].tolist())
                ]
                #Then merging it so we can get the class_id. It's implicitly merging it by title.
                input_classes = pd.merge(input_id, input_classes)
                # #Dropping information we won't use from the input dataframe
                # inputMovies = inputMovies.drop('year', 1)
                #Final input dataframe
                #If a movie you added in above isn't here, then it might not be in the original 
                #dataframe or it might spelled differently, please check capitalisation.
                # print(input_classes)

                #Filtering out users that have watched movies that the input has watched and storing it
                user_subset = rating_df[rating_df['classroom_id'].isin(input_classes['classroom_id'].tolist())]
                print(user_subset.head())

                #Groupby creates several sub dataframes where they all have the same value in the column specified as the parameter
                userSubsetGroup = user_subset.groupby(['rated_by'])
                
                #print(userSubsetGroup.get_group(7))

                #Sorting it so users with movie most in common with the input will have priority
                userSubsetGroup = sorted(userSubsetGroup,  key=lambda x: len(x[1]), reverse=True)

                # print(userSubsetGroup[0:])

                userSubsetGroup = userSubsetGroup[0:]

                #Store the Pearson Correlation in a dictionary, where the key is the user Id and the value is the coefficient
                pearsonCorrelationDict = {}

            #For every user group in our subset
                for name, group in userSubsetGroup:
                #Let's start by sorting the input and current user group so the values aren't mixed up later on
                    group = group.sort_values(by='classroom_id')
                    input_classes = input_classes.sort_values(by='classroom_id')
                    #Get the N for the formula
                    nRatings = len(group)
                    #Get the review scores for the movies that they both have in common
                    temp_df = input_classes[input_classes['classroom_id'].isin(group['classroom_id'].tolist())]
                    #And then store them in a temporary buffer variable in a list format to facilitate future calculations
                    tempRatingList = temp_df['rating'].tolist()
                    #Let's also put the current user group reviews in a list format
                    tempGroupList = group['rating'].tolist()
                    #Now let's calculate the pearson correlation between two users, so called, x and y
                    Sxx = sum([i**2 for i in tempRatingList]) - pow(sum(tempRatingList),2)/float(nRatings)
                    Syy = sum([i**2 for i in tempGroupList]) - pow(sum(tempGroupList),2)/float(nRatings)
                    Sxy = sum( i*j for i, j in zip(tempRatingList, tempGroupList)) - sum(tempRatingList)*sum(tempGroupList)/float(nRatings)
                    
                    #If the denominator is different than zero, then divide, else, 0 correlation.
                    if Sxx != 0 and Syy != 0:
                        pearsonCorrelationDict[name] = Sxy/sqrt(Sxx*Syy)
                    else:
                        pearsonCorrelationDict[name] = 0

                # print(pearsonCorrelationDict.items())

                pearsonDF = pd.DataFrame.from_dict(pearsonCorrelationDict, orient='index')
                pearsonDF.columns = ['similarityIndex']
                pearsonDF['user_id'] = pearsonDF.index
                pearsonDF.index = range(len(pearsonDF))
                # print(pearsonDF.head())

                topUsers=pearsonDF.sort_values(by='similarityIndex', ascending=False)[0:]
                # print(topUsers.head())

                topUsersRating=topUsers.merge(rating_df, left_on='user_id', right_on='rated_by', how='inner')
                topUsersRating.head()

                    #Multiplies the similarity by the user's ratings
                topUsersRating['weightedRating'] = topUsersRating['similarityIndex']*topUsersRating['rating']
                topUsersRating.head()


                #Applies a sum to the topUsers after grouping it up by userId
                tempTopUsersRating = topUsersRating.groupby('classroom_id').sum()[['similarityIndex','weightedRating']]
                tempTopUsersRating.columns = ['sum_similarityIndex','sum_weightedRating']
                tempTopUsersRating.head()

                #Creates an empty dataframe
                recommendation_df = pd.DataFrame()
                #Now we take the weighted average
                recommendation_df['weighted average recommendation score'] = tempTopUsersRating['sum_weightedRating']/tempTopUsersRating['sum_similarityIndex']
                recommendation_df['classroom_id'] = tempTopUsersRating.index
                recommendation_df.head()

                recommendation_df = recommendation_df.sort_values(by='weighted average recommendation score', ascending=False)
                recommender=classroom_df.loc[classroom_df['classroom_id'].isin(recommendation_df.head(5)['classroom_id'].tolist())]
                # print("_________________________________________________________________")
                # print(recommender)
                # print("_________________________________________________________________")
                return recommender.to_dict('records')
