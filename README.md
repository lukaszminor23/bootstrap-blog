# Flask and Bootstrap Blog
This is a blog application that I wrote on the course of "100 Days of Code: The Complete Python Pro Bootcamp".
It uses Bootstrap for the frontend, Flask for the backend and SQLite3 for database handling using SQLAlchemy as an ORM
(Object-Relational Mapper).The app allows users to register accounts and, while logged in, to perform certain actions like adding
new posts, as well as comment on them.
## Installation
1. Clone the repository:

        git clone https://github.com/lukaszminor23/bootstrap-blog.git
2. Install dependencies:
    
        pip install -r requirements.txt
3. Run the app

        python main.py
4. Visit the blog
        
        http://localhost:5000
    type this url inside your browser to see the blog.
## Setup
1. If you want the contact page to work, you need to update "modules/utils.py" file.
Update your_email and your_password variables with your email and your emails app password.
(Contact page only works for gmail accounts)
      
   ```python
        def send_email(name, email, phone, message):
            your_email = "Your email"
            your_password = "Your password"
   ```

2. Running the app for the first time will create a new empty database.
   While visiting the blog for the first time feel free to register the first account.
   First user account created will be an Admin account (user with id 1). Admin account have special
   privileges.
## User accounts
1. Unregistered users can only view the site contents and use the contact page to write messages to blog owner/admin.
2. Registered users can view the site contents, comment on posts and use the contact page.
3. Admin, in addition to the standard actions, can edit and create new posts, as well as delete posts and comments
   using the ✘ marks that are only visible to him.
## Acknowledgements
Special thanks to Angela Yu for teaching me how to use Flask, SQLAlchemy and Python in general.

Link to the course:
https://www.udemy.com/course/100-days-of-code
   