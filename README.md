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


