import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import praw



reddit = praw.Reddit(client_id= 'YrcURd1GF1nwXw',
                     client_secret= 'cp3lw_xE9S6j0shBMAEJqTN4wY8',
                     user_agent= 'ejescobedo')

nltk.download('vader_lexicon')
sid = SentimentIntensityAnalyzer()

list_positive = []
list_negative = []
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


def check_comment(comment):
    negative = get_text_negative_proba(comment)
    neutral = get_text_neutral_proba(comment)
    positive = get_text_positive_probra(comment)
    if negative > neutral and negative > positive:
        list_negative.append(comment)
    if positive > neutral and positive > negative:
        list_positive.append(comment)
    if neutral > positive and neutral > negative:
        list_neutral.append(comment)

def the_world(reddit):
    for i in range(len(reddit)):
        check_comment(reddit[i].body)
        the_world(reddit[i].replies)


#comments.comments_sort = 'old'

def main():
    comments = get_submission_comments('https://www.reddit.com/r/learnprogramming/comments/5w50g5/eli5_what_is_recursion/')
    comments.comments_sort = 'old'

    the_world(comments)
    print("These are the positive comments: ")
    for i in range(len(list_positive)):
        print(list_positive[i])
        print("")

    print("These are the negative comments: ")
    for i in range(len(list_negative)):
        print(list_negative[i])
        print("")

    print("These are the neutral comments: ")
    #for i in range(len(list_neutral)):
        #print(list_neutral[i])
        #print("")


main()
