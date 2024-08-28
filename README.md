
# Car Rental System

## Overview
The Car Rental System is a Python-based application that allows users to rent cars, manage rentals, and provide car recommendations based on user preferences. The system supports different user roles, including admin and customer, each with specific privileges.

## Table of Contents
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [File Structure](#file-structure)
- [Licensing](#licensing)
- [Known Issues](#known-issues)
- [Credits](#credits)

## Installation

### Prerequisites
Before you begin, ensure you have the following installed on your machine:
- Python 3.8 or higher
- MySQL Server
- Python package manager (pip)

### Step-by-Step Installation

1. **Install Required Python Packages:**
   Run the following command in your terminal to install the necessary Python packages:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set Up MySQL Database:**
   - Open your MySQL client.
   - Create a new database:
     ```sql
     CREATE DATABASE car_rental_auckland;
     ```
   - Update the `config.ini` file in the root directory with your MySQL credentials:
     ```ini
     [mysql]
     host = localhost
     user = your_username
     password = your_password
     database = car_rental_auckland
     ```

3. **Initialize the Database:**
   Run the `main.py` file to initialize the database tables and create the default admin user:
   ```bash
   python main.py
   ```
   The system will create the necessary tables and a default admin account.

## Configuration

### Configuring the Database
The database configuration is stored in the `config.ini` file. Ensure you update the file with your MySQL credentials. Here is the structure:

```ini
[mysql]
host = localhost
user = your_username
password = your_password
database = car_rental_auckland
```

### Adding Initial Data
To add initial data like car details or user accounts, you can modify the `main.py` script or directly insert records into the database via MySQL client.

## Usage

### Running the Application
To start the Car Rental System, run the following command:

```bash
python main.py
```

### User Roles
- **Admin:** Can manage cars, approve/reject rentals, and view all users.
- **Customer:** Can browse available cars, book rentals, and get car recommendations.

### Features
- **Car Management:** Admins can add, update, or delete car records.
- **Rental Management:** Admins can approve or reject rental requests.
- **Car Recommendations:** Users can receive car recommendations based on their preferences or rental history.

## File Structure
- `main.py`: Entry point of the application. Initializes the database and starts the CLI.
- `models/`: Contains all the data models (User, Car, Rental) that represent the database tables.
- `controllers/`: Contains controllers that manage the business logic and database interactions for users, cars, and rentals.
- `views/cli.py`: Handles the command-line interface (CLI) and user interactions.
- `utils/io_utils.py`: Contains utility functions for handling input/output operations.
- `controllers/ai_recommendation.py`: Provides AI-based car recommendations.
- `config.ini`: Configuration file for the MySQL database connection.
- `requirements.txt`: Lists all Python packages required by the system.
- `README.md`: This file, providing detailed information about the system.

## Licensing
This Car Rental System is released under the MIT License. You are free to use, modify, and distribute this software, provided that the original authorship is credited.

```txt
MIT License

Copyright (c) 2024 Mehrab Bhuiyan

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
```

## Known Issues
- **Login Issues:** Some users may experience problems logging in due to incorrect password hashing. Ensure that the database is correctly set up and the `bcrypt` library is properly installed.
- **AI Recommendations:** The recommendation system might not always return results if the user’s preferences are too specific or there is insufficient data in the database.

## Credits
Developed by:

- **Mehrab Bhuiyan**
  - Email: mehrabhuiyan@gmail.com
  - GitHub: [Mehrab Bhuiyan](https://github.com/MehrabBhuiyan)
  - Institution: Yoobee Colleges

Special thanks to my instructors and colleagues for their guidance and support during the development of this project.
