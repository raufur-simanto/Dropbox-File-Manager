# Dropbox File Manager

## Overview

The **Dropbox File Manager** is a web-based application implemented using REST architecture. Dropbox(`http://www.dropbox.com/`) is used as a static file host. Connecting to Dropbox using REST API allows manipulation with content via REST Clients.


## Available Apis

The application is built on top of SOAP web services that provide the following functionalities:

- `login`: Give access token for api calls.
- `get_all_files`: List all the files.
- `count`: Gives total numbers of file
- `delete`: Delete a specific file
- `search`: Search a file and gives it's information
- `download`: Download a file
- `rename`: Rename a file
- `upload`: Upload a file
- `create`: Create a folder
- `user-info`: Gives profile information

## Technologies Used

- **Backend**:
  - **Python3.10**
  - **Flask** (for handling web requests)

- **Api Testing**:
  - **Postman**
  
## Project Structure

```
dropbox File Manager
│
├── project/
│   └── __init__.py           # project initial configuration file
│   └── config.py             # project configuration file
│   └── apis/         
│       └── __init__.py       # apis configuration file
│       └── auth.py           # authentication apis
│       └── files.py          # file related apis 
│       └── profile.py        # profile apis
│       └── folder.py         # folder apis
│
├── manage.py                 # Main Flask application file
├── .flaskenv                 # flask environment file
│
├── requirements.txt          # Project dependencies
└── readme.MD                 # Project overview and details

```

## Setup Instructions

1. **Clone the repository**:

   ```bash
   git@github.com:raufur-simanto/Dropbox-File-Manager.git
   cd Dropbox-File-Manager.git
   ```

2. **Create and activate a virtual environment**:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # For Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:

   ```bash
   flask run or
   python manage.py
   ```

5. **Access the application**:

   Open your browser and navigate to `http://127.0.0.1:5000`.

