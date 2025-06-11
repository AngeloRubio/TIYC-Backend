import mysql.connector
from typing import Dict, Any
import os
from contextlib import contextmanager
from mysql.connector import Error

class DatabaseConnection:
    """Clase para manejar la conexión a la base de datos MySQL."""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance._connection = None
        return cls._instance
    
    def __init__(self):
        self._db_config = {
            "host": os.getenv("DB_HOST", "localhost"),
            "user": os.getenv("DB_USER", "root"),
            "password": os.getenv("DB_PASSWORD", "angelo"), # esta contraseña es temporal y local
            "database": os.getenv("DB_NAME", "santa_fe"),
        }
    
    @contextmanager
    def get_cursor(self, dictionary=True):
        """
        Proporciona un cursor para ejecutar consultas SQL.
        Gestiona la conexión y el cierre automáticamente.
        """
        if self._connection is None or not self._connection.is_connected():
            try:
                self._connection = mysql.connector.connect(**self._db_config)
            except Error as e:
                raise Exception(f"Error al conectar a MySQL: {e}")
                
        cursor = self._connection.cursor(dictionary=dictionary)
        try:
            yield cursor
            self._connection.commit()
        except Error as e:
            self._connection.rollback()
            raise Exception(f"Error en la operación de base de datos: {e}")
        finally:
            cursor.close()
    
    def close(self):
        """Cierra la conexión a la base de datos."""
        if self._connection and self._connection.is_connected():
            self._connection.close()
