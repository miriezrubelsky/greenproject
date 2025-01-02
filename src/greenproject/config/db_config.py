import pathlib
import os
import greenproject


PACKAGE_ROOT = pathlib.Path(greenproject.__file__).resolve().parent

DB_CONFIG = {
    'host': 'postgres',
    'port': '5432',
    'dbname': 'postgres',
    'user': 'postgres',
    'password': '1234'
}