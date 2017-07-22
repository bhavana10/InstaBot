import requests,urllib
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

'''
GLOBAL VARIABLE TO STORE BASE URL AND ACCESS TOKEN OF THE USER.
'''

APP_ACCESS_TOKEN = '1718452521.5a7caf4.ff77bf36d87b4737911ee28c72a5c190'
BASE_URL = 'https://api.instagram.com/v1/'


'''
FUNCTION DECLARATION TO FETCH OWN DETAILS. IT DO NOT ACCEPT ANY INPUT PARAMETER.
'''
def self_info():
    request_url = (BASE_URL + 'users/self/?access_token=%s') % (APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    # get call to fetch user details
    user_info = requests.get(request_url).json()
    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print 'User does not exist!'
    else:
        print 'Status code other than 200 received!'


'''
FUNCTION TO GET THE USER ID FROM THE GIVEN USERNAME.
'''
def get_user_id( insta_username ) :
    request_url = (BASE_URL + 'users/search?q=%s&access_token=%s') % ( insta_username, APP_ACCESS_TOKEN)
    user_info = requests.get(request_url).json()
    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            return user_info['data'][0]['id']
        else:
            return None
    else:
        print 'Status code other than 200 received!'
        exit()


'''
FUNCTION DECLARATION TO FETCH DETAILS OF THE GIVEN USERNAME. IT ACCEPT USERNAME AS INPUT PARAMETER.
'''
def get_user_info(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print 'There is no data for this user!'
    else:
        print 'Status code other than 200 received!'


'''
FUNCTION DECLARATION TO GET THE ID OF THE RECENT POST OF A USER BY USERNAME
'''
def get_post_id(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    #print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            return user_media['data'][0]['id']
        else:
            print 'There is no recent post of the user!'
            exit()
    else:
        print 'Status code other than 200 received!'
        exit()


'''
FUNCTION DECLARATION TO GET YOUR RECENT POST
'''
def get_own_post():
    request_url = (BASE_URL + 'users/self/media/recent/?access_token=%s') % (APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    own_media = requests.get(request_url).json()

    if own_media['meta']['code'] == 200:
        if len(own_media['data']):
            image_name = own_media['data'][0]['id'] + '.jpeg'
            image_url = own_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded!'
            print "Recent post id: " + own_media['data'][0]['id']
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'


'''
FUNCTION DECLARATION TO GET THE RECENT POST OF A USER BY USERNAME
'''
def get_user_post(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            media_id = get_post_id(insta_username)
            image_name = user_media['data'][0]['id'] + '.jpeg'
            image_url = user_media['data'][0]['images']['standard_resolution']['url']
            #download the recent post
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded!'
            print 'Recent Post ID: ' + media_id
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'


'''
FUNCTION SEARCH A POST HAVING MINIMUM LIKE OF A USER
'''
def post_with_min_like(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()
    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            min = user_media['data'][0]['likes']['count']
            for i in range(len(user_media['data'])):
                if min > user_media['data'][i]['likes']['count']:
                    min = user_media['data'][i]['likes']['count']
                    pos= i
            print "Likes on post : %d"  %user_media['data'][pos]['likes']['count']
            print "Image URL :" + user_media['data'][pos]['images']['standard_resolution']['url']
            print "Post ID : " + user_media['data'][pos]['id'] + "\n"
        else:
            print 'There is no post of the user!'
            exit()
    else:
        print 'Status code other than 200 received!'
        exit()


'''
FUNCTION TO SEARCH A POST BY INPUTING CAPTION
'''
def get_post_by_caption(word,insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()
    flag = False
    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            for i in range(len(user_media['data'])):
                caption_text = user_media['data'][i]['caption']['text']
                if word in caption_text:
                    print "Caption on the post : " + user_media['data'][i]['caption']['text']
                    print "Image URL :" + user_media['data'][i]['images']['standard_resolution']['url']
                    print "Post ID : " + user_media['data'][i]['id'] +"\n"
                    flag = True
            if(flag == False):
                print "No caption related post found"
        else:
            print 'There is no required post of the user!'
            exit()
    else:
        print 'Status code other than 200 received!'
        exit()


'''
FUNCTION TO TRY AND CHOOSE THE POST IN A CREATIVE WAY,
1- WITH MINIMUM NUMBER LIKES
2-WHOSE CAPTION HAS A PARTICULAR TEXT
'''
def try_creative_ways(insta_username):
    print "Choose a way for getting a post of a user:"
    print "1- with minimum number likes"
    print "2-whose caption has a particular text"
    print "3- exit"
    while True:
        choice= raw_input("Enter your choice:")
        choice=int(choice)
        if choice==1:
            post_with_min_like(insta_username)
        elif choice == 2:
            word = raw_input("Enter a particular text to be searched in caption")
            get_post_by_caption(word,insta_username)
        elif choice == 3:
            break
        else:
            print "Invalid Choice"


'''
FUNCTION TO GET THE LIST OF USERS LIKED THE RECENT POST OF THE USER
'''
def get_like_list(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/likes?access_token=%s') % (media_id,APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    like_list = requests.get(request_url).json()
    if like_list['meta']['code']==200:
        if len(like_list['data']):
            print "Post liked by :"
            for i in range(len(like_list['data'])):
                print "%d)" %(i+1)+ like_list['data'][i]['username']
        else:
            print "No one liked the recent post of user"
    else:
        print 'Status code other than 200 received!'


'''
FUNCTION DECLARATION TO LIKE THE RECENT POST OF A USER
'''
def like_a_post(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/likes') % (media_id)
    payload = {"access_token": APP_ACCESS_TOKEN}
    print 'POST request url : %s' % (request_url)
    post_a_like = requests.post(request_url, payload).json()
    if post_a_like['meta']['code'] == 200:
        print 'You successfully liked the post!'
    else:
        print 'Failed to like the post. Try again!'


'''
FUNCTION TO FETCH THE COMMENTS ON A POST OF GIVEN USERNAME.
'''
def get_comment_list(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/comments?access_token=%s') % (media_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    comment_list = requests.get(request_url).json()
    if comment_list['meta']['code'] == 200:
        if len(comment_list['data']):
            print "Post liked by :"
            for i in range(len(comment_list['data'])):
                print "%d)" % (i + 1) + comment_list['data'][i]['text']
        else:
            print "No one commented the recent post of user"
    else:
        print 'Status code other than 200 received!'


'''
FUNCTION DECLARATION TO MAKE A COMMENT ON THE RECENT POST OF THE USER
'''
def post_a_comment(insta_username):
    media_id = get_post_id(insta_username)
    comment_text = raw_input("Your comment: ")
    payload = {"access_token": APP_ACCESS_TOKEN, "text" : comment_text}
    request_url = (BASE_URL + 'media/%s/comments') % (media_id)
    print 'POST request url : %s' % (request_url)
    make_comment = requests.post(request_url, payload).json()
    if make_comment['meta']['code'] == 200:
        print "Successfully added a new comment!"
    else:
        print "Unable to add comment. Try again!"


'''
FUNCTION DECLARATION TO MAKE DELETE NEGATIVE COMMENTS FROM THE RECENT POST
'''
def delete_negative_comment(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    comment_info = requests.get(request_url).json()
    if comment_info['meta']['code'] == 200:
        if len(comment_info['data']):
            #Here's a naive implementation of how to delete the negative comments :)
            for i in range(len(comment_info['data'])):
                comment_id = comment_info['data'][i]['id']
                comment_text = comment_info['data'][i]['text']
                blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())
                if (blob.sentiment.p_neg > blob.sentiment.p_pos):
                    print 'Negative comment : %s' % (comment_text)
                    delete_url = (BASE_URL + 'media/%s/comments/%s/?access_token=%s') % (media_id, comment_id, APP_ACCESS_TOKEN)
                    print 'DELETE request url : %s' % (delete_url)
                    delete_info = requests.delete(delete_url).json()
                    if delete_info['meta']['code'] == 200:
                        print 'Comment successfully deleted!\n'
                    else:
                        print 'Unable to delete comment!'
                else:
                    print 'Positive comment : %s\n' % (comment_text)
        else:
            print 'There are no existing comments on the post!'
    else:
        print 'Status code other than 200 received!'


'''
FUCTION TO SEARCH A WORD IN COMMENT AND DELETE THE PERTICULAR COMMENT OF A USER
'''
def search_delete_comment(word,insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    comment_info = requests.get(request_url).json()

    if comment_info['meta']['code'] == 200:
        if len(comment_info['data']):
            #Here's a naive implementation of how to delete the negative comments :)
            for i in range(len(comment_info['data'])):
                comment_id = comment_info['data'][i]['id']
                comment_text = comment_info['data'][i]['text']
                if(word in comment_text):
                    print "Comment found:" + comment_text
                    delete_url = (BASE_URL + 'media/%s/comments/%s/?access_token=%s') % (media_id, comment_id, APP_ACCESS_TOKEN)
                    print 'DELETE request url : %s' % (delete_url)
                    delete_info = requests.delete(delete_url).json()
                    if delete_info['meta']['code'] == 200:
                        print 'Comment successfully deleted!\n'
                    else:
                        print 'Unable to delete comment!'
                else:
                    print '%s not found in the comment : ' %(word) +comment_text
        else:
            print 'There are no existing comments on the post!'
    else:
        print 'Status code other than 200 received!'


'''
FUNCTION TO RETURN A POST ID OF A PERTICULAR POST OF A USER
'''
def get_total_post(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print '%s has %s total no. of posts.' % (user_info['data']['username'],user_info['data']['counts']['media'])
        else:
            print 'There is no data for this user!'
    else:
        print 'Status code other than 200 received!'

    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    # print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()
    user_info = requests.get(request_url).json()
    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            post_number=raw_input("Choose a post's number:")
            post_number=int(post_number)
            return user_media['data'][post_number-1]['id']
        else:
            print 'There is no post of the user!'
            exit()
    else:
        print 'Status code other than 200 received!'
        exit()


'''
FUNCTION TO GET A USER'S POST ID, AND ITERATE THROUGH THE COMMENTS
'''
def get_post_comments(post_id):
    request_url = (BASE_URL + 'media/%s/comments?access_token=%s') % (post_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    comment_list = requests.get(request_url).json()
    if comment_list['meta']['code'] == 200:
        if len(comment_list['data']):
            print "Post liked by :"
            for i in range(len(comment_list['data'])):
                print "%d)" % (i + 1) + comment_list['data'][i]['text']
        else:
            print "No one commented the recent post of user"
    else:
        print 'Status code other than 200 received!'


'''
************************************************ M E N U **********************************************
'''
def start_bot():
    while True:
        print '\n'
        print 'Hey! Welcome to instaBot!'
        print 'Here are your menu options:'
        print "a.Get your own details"
        print "b.Get details of a user by username"
        print "c.Get your own recent post"
        print "d.Get the recent post of a user by username"
        print "e. Get the post in a creative way"
        print "f.Get a list of people who have liked the recent post of a user"
        print "g.Like the recent post of a user"
        print "h.Get a list of comments on the recent post of a user"
        print "i.Make a comment on the recent post of a user"
        print "j.Delete negative comments from the recent post of a user"
        print "k.Search a word and delete the comment from the recent post of a user"
        print "l.Get a user's posts, and iterate through the comments"
        print "m.Exit"

        choice=raw_input("Enter you choice: ")
        if choice=="a":
            self_info()
        elif choice=="b":
            insta_username = raw_input("Enter the username of the user: ")
            get_user_info(insta_username)
        elif choice=="c":
            get_own_post()
        elif choice=="d":
            insta_username = raw_input("Enter the username of the user: ")
            get_user_post(insta_username)
        elif choice == "e":
            insta_username = raw_input("Enter the username of the user: ")
            try_creative_ways(insta_username)
        elif choice=="f":
            insta_username = raw_input("Enter the username of the user: ")
            get_like_list(insta_username)
        elif choice=="g":
            insta_username = raw_input("Enter the username of the user: ")
            like_a_post(insta_username)
        elif choice=="h":
            insta_username = raw_input("Enter the username of the user: ")
            get_comment_list(insta_username)
        elif choice=="i":
            insta_username = raw_input("Enter the username of the user: ")
            post_a_comment(insta_username)
        elif choice=="j":
            insta_username = raw_input("Enter the username of the user: ")
            delete_negative_comment(insta_username)
        elif choice=='k':
            insta_username = raw_input("Enter the username of the user: ")
            word= raw_input("Enter the word to be searched in the comments:")
            search_delete_comment(word,insta_username)
        elif choice=='l':
            insta_username = raw_input("Enter the username of the user: ")
            post_id = get_total_post(insta_username)
            get_post_comments(post_id)
        elif choice=="m":
            exit()
        else:
            print "wrong choice"


'''
CALLING THE START_BOT() TO GET THE MENU AND PERFORM VARIOUS OPERATIONS
'''
start_bot()