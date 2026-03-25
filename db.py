#!/usr/bin/env python3
"""
db.py - Shared MySQL connection helper for KultureKonnect.

Fill in YOUR_HOST, YOUR_USER, and YOUR_PASSWORD before running.
The database name must match the MySQL database you created (PLP2).
"""

import mysql.connector
import os


def _env_bool(name, default=False):
    return os.getenv(name, str(default)).lower() in ("true", "1", "yes")


DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "user": os.getenv("DB_USER", ""),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "defaultdb"),
    "ssl_disabled": _env_bool("DB_SSL_DISABLED", False),
    "ssl_ca": os.getenv("DB_SSL_CA", "ca.pem"),
    "ssl_verify_cert": _env_bool("DB_SSL_VERIFY_CERT", True),
    "ssl_verify_identity": _env_bool("DB_SSL_VERIFY_IDENTITY", True),
}


def get_connection():
    """Return a live mysql.connector connection to the PLP2 database."""
    return mysql.connector.connect(**DB_CONFIG)
