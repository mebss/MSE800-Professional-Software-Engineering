import mysql.connector
import configparser

class DatabaseConnection:
    _instance = None

    def __init__(self):
        if DatabaseConnection._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            DatabaseConnection._instance = self
            self.connection = None
            self.connection = self.create_connection()

    @staticmethod
    def get_instance():
        if DatabaseConnection._instance is None:
            DatabaseConnection()
        return DatabaseConnection._instance

    def create_connection(self):
        try:
            # Read database configuration from config.ini
            config = configparser.ConfigParser()
            config.read('config.ini')
            host = config['mysql']['host']
            user = config['mysql']['user']
            password = config['mysql']['password']
            database = config['mysql']['database']

            # Connect to MySQL server
            print("Attempting to connect to MySQL server...")
            connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password
            )
            if connection.is_connected():
                print("Successfully connected to MySQL server")
                self.connection = connection
                self.create_or_use_database(connection, database)
                return connection
        except mysql.connector.Error as e:
            print(f"Error: '{e}' occurred while connecting to MySQL database")

    def create_or_use_database(self, connection, db_name):
        cursor = connection.cursor()
        cursor.execute(f"SHOW DATABASES LIKE '{db_name}'")
        result = cursor.fetchone()

        if result:
            print(f"Database '{db_name}' already exists. Using the existing database.")
        else:
            cursor.execute(f"CREATE DATABASE {db_name}")
            print(f"Database '{db_name}' created.")
        
        cursor.execute(f"USE {db_name}")
        self.create_tables(cursor)
        self.connection.commit()

    def create_tables(self, cursor):
        print("Creating users table...")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INT AUTO_INCREMENT PRIMARY KEY,
            first_name VARCHAR(50),
            last_name VARCHAR(50),
            email VARCHAR(100) UNIQUE,
            phone VARCHAR(15),
            role ENUM('admin', 'customer') DEFAULT 'customer',
            password_hash VARCHAR(255)  -- Assuming you're storing hashed passwords
        );
        """)
        print("Users table created or already exists.")

        # Insert default admin account if it doesn't exist
        cursor.execute("SELECT * FROM users WHERE role='admin'")
        if cursor.fetchone() is None:
            cursor.execute("""
            INSERT INTO users (first_name, last_name, email, phone, role, password_hash)
            VALUES ('Admin', 'User', 'admin@example.com', '000-000-0000', 'admin', 'hashed_password')
            """)
            self.connection.commit()
            print("Default admin account created.")

        print("Creating cars table...")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS cars (
            car_id INT AUTO_INCREMENT PRIMARY KEY,
            make VARCHAR(50),
            model VARCHAR(50),
            year INT,
            mileage INT,
            available BOOLEAN DEFAULT TRUE,
            rental_rate DECIMAL(10, 2)
        );
        """)
        print("Cars table created or already exists.")

        print("Creating rentals table...")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS rentals (
            rental_id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            car_id INT,
            rental_start_date DATE,
            rental_end_date DATE,
            total_cost DECIMAL(10, 2),
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (car_id) REFERENCES cars(car_id)
        );
        """)
        print("Rentals table created or already exists.")

        print("Creating locations table...")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS locations (
            location_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            address VARCHAR(255)
        );
        """)
        print("Locations table created or already exists.")

    def close_connection(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("MySQL connection is closed")

# Run the database setup
if __name__ == "__main__":
    db_connection = DatabaseConnection.get_instance()
    db_connection.close_connection()
