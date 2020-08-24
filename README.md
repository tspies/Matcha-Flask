# READ ME

## Matcha---Flask
A dating website that allows users to connect with others based on romantic preferences/interests.<br>
Built using Python and the light-weight Flask Micro Framwork.<br>
Install requirments before proceeding to Intallation Steps.

### Requirments :
- Python https://www.python.org/downloads/<br>
<br>

## Installation Steps:

### 1. Setting Up Source Code
  - Navigate to https://github.com/tspies/Matcha-Flask and click the clone or download button
  - Once the project is cloned, navigate to the inner Matcha folder.
  - Install virtualenv using the following command in your terminal:
  ```bash
    pip install virtualenv
  ```
  - Activate your Python Venv using this command in your terminal:
    - Mac OS
    ```bash
      source venv/Scripts/activate
    ```
    - Windows
    ```bash
      venv\Scripts\activate
    ```
  - Next install all dependancies using the following command in your terminal:
    ```bash
      pip install -r requirements.txt
    ```
### 2. Setting Up Database
  - No downloads for the Database are needed as Matcha uses the built in sqlite3 that comes with Flask<br>
  - With your venv still running, run the following command:
    ```bash
      python database.py
    ```
    - This will create the database structure using schema.sql.
    - It will then populate the database using populate_db.sql.
    
### 3. Run Matcha-Flask Server
  - Run the following command:
    ```bash
      python run.py
    ```
  - Navigate to http://127.0.0.1:5000/ to start using Matcha
  
## Code Breakdown
  - Back-end Technologies
    - Flask
  - Front-end Techanologies
    - HTML
    - CSS
    - Javascript
    - Boostrap
  - Database Management Systems
    - mysql
    - sqlite3
  - Folder Structure Breakdown
    - matcha
      - admin_lib
        - Folder containing logic used on the admin site of Matcha.
      - browsing_lib
        - Folder containing logic with regard to the user movement through the website i.e: searching, user suggestions.
      - common_lib
        - Folder containing logic that is accessed from multiple other aprts of Matcha and its modules.
      - notification_lib
        - Folder containing logic that handles notifications and messages between users.
      - static
        - image
          - Folder containing all images used for the website
        - main.css
          - Main source of CSS Styling
        - socket.js
          - Javascript used to handle the Socket Programming for Notifications and Messages
      - templates
        - Folder containing all .html files that Flask will serve as templates to the user.
      - user_lib
        - Folder containing logic for user logging in and signing up.
      - validation_lib
        - Folder conatining logic for all validation needed for Matcha, i.e: user validation, form validation etc.
    - venv
      - Folder with all dependencies and sources for Python Venv to run.

