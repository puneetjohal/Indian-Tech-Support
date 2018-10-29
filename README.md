# Indian-Tech-Support
#### Roster: Adil Gondal, Shafali Gupta, Ahnaf Hasan, Puneet Johal

## What It Is:
We've created a web log hosting site. Users will register for the site which will allow them to create new blogs, view and edit old blogs, and look at the blogs of other users.
## What You'll Need:
* Python 3
* Virtual Environment
* Flask

### Virtual Environment
* Create your virtual environment using: ```python3 -m venv <name> ```
* Go to the directory containing your virtual environemnt and activate it using: ```source name/bin/activate``` 
### Flask
* Once your virtual environment is activated you can download flask using:
```
pip install wheel
pip install flask
```
### Running The Program
* Clone our project repo using:```git clone https://github.com/puneetjohal/Indian-Tech-Support.git```
* Go into our project repo and run it using:```python app.py```
* Open a browser and see the website at: http://127.0.0.1:5000/
* Once you're finished, disable your virtual environment using:```deactivate```

### Extra Modules and Libraries
#### Datetime
* Documentation: <https://docs.python.org/3/library/datetime.html#module-datetime>
* This module provides users with access to time related functions that can track date and time in a variety of different formats.
* We deemed it necessary in order to display the most recent date and time of post editing on blogs.
* We used the datetime module functions for keeping track of when posts were created or edited, and displayed the most recent of those dates and times along with the post content on the blogs.

#### Random
* Documentation: <https://docs.python.org/3/library/random.html>
* This module provides users with access to functions related to generating psuedo-random numbers.
* We deemed it necessary in order to display a random "post of the day" on our landing page.
* We used the random module functions for selecting a random post made by any user from our database, and then displaying its contents, author, and last edit time on the landing page.
