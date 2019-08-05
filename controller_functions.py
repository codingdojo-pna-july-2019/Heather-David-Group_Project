import re
import tweepy
from flask import render_template, redirect, request, session, url_for
from sqlalchemy import desc
from config import db, api
from models import User, Admin, Food, Beer, Liquor

################
## ROOT ROUTE ##
################
def index():
	twitter_search_q = '#FortniteWorldCup'
	cur_tweet_ids = []
	for tweet in tweepy.Cursor(api.search, q=twitter_search_q, lang='en').items(10):
		cur_tweet_ids.append(tweet.id)

	return render_template("index.html", cur_tweets=cur_tweet_ids, cur_tweet_q=twitter_search_q)


######################
## USER SIGNUP FORM ##
######################
def signup_form():
	if 'userid' in session:
		return redirect('/')

	return render_template('signup.html')


##########################################
## VALIDATE FORM DATA and REGISTER USER ##
##########################################
def user_signup():
	is_valid = User.validate_user_signup(request.form)

	# Record data and flash success
	if is_valid:
		new_user = User.add_new_user(request.form)
		session['userid'] = new_user.id
		session['name'] = request.form['uname']

		return redirect('/')

	return redirect('/signup')


#####################
## USER LOGIN FORM ##
#####################
def login_form():
	if 'userid' in session:
		return redirect('/')

	return render_template('index.html?login_form=1')


#########################
## VALIDATE USER LOGIN ##
#########################
def validate_login():
	loginUser = User.query.filter_by(email=request.form['email']).first()

	if loginUser:
		pw = bcrypt.check_password_hash(loginUser.password, request.form['password'])

		if pw:
			session['userid'] = loginUser.id
			session['name'] = loginUser.username
			return redirect('/')
		else:
			flash("Password incorrect! Please try again.", 'login_error')
	else:
		flash("Email not recognized", 'login_error')

	return redirect('/login')


#####################
## CONTACT US PAGE ##
#####################
def contactus_page():
	return render_template('contactus.html')


########################
## CALENDAR OF EVENTS ##
########################
def calendar_page():
	return render_template('calendar.html')


####################
## THANK YOU PAGE ##
####################
def thanks_page():
	return render_template('thanks.html')



############
## LOGOUT ##
############
def logout():
	session.clear()
	return redirect('/')


#########################################################################################
## 								    AJAX ROUTES									   	   ##
#########################################################################################
def ajax_validate_user_first_name():
	User.validate_user_first_name()
def ajax_validate_user_last_name():
	User.validate_user_last_name()
def ajax_validate_user_name():
	User.validate_user_name()
def ajax_validate_user_email():
	User.validate_user_email()
def ajax_validate_user_password():
	User.validate_user_password()
def ajax_validate_user_password_sameness():
	User.validate_user_password_sameness()


#########################################################################################
## 								ADMIN ONLY ACCESS 									   ##
#########################################################################################
################
## ADMIN PAGE ##
################
def admin_page():
	return render_template('admin.html')


######################
## UPDATE FOOD MENU ##
######################
def update_food_menu():
	# perform check for Admin access BEFORE updating

	# ADD
	# UPDATE
	# MAKE INACTIVE
	# DELETE
	pass


######################
## UPDATE BEER MENU ##
######################
def update_beer_menu():
	# perform check for Admin access BEFORE updating

	# ADD
	# UPDATE
	# MAKE INACTIVE
	# DELETE
	pass


########################
## UPDATE LIQUOR MENU ##
########################
def update_liquor_menu():
	# perform check for Admin access BEFORE updating

	# ADD
	# UPDATE
	# MAKE INACTIVE
	# DELETE
	pass