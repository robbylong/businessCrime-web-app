# businessCrime-web-app
## Introduction

London Crime is a flask, web-based application created to display recent crime statistics in London, aiming to help 
police officers conduct analysis and help citizens protect themselves. To provide a straightforward visual display of crime data, 
the web app showcases total crime cases in London from 2020 to 2021 in a dashboard sorted by crime types and borough levels. 
The data is provided by Metropolitan Police Service.

Users can access the crime dashboard by registering an account on the web app (with an email address),
they can create or modify their user profile (i.e. profile photo, region, personal description)

## instruction to run the web app
Firstly, install all packages required in the file 'requirements.txt'. It can be done by typing the command below in the terminal
```python
pip install -r requirements.txt
```
Secondly, double-click the app.py file in business crime app folder and go to the bottom
```python
if __name__ == '__main__':
    app.run(debug=True)
```
run it and click the 'http://127.0.0.1:5000/'.
![img.png](img.png)
## Instructions to use the web app

### Sign up and login (to access business crime dashboard)
- User can sign up an account with an email, and log in to view the crime dashboard
  <img alt="img_8.png" src="images for README/img_8.png"/><img alt="img_9.png" src="images for README/img_9.png"/><img alt="img_10.png" src="images for README/img_10.png"/>

Then click the 'Dashboard' in the navigation bar:
<img alt="img_11.png" src="images for README/img_11.png"/>
Click the 'go back' button to go back to home page.

### User profile (can be created or updated)
After you have logged in:
<img alt="img_12.png" src="images for README/img_12.png"/><img alt="img_13.png" src="images for README/img_13.png"/>

To search a user profile:
<img alt="img_14.png" src="images for README/img_14.png"/><img alt="img_15.png" src="images for README/img_15.png"/>
