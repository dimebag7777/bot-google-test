import os
import pymysql
from pymysql.cursors import DictCursor
import bcrypt
import logging
from contextlib import contextmanager

logger = logging.getLogger(__name__)

# Database configuration from environment variables
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'password'),
    'database': os.getenv('DB_NAME', 'trading_bot_db'),
    'charset': 'utf8mb4',
    'cursorclass': DictCursor
}


@contextmanager
def get_db_connection():
    """Context manager for database connections"""
    connection = None
    try:
        connection = pymysql.connect(**DB_CONFIG)
        yield connection
        connection.commit()
    except Exception as e:
        if connection:
            connection.rollback()
        logger.error(f"Database error: {str(e)}")
        raise
    finally:
        if connection:
            connection.close()


def init_database():
    """Initialize database and create tables if they don't exist"""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                # Create users table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        username VARCHAR(50) UNIQUE NOT NULL,
                        email VARCHAR(100) UNIQUE NOT NULL,
                        password_hash VARCHAR(255) NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                        INDEX idx_email (email),
                        INDEX idx_username (username)
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
                """)
                logger.info("Database tables initialized successfully")
                return True
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")
        return False


class User:
    """User model for database operations"""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password using bcrypt"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        """Verify a password against its hash"""
        return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
    
    @staticmethod
    def create(username: str, email: str, password: str) -> dict:
        """Create a new user"""
        try:
            password_hash = User.hash_password(password)
            
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
                        (username, email, password_hash)
                    )
                    user_id = cursor.lastrowid
                    
                    return {
                        'id': user_id,
                        'username': username,
                        'email': email
                    }
        except pymysql.IntegrityError as e:
            if 'username' in str(e):
                raise ValueError("Username already exists")
            elif 'email' in str(e):
                raise ValueError("Email already exists")
            raise ValueError("User creation failed")
        except Exception as e:
            logger.error(f"Error creating user: {str(e)}")
            raise
    
    @staticmethod
    def find_by_email(email: str) -> dict:
        """Find a user by email"""
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "SELECT id, username, email, password_hash, created_at FROM users WHERE email = %s",
                        (email,)
                    )
                    return cursor.fetchone()
        except Exception as e:
            logger.error(f"Error finding user by email: {str(e)}")
            return None
    
    @staticmethod
    def find_by_id(user_id: int) -> dict:
        """Find a user by ID"""
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "SELECT id, username, email, created_at FROM users WHERE id = %s",
                        (user_id,)
                    )
                    return cursor.fetchone()
        except Exception as e:
            logger.error(f"Error finding user by ID: {str(e)}")
            return None
    
    @staticmethod
    def find_by_username(username: str) -> dict:
        """Find a user by username"""
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "SELECT id, username, email, created_at FROM users WHERE username = %s",
                        (username,)
                    )
                    return cursor.fetchone()
        except Exception as e:
            logger.error(f"Error finding user by username: {str(e)}")
            return None
