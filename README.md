# Rent-A-Car

This is my SE 3355 final project called "Rent-A-Car", which is done in Flask. The "Final Requirements" file said that Flask is not accepted at first, but we've been told that our lecturer allowed Flask later, but they will be graded out of 80 instead of 100, which is fine. The website is also hosted on pythonanywhere, which because it is also not specified and left us to choose our hosting website in the file.

Explanation of the project:
- The base has a header that implements the hidden home page button, login, register, and logout buttons.
- The main page has a search for office option, a map showing all the available offices, and a language switch option at the bottom. If you're not logged in, it will ask for your location to pinpoint your location on the map.
- The login page is simple. You just log in. We've been requested in our "Final Requirements" file to do either a manual login or a "Sign in with Google" type of login, which I ended up doing the former.
- The register page has the optional file upload button, which does nothing as it is said in our "Final Requirements" file.
- The office and car pages are simple and have more or less the same design.
- The search results can be sorted. In our "Final Requirements" file, we were requested to create a header for this sorting process, but I ended up creating a sidebar because I liked how it looked.

Explanation of code:
- app.py class is the basic Flask class. It has all the needed methods for this entire project.
- languages.py is my dictionary class. It's for translation from English to Turkish, and vice versa.
- models.py has my SQL models. Pretty simple.
- auth_handler is for authenticating and protecting passwords.
- Google Maps is to locate my offices, which could have been implemented better. It's not working with the office database much. My end is at fault for that.
- validators.py is for validating email and passwords while registering.
- syles.css has the styles as the name implies


[Click here to watch the presentation](https://drive.google.com/file/d/1f6aS1tSrqPvtj9JpfprxS4p4IhiY87jC/view?usp=drive_link)

ASSUMPTIONS
- It says "Login with email/password or Google will be supported" in the file, so I assumed it was either one of them
- It says "Photo upload needs to be supported but is optional for registration" in the file, so I implemented the option, but it does absolutely nothing
- It says "Web application needs to be hosted on a provider like Azure Apps, Render.com." in the file, so I assumed it could be any hosting website since it says 'like'.

PROBLEMS I ENCOUNTERED
- I had problems with the password and email validation and authentication, so I got help from GitHub, YouTube, and StackOverflow, hence the leftover comments in those classes
- I had problems with pinpointing offices on the map, so I added their locations to the code manually instead of getting them from the database
- I changed some of the design choices since I liked mine better
