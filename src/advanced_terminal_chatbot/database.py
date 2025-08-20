"""Database manager for the chatbot."""

import sqlite3
from typing import List, Dict, Any, Optional

class DatabaseManager:
    """Manages the SQLite database for the chatbot."""

    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        """Create the necessary tables if they don&#39;t exist."""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS contexts (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                created_at REAL,
                updated_at REAL,
                tags TEXT,
                metadata TEXT,
                conversation_summary TEXT,
                key_points TEXT,
                model_used TEXT,
                provider_used TEXT
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id TEXT PRIMARY KEY,
                content TEXT NOT NULL,
                context_id TEXT,
                importance REAL,
                created_at REAL,
                last_accessed REAL,
                access_count INTEGER,
                tags TEXT,
                type TEXT
            )
        """)
        self.conn.commit()

    def close(self):
        """Close the database connection."""
        self.conn.close()

    def execute_query(self, query: str, params: tuple = ()) -> None:
        """Execute a query that modifies the database."""
        self.cursor.execute(query, params)
        self.conn.commit()

    def fetch_one(self, query: str, params: tuple = ()) -> Optional[tuple]:
        """Fetch a single row from the database."""
        self.cursor.execute(query, params)
        return self.cursor.fetchone()

    def fetch_all(self, query: str, params: tuple = ()) -> List[tuple]:
        """Fetch all rows from the database."""
        self.cursor.execute(query, params)
        return self.cursor.fetchall()
