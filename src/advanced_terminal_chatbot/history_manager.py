"""
History management for persistent conversation storage.
"""

import sqlite3
import json
import uuid
from datetime import datetime
from typing import List, Dict, Optional, Any
from pathlib import Path


class HistoryManager:
    """Manages persistent conversation history using SQLite."""

    def __init__(self, db_path: str = "chatbot_history.db"):
        """Initialize the history manager with database path."""
        self.db_path = Path(db_path)
        self._init_database()

    def _init_database(self) -> None:
        """Initialize the database with required tables."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id TEXT PRIMARY KEY,
                    timestamp DATETIME,
                    provider TEXT,
                    model TEXT,
                    messages TEXT,
                    title TEXT
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS command_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    command TEXT,
                    timestamp DATETIME
                )
            """)
            conn.commit()

    def save_conversation(self, messages: List[Dict[str, str]], provider: str, 
                         model: str, session_id: Optional[str] = None) -> str:
        """Save a conversation to the database."""
        if not session_id:
            session_id = str(uuid.uuid4())
        
        timestamp = datetime.now()
        messages_json = json.dumps(messages)
        
        # Generate title from first user message
        title = "New Conversation"
        for msg in messages:
            if msg.get("role") == "user":
                title = msg.get("content", "")[:50] + ("..." if len(msg.get("content", "")) > 50 else "")
                break
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO conversations 
                (id, timestamp, provider, model, messages, title)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (session_id, timestamp, provider, model, messages_json, title))
            conn.commit()
        
        return session_id

    def load_conversation(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Load a conversation from the database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT timestamp, provider, model, messages, title
                FROM conversations WHERE id = ?
            """, (session_id,))
            
            row = cursor.fetchone()
            if row:
                return {
                    "id": session_id,
                    "timestamp": row[0],
                    "provider": row[1],
                    "model": row[2],
                    "messages": json.loads(row[3]),
                    "title": row[4]
                }
        return None

    def list_conversations(self, limit: int = 20) -> List[Dict[str, Any]]:
        """List recent conversations."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT id, timestamp, provider, model, title
                FROM conversations 
                ORDER BY timestamp DESC 
                LIMIT ?
            """, (limit,))
            
            return [
                {
                    "id": row[0],
                    "timestamp": row[1],
                    "provider": row[2],
                    "model": row[3],
                    "title": row[4]
                }
                for row in cursor.fetchall()
            ]

    def export_conversation(self, session_id: str, format_type: str = "json") -> Optional[str]:
        """Export a conversation in the specified format."""
        conversation = self.load_conversation(session_id)
        if not conversation:
            return None

        if format_type.lower() == "json":
            return json.dumps(conversation, indent=2, default=str)
        
        elif format_type.lower() == "markdown":
            md_content = f"# Conversation Export\n\n"
            md_content += f"**Session ID:** {conversation['id']}\n"
            md_content += f"**Timestamp:** {conversation['timestamp']}\n"
            md_content += f"**Provider:** {conversation['provider']}\n"
            md_content += f"**Model:** {conversation['model']}\n\n"
            md_content += "## Messages\n\n"
            
            for msg in conversation['messages']:
                role = "**User:**" if msg['role'] == 'user' else "**Assistant:**"
                md_content += f"{role}\n{msg['content']}\n\n---\n\n"
            
            return md_content
        
        elif format_type.lower() == "txt":
            txt_content = f"Conversation Export\n"
            txt_content += f"Session ID: {conversation['id']}\n"
            txt_content += f"Timestamp: {conversation['timestamp']}\n"
            txt_content += f"Provider: {conversation['provider']}\n"
            txt_content += f"Model: {conversation['model']}\n\n"
            txt_content += "Messages:\n\n"
            
            for msg in conversation['messages']:
                role = "User:" if msg['role'] == 'user' else "Assistant:"
                txt_content += f"{role}\n{msg['content']}\n\n---\n\n"
            
            return txt_content
        
        return None

    def save_command(self, command: str) -> None:
        """Save a command to history."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO command_history (command, timestamp)
                VALUES (?, ?)
            """, (command, datetime.now()))
            conn.commit()

    def get_command_history(self, limit: int = 100) -> List[str]:
        """Get command history."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT command FROM command_history 
                ORDER BY timestamp DESC 
                LIMIT ?
            """, (limit,))
            
            return [row[0] for row in cursor.fetchall()]

    def delete_conversation(self, session_id: str) -> bool:
        """Delete a conversation from the database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("DELETE FROM conversations WHERE id = ?", (session_id,))
            conn.commit()
            return cursor.rowcount > 0

    def clear_all_history(self) -> None:
        """Clear all conversation and command history."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM conversations")
            conn.execute("DELETE FROM command_history")
            conn.commit()
