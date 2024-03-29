from config import app
from controller_functions import *

# Main Index page
app.add_url_rule('/', view_func=index)
# Render sign-up form
app.add_url_rule('/signup', view_func=signup_form)
# Submit and Validate sign-up form information
app.add_url_rule('/submit/signup', view_func=user_signup, methods=['POST'])
# Render login form
app.add_url_rule('/login', view_func=login_form)
# Submit and Validate login form information
app.add_url_rule('/user/validate/login', view_func=validate_login, methods=['POST'])
# Render Contact page
app.add_url_rule('/contactus', view_func=contactus_page)
# Render Calendar page
app.add_url_rule('/calendar', view_func=calendar_page)
# Render 'Thank You' page
app.add_url_rule('/thanks', view_func=thanks_page)
# Log current user out
app.add_url_rule('/logout', view_func=logout)

##################################################################
##						   AJAX ROUTES 							##
##################################################################
# Validate each input field as it is being typed
app.add_url_rule('/ajax/validate/user_first_name', view_func=ajax_validate_user_first_name, methods=['POST'])
app.add_url_rule('/ajax/validate/user_last_name', view_func=ajax_validate_user_last_name, methods=['POST'])
app.add_url_rule('/ajax/validate/user_name', view_func=ajax_validate_user_name, methods=['POST'])
app.add_url_rule('/ajax/validate/user_email', view_func=ajax_validate_user_email, methods=['POST'])
app.add_url_rule('/ajax/validate/user_password', view_func=ajax_validate_user_password, methods=['POST'])
app.add_url_rule('/ajax/validate/user_password_sameness', view_func=ajax_validate_user_password_sameness, methods=['POST'])

##################################################################
##						ADMIN ACCESS ONLY						##
##################################################################
# Render Admin page with forms
app.add_url_rule('/admin', view_func=admin_page)
# Load admin view of food items with AJAX
app.add_url_rule('/admin/food', view_func=load_food_menu)
# Load admin view of beer items with AJAX
app.add_url_rule('/admin/beer', view_func=load_beer_menu)
# Load admin view of liquor items with AJAX
app.add_url_rule('/admin/liquor', view_func=load_liquor_menu)
# Submit new user as admin
app.add_url_rule('/admin/add/user', view_func=admin_add_user, methods=['POST'])
# Remove user as admin
app.add_url_rule('/admin/remove/user', view_func=admin_remove_user, methods=['POST'])
# Submit and Validate food menu update
app.add_url_rule('/update/food', view_func=update_food_menu, methods=['POST'])
# Submit and Validate beer menu update
app.add_url_rule('/update/beer', view_func=update_beer_menu, methods=['POST'])
# Submit and Validate liquor menu update
app.add_url_rule('/update/liquor', view_func=update_liquor_menu, methods=['POST'])