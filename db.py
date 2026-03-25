#!/usr/bin/env python3
"""
db.py - Shared MySQL connection helper for KultureKonnect.

Fill in YOUR_HOST, YOUR_USER, and YOUR_PASSWORD before running.
The database name must match the MySQL database you created (PLP2).
"""

import mysql.connector

DB_CONFIG = {
    "host": "mysql-5d3ad6b-alustudent-5222.e.aivencloud.com",
    "port": 15467,  # <-- replace with the port shown in your Aiven console
    "user": "avnadmin",
    "password": "REDACTED_SECRET",
    "database": "defaultdb",
    "ssl_disabled": False,
    "ssl_ca": "ca.pem",
    "ssl_verify_cert": True,
    "ssl_verify_identity": True,
}


def get_connection():
    """Return a live mysql.connector connection to the PLP2 database."""
    return mysql.connector.connect(**DB_CONFIG)
