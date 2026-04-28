# HIC Final Project - Cat Cafe Website

## Table of Contents

- [File Structure](#file-structure)
- [Setup Instructions](#setup-instructions)
- [Usage Instructions](#usage-instructions)

## File Structure

- `app.py` - Main Flask application file
- `templates/` - HTML templates for the website
- `static/` - Static files (CSS, images, etc.)
- `cat_cafe.sql` - SQL file to set up the MySQL database

## Setup Instructions

1.  Clone the repository

        git clone https://github.com/yourusername/cat-cafe.git
        cd cat-cafe

2.  Create a virtual environment (recommended)

        python -m venv venv

    Activate it:

        Windows:
            venv\Scripts\activate

        Mac/Linux:
            source venv/bin/activate

3.  Install dependencies

        pip install flask flask-mysqldb flask-bcrypt

4.  Set up the database

    Open XAMPP Control Panel
    Start MySQL
    Import the database
    Open phpMyAdmin (http://localhost/phpmyadmin)
    Create a database named:

        cats

    Import the SQL file:

        cats.sql

5.  Configure your database connection

    In app.py:

        app.config['MYSQL_HOST'] = '127.0.0.1'
        app.config['MYSQL_USER'] = 'root'
        app.config['MYSQL_PASSWORD'] = ''
        app.config['MYSQL_DB'] = 'cats'
        app.config['MYSQL_PORT'] = 3306

## Usage Instructions

1. Run the Flask application

   python app.py

   Then open:

   http://127.0.0.1:5050
