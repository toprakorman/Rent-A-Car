# Rent-A-Car

This is my SE 3355 final project called "Rent-A-Car", that is done in Flask. The "Final Requirements" file said that Flask is not accepted at first, but we've been told that our lecturer allowed Flask later, but they will be graded out of 80 instead of 100, which is fine.

Explanation of the project:
- The base has a header that has the hidden home page button, login, register, and logout button implemented.
- The main page has the search for office option, the map that shows the all the available offices, and the language switch option at the bottom. It will ask for your loccation if you're not logged in to find and pinpoint your location on the map.
- Login page is simple. You just log in. We've been requested in our "Final Requirements" file to do either a manual login or a "Sign in with Google" type of login, which I ended up doing the former.
- Register page has the optional file upload button, which does nothing as it is said in our "Final Requirements" file.
- The office and car pages are simple and more or less have the same design.
- The search results can be sorted. In in our "Final Requirements" file we've been requested to make a header for this sorting process, but I ended up doing a sidebar as I liked how it looked a lot better.

Explanation of code:
- app.py class is the basic Flask class. It has all the needed methods for this entire project.
- languages.py is my dictionary class. It's for translation English to Turkish, and vice versa.
- models.py has my SQL models. Pretty simple.
- auth_handler is for authenticating and protecting passwords.
- Google Maps is to locate my offices, which could have been implemented better. It's not working with the office dabatase much. My end is at fault on that.
- validators.py is for validating email and passwords while registering.
- syles.css has the styles as the name implies
