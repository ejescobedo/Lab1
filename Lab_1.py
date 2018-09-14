import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import praw



reddit = praw.Reddit(client_id= 'YrcURd1GF1nwXw',
                     client_secret= 'cp3lw_xE9S6j0shBMAEJqTN4wY8',
                     user_agent= 'ejescobedo')

nltk.download('vader_lexicon')
sid = SentimentIntensityAnalyzer()

list_positive = []                  #Creation of 3 global lists in which the positive, negative and neutral comments will be stored
list_negative = []                  #I decided to do it this way, because I believe is a more efficient way of doing for this case
list_neutral = []

def get_text_negative_proba(text):
    return sid.polarity_scores(text)['neg']


def get_text_neutral_proba(text):
    return sid.polarity_scores(text)['neu']


def get_text_positive_probra(text):
    return sid.polarity_scores(text)['pos']


def get_submission_comments(url):
    submission = reddit.submission(url=url)
    submission.comments.replace_more()

    return submission.comments


def check_comment(comment):                         #In this method we will take as parameter the current comment we are working on
    negative = get_text_negative_proba(comment)     #From there we will use 3 methods to determine the neutral, negative and
    neutral = get_text_neutral_proba(comment)       # positive percentage of the current comment. Next we will compare these
    positive = get_text_positive_probra(comment)    #percentages against each other to see which is the biggest percentage
    if negative > neutral and negative > positive:  # Depending of which percentage wins, that comment will go to the corresponding list
        list_negative.append(comment)
    if positive > neutral and positive > negative:
        list_positive.append(comment)
    if neutral > positive and neutral > negative:
        list_neutral.append(comment)

def the_thread(reddit):                             #This method recursively analizes the reddit posts, it moves by means of "replies" to go
    for i in range(len(reddit)):                    #through the post in a accordingly manner. If the current comment has no more replies , the for
        check_comment(reddit[i].body)               #loop will enable us to read comments below the current comment(if any exists) and increasing the value of i,
        the_thread(reddit[i].replies)               #once it agains reaches a comment with replies, the "replies" method will be recursively used



#This print method will simply get the lists as parameters and print the elements inside each of the lists
def show(list_positive, list_negative, list_neutral):
    print("*******************************************************************")
    print("These are the positive comments: ")
    for i in range(len(list_positive)):
        print(list_positive[i])
        print("")
    print("*******************************************************************")
    print("These are the negative comments: ")
    for i in range(len(list_negative)):
        print(list_negative[i])
        print("")
    print("********************************************************************")
    print("These are the neutral comments: ")
    for i in range(len(list_neutral)):
        print(list_neutral[i])
        print("")

#Since we have multiple posts being analyzed, the same 3 lists will be used to save the positive, negative and neutral comments, in order
#to do this, the list will be emptied once its function complete, in order to save new elemets in these lists
def empty_lists():
    del list_positive[:]
    del list_negative[:]
    del list_neutral[:]


#The following posts were chosen because it had a good amount of positive, negative and neutral comments, so it would be more appreciated
#how they are tested and put into the correct spot
def main():
    comments = get_submission_comments('https://www.reddit.com/r/learnprogramming/comments/5w50g5/eli5_what_is_recursion/')
    comments_2 = get_submission_comments('https://www.reddit.com/r/politics/comments/9fl1as/us_government_posts_214_billion_deficit_in_august/')
    comments_3 = get_submission_comments('https://www.reddit.com/r/politics/comments/9fkb18/brett_kavanaugh_has_a_mysterious_metoo_problem/')


    the_thread(comments)                                #setting the posts and using the previously mentioned methods to perform the task required

    print("These are the comments for the first post")
    print("")
    show(list_positive, list_negative, list_neutral)
    empty_lists()
    the_thread(comments_2)
    print("These are the comments for the second post")
    print("")
    show(list_positive, list_negative, list_neutral)
    empty_lists()
    print("")
    print("These are the comments for the third post")
    print("")
    the_thread(comments_3)
    show(list_positive, list_negative, list_neutral)


main()
