"""
Context management system for the terminal chatbot.
"""

import json
import time
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path
import hashlib


@dataclass
class Context:
    """Represents a conversation context."""
    id: str
    name: str
    description: str
    created_at: float
    updated_at: float
    tags: List[str]
    metadata: Dict[str, Any]
    conversation_summary: str
    key_points: List[str]
    model_used: str
    provider_used: str


@dataclass
class MemoryItem:
    """Represents a memory item for long-term storage."""
    id: str
    content: str
    context_id: str
    importance: float  # 0.0 to 1.0
    created_at: float
    last_accessed: float
    access_count: int
    tags: List[str]
    type: str  # 'fact', 'preference', 'instruction', 'example'


class ContextManager:
    """Manages conversation contexts and memory for better AI interactions."""
    
    def __init__(self, storage_dir: str = ".chatbot_context"):
        """Initialize the context manager."""
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True)
        
        self.contexts: Dict[str, Context] = {}
        self.memories: Dict[str, MemoryItem] = {}
        self.current_context_id: Optional[str] = None
        
        # Load existing contexts and memories
        self._load_contexts()
        self._load_memories()
    
    def create_context(self, name: str, description: str = "", tags: List[str] = None, 
                      metadata: Dict[str, Any] = None) -> str:
        """Create a new conversation context."""
        context_id = self._generate_context_id(name)
        
        context = Context(
            id=context_id,
            name=name,
            description=description or f"Conversation about {name}",
            created_at=time.time(),
            updated_at=time.time(),
            tags=tags or [],
            metadata=metadata or {},
            conversation_summary="",
            key_points=[],
            model_used="",
            provider_used=""
        )
        
        self.contexts[context_id] = context
        self._save_contexts()
        
        return context_id
    
    def switch_context(self, context_id: str) -> bool:
        """Switch to a different conversation context."""
        if context_id in self.contexts:
            self.current_context_id = context_id
            self.contexts[context_id].updated_at = time.time()
            self._save_contexts()
            return True
        return False
    
    def get_current_context(self) -> Optional[Context]:
        """Get the current active context."""
        if self.current_context_id:
            return self.contexts[self.current_context_id]
        return None
    
    def update_context_summary(self, summary: str, key_points: List[str] = None):
        """Update the current context with a conversation summary."""
        if self.current_context_id:
            context = self.contexts[self.current_context_id]
            context.conversation_summary = summary
            if key_points:
                context.key_points = key_points
            context.updated_at = time.time()
            self._save_contexts()
    
    def add_memory(self, content: str, importance: float = 0.5, tags: List[str] = None, 
                   memory_type: str = "fact") -> str:
        """Add a new memory item."""
        memory_id = self._generate_memory_id(content)
        
        memory = MemoryItem(
            id=memory_id,
            content=content,
            context_id=self.current_context_id or "global",
            importance=importance,
            created_at=time.time(),
            last_accessed=time.time(),
            access_count=1,
            tags=tags or [],
            type=memory_type
        )
        
        self.memories[memory_id] = memory
        self._save_memories()
        
        return memory_id
    
    def search_memories(self, query: str, limit: int = 5) -> List[MemoryItem]:
        """Search memories based on content and tags."""
        query_lower = query.lower()
        scored_memories = []
        
        for memory in self.memories.values():
            score = 0
            
            # Content relevance
            if query_lower in memory.content.lower():
                score += 2
            
            # Tag relevance
            for tag in memory.tags:
                if query_lower in tag.lower():
                    score += 1
            
            # Recency bonus
            days_old = (time.time() - memory.created_at) / (24 * 3600)
            if days_old < 7:  # Recent memories get bonus
                score += 0.5
            
            # Importance bonus
            score += memory.importance
            
            if score > 0:
                scored_memories.append((memory, score))
        
        # Sort by score and return top results
        scored_memories.sort(key=lambda x: x[1], reverse=True)
        return [memory for memory, score in scored_memories[:limit]]
    
    def get_relevant_context(self, query: str) -> Optional[Context]:
        """Get the most relevant context for a query."""
        if not self.contexts:
            return None
        
        # Simple relevance scoring based on name, description, and tags
        scored_contexts = []
        query_lower = query.lower()
        
        for context in self.contexts.values():
            score = 0
            
            if query_lower in context.name.lower():
                score += 3
            
            if query_lower in context.description.lower():
                score += 2
            
            for tag in context.tags:
                if query_lower in tag.lower():
                    score += 1
            
            # Recency bonus
            days_old = (time.time() - context.updated_at) / (24 * 3600)
            if days_old < 7:  # Recent contexts get bonus
                score += 0.5
            
            if score > 0:
                scored_contexts.append((context, score))
        
        if scored_contexts:
            scored_contexts.sort(key=lambda x: x[1], reverse=True)
            return scored_contexts[0][0]
        
        return None
    
    def get_context_suggestions(self, query: str) -> List[Context]:
        """Get context suggestions based on query."""
        relevant_contexts = []
        query_lower = query.lower()
        
        for context in self.contexts.values():
            relevance = 0
            
            if query_lower in context.name.lower():
                relevance += 2
            if query_lower in context.description.lower():
                relevance += 1
            for tag in context.tags:
                if query_lower in tag.lower():
                    relevance += 1
            
            if relevance > 0:
                relevant_contexts.append((context, relevance))
        
        relevant_contexts.sort(key=lambda x: x[1], reverse=True)
        return [context for context, relevance in relevant_contexts[:3]]
    
    def merge_contexts(self, context_ids: List[str], new_name: str, 
                      new_description: str = "") -> str:
        """Merge multiple contexts into one."""
        if len(context_ids) < 2:
            raise ValueError("Need at least 2 contexts to merge")
        
        # Create new merged context
        merged_id = self.create_context(new_name, new_description)
        merged_context = self.contexts[merged_id]
        
        # Combine summaries and key points
        summaries = []
        all_key_points = []
        all_tags = set()
        
        for context_id in context_ids:
            if context_id in self.contexts:
                context = self.contexts[context_id]
                if context.conversation_summary:
                    summaries.append(context.conversation_summary)
                all_key_points.extend(context.key_points)
                all_tags.update(context.tags)
        
        merged_context.conversation_summary = "\n\n".join(summaries)
        merged_context.key_points = list(set(all_key_points))  # Remove duplicates
        merged_context.tags = list(all_tags)
        
        # Update memories to point to new context
        for memory in self.memories.values():
            if memory.context_id in context_ids:
                memory.context_id = merged_id
        
        # Remove old contexts
        for context_id in context_ids:
            if context_id in self.contexts:
                del self.contexts[context_id]
        
        self._save_contexts()
        self._save_memories()
        
        return merged_id
    
    def export_context(self, context_id: str, format: str = "json") -> str:
        """Export a context to various formats."""
        if context_id not in self.contexts:
            raise ValueError(f"Context {context_id} not found")
        
        context = self.contexts[context_id]
        
        if format == "json":
            return json.dumps(asdict(context), indent=2)
        elif format == "markdown":
            return self._context_to_markdown(context)
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def _context_to_markdown(self, context: Context) -> str:
        """Convert context to markdown format."""
        md = f"# {context.name}\n\n"
        md += f"**Description**: {context.description}\n\n"
        md += f"**Created**: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(context.created_at))}\n"
        md += f"**Updated**: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(context.updated_at))}\n\n"
        
        if context.tags:
            md += f"**Tags**: {', '.join([f'`{tag}`' for tag in context.tags])}\n\n"
        
        if context.conversation_summary:
            md += f"## Summary\n\n{context.conversation_summary}\n\n"
        
        if context.key_points:
            md += "## Key Points\n\n"
            for point in context.key_points:
                md += f"- {point}\n"
            md += "\n"
        
        if context.metadata:
            md += "## Metadata\n\n"
            for key, value in context.metadata.items():
                md += f"- **{key}**: {value}\n"
        
        return md
    
    def _generate_context_id(self, name: str) -> str:
        """Generate a unique context ID."""
        timestamp = str(int(time.time() * 1000))
        name_hash = hashlib.md5(name.encode()).hexdigest()[:8]
        return f"ctx_{name_hash}_{timestamp}"
    
    def _generate_memory_id(self, content: str) -> str:
        """Generate a unique memory ID."""
        content_hash = hashlib.md5(content.encode()).hexdigest()[:8]
        timestamp = str(int(time.time() * 1000))
        return f"mem_{content_hash}_{timestamp}"
    
    def _load_contexts(self):
        """Load contexts from storage."""
        contexts_file = self.storage_dir / "contexts.json"
        if contexts_file.exists():
            try:
                with open(contexts_file, 'r') as f:
                    data = json.load(f)
                    for context_data in data.values():
                        context = Context(**context_data)
                        self.contexts[context.id] = context
            except Exception as e:
                print(f"Warning: Could not load contexts: {e}")
    
    def _save_contexts(self):
        """Save contexts to storage."""
        contexts_file = self.storage_dir / "contexts.json"
        try:
            with open(contexts_file, 'w') as f:
                json.dump({ctx.id: asdict(ctx) for ctx in self.contexts.values()}, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save contexts: {e}")
    
    def _load_memories(self):
        """Load memories from storage."""
        memories_file = self.storage_dir / "memories.json"
        if memories_file.exists():
            try:
                with open(memories_file, 'r') as f:
                    data = json.load(f)
                    for memory_data in data.values():
                        memory = MemoryItem(**memory_data)
                        self.memories[memory.id] = memory
            except Exception as e:
                print(f"Warning: Could not load memories: {e}")
    
    def _save_memories(self):
        """Save memories to storage."""
        memories_file = self.storage_dir / "memories.json"
        try:
            with open(memories_file, 'w') as f:
                json.dump({mem.id: asdict(mem) for mem in self.memories.values()}, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save memories: {e}")
    
    def cleanup_old_contexts(self, days_old: int = 30):
        """Remove contexts older than specified days."""
        cutoff_time = time.time() - (days_old * 24 * 3600)
        to_remove = []
        
        for context_id, context in self.contexts.items():
            if context.updated_at < cutoff_time:
                to_remove.append(context_id)
        
        for context_id in to_remove:
            del self.contexts[context_id]
        
        if to_remove:
            self._save_contexts()
            print(f"Removed {len(to_remove)} old contexts")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about contexts and memories."""
        total_contexts = len(self.contexts)
        total_memories = len(self.memories)
        
        if total_contexts > 0:
            avg_memories_per_context = total_memories / total_contexts
        else:
            avg_memories_per_context = 0
        
        return {
            'total_contexts': total_contexts,
            'total_memories': total_memories,
            'avg_memories_per_context': round(avg_memories_per_context, 2),
            'current_context': self.current_context_id,
            'storage_directory': str(self.storage_dir)
        }
