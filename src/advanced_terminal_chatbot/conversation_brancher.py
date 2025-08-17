"""
Conversation branching system for multiple conversation threads.
"""

import json
import time
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path
import hashlib
from .context_manager import ContextManager


@dataclass
class ConversationBranch:
    """Represents a conversation branch."""
    id: str
    name: str
    parent_id: Optional[str]
    context_id: str
    created_at: float
    updated_at: float
    messages: List[Dict[str, str]]
    metadata: Dict[str, Any]
    is_active: bool
    tags: List[str]


class ConversationBrancher:
    """Manages multiple conversation branches and threads."""
    
    def __init__(self, context_manager: ContextManager, storage_dir: str = ".chatbot_branches"):
        """Initialize the conversation brancher."""
        self.context_manager = context_manager
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True)
        
        self.branches: Dict[str, ConversationBranch] = {}
        self.current_branch_id: Optional[str] = None
        self.branch_history: List[str] = []  # Stack for branch navigation
        
        # Load existing branches
        self._load_branches()
    
    def create_branch(self, name: str, context_id: str = None, parent_id: str = None, 
                      tags: List[str] = None, metadata: Dict[str, Any] = None) -> str:
        """Create a new conversation branch."""
        branch_id = self._generate_branch_id(name)
        
        # Use current context if none specified
        if not context_id:
            current_context = self.context_manager.get_current_context()
            if current_context:
                context_id = current_context.id
            else:
                # Create a default context
                context_id = self.context_manager.create_context(name, f"Conversation branch: {name}")
        
        branch = ConversationBranch(
            id=branch_id,
            name=name,
            parent_id=parent_id,
            context_id=context_id,
            created_at=time.time(),
            updated_at=time.time(),
            messages=[],
            metadata=metadata or {},
            is_active=True,
            tags=tags or []
        )
        
        self.branches[branch_id] = branch
        
        # If this is the first branch, make it current
        if not self.current_branch_id:
            self.current_branch_id = branch_id
        
        self._save_branches()
        return branch_id
    
    def switch_branch(self, branch_id: str) -> bool:
        """Switch to a different conversation branch."""
        if branch_id in self.branches:
            # Add current branch to history if it exists
            if self.current_branch_id:
                self.branch_history.append(self.current_branch_id)
            
            self.current_branch_id = branch_id
            self.branches[branch_id].updated_at = time.time()
            self.branches[branch_id].is_active = True
            
            # Switch context to match the branch
            branch = self.branches[branch_id]
            self.context_manager.switch_context(branch.context_id)
            
            self._save_branches()
            return True
        return False
    
    def get_current_branch(self) -> Optional[ConversationBranch]:
        """Get the current active branch."""
        if self.current_branch_id:
            return self.branches[self.current_branch_id]
        return None
    
    def add_message_to_branch(self, role: str, content: str, branch_id: str = None) -> bool:
        """Add a message to a specific branch."""
        if not branch_id:
            branch_id = self.current_branch_id
        
        if branch_id and branch_id in self.branches:
            branch = self.branches[branch_id]
            branch.messages.append({
                'role': role,
                'content': content,
                'timestamp': time.time()
            })
            branch.updated_at = time.time()
            self._save_branches()
            return True
        return False
    
    def fork_branch(self, name: str, from_branch_id: str = None, 
                    include_history: bool = True) -> str:
        """Fork an existing branch to create a new one."""
        if not from_branch_id:
            from_branch_id = self.current_branch_id
        
        if not from_branch_id or from_branch_id not in self.branches:
            raise ValueError("No valid branch to fork from")
        
        source_branch = self.branches[from_branch_id]
        
        # Create new branch
        new_branch_id = self.create_branch(
            name=name,
            context_id=source_branch.context_id,
            parent_id=from_branch_id,
            tags=source_branch.tags.copy(),
            metadata=source_branch.metadata.copy()
        )
        
        new_branch = self.branches[new_branch_id]
        
        # Copy messages if requested
        if include_history:
            new_branch.messages = source_branch.messages.copy()
        
        self._save_branches()
        return new_branch_id
    
    def merge_branches(self, source_branch_ids: List[str], target_branch_id: str, 
                       merge_strategy: str = "append") -> bool:
        """Merge multiple branches into a target branch."""
        if target_branch_id not in self.branches:
            return False
        
        target_branch = self.branches[target_branch_id]
        all_messages = []
        
        # Collect messages from source branches
        for source_id in source_branch_ids:
            if source_id in self.branches:
                source_branch = self.branches[source_id]
                all_messages.extend(source_branch.messages)
        
        if merge_strategy == "append":
            # Append new messages to existing ones
            target_branch.messages.extend(all_messages)
        elif merge_strategy == "replace":
            # Replace all messages
            target_branch.messages = all_messages
        elif merge_strategy == "smart":
            # Smart merge: avoid duplicates and maintain order
            existing_content = set()
            for msg in target_branch.messages:
                existing_content.add(f"{msg['role']}:{msg['content']}")
            
            for msg in all_messages:
                msg_key = f"{msg['role']}:{msg['content']}"
                if msg_key not in existing_content:
                    target_branch.messages.append(msg)
                    existing_content.add(msg_key)
        
        target_branch.updated_at = time.time()
        self._save_branches()
        return True
    
    def get_branch_tree(self) -> Dict[str, Any]:
        """Get a tree representation of all branches."""
        tree = {}
        
        # Find root branches (no parent)
        root_branches = [branch for branch in self.branches.values() if not branch.parent_id]
        
        for root_branch in root_branches:
            tree[root_branch.id] = self._build_branch_subtree(root_branch.id)
        
        return tree
    
    def _build_branch_subtree(self, branch_id: str) -> Dict[str, Any]:
        """Build a subtree for a specific branch."""
        branch = self.branches[branch_id]
        subtree = {
            'id': branch.id,
            'name': branch.name,
            'created_at': branch.created_at,
            'updated_at': branch.updated_at,
            'is_active': branch.is_active,
            'message_count': len(branch.messages),
            'children': []
        }
        
        # Find child branches
        children = [b for b in self.branches.values() if b.parent_id == branch_id]
        for child in children:
            subtree['children'].append(self._build_branch_subtree(child.id))
        
        return subtree
    
    def navigate_branch_history(self, direction: str = "back") -> Optional[str]:
        """Navigate through branch history (back/forward)."""
        if direction == "back" and self.branch_history:
            # Go back to previous branch
            previous_branch = self.branch_history.pop()
            if previous_branch in self.branches:
                self.switch_branch(previous_branch)
                return previous_branch
        elif direction == "forward" and self.branch_history:
            # Go forward (this would require a forward history stack)
            # For now, we'll implement a simple forward navigation
            pass
        
        return None
    
    def search_branches(self, query: str, limit: int = 5) -> List[ConversationBranch]:
        """Search branches based on name, tags, and content."""
        query_lower = query.lower()
        scored_branches = []
        
        for branch in self.branches.values():
            score = 0
            
            # Name relevance
            if query_lower in branch.name.lower():
                score += 3
            
            # Tag relevance
            for tag in branch.tags:
                if query_lower in tag.lower():
                    score += 1
            
            # Content relevance (search through messages)
            for message in branch.messages:
                if query_lower in message['content'].lower():
                    score += 0.5
            
            # Recency bonus
            days_old = (time.time() - branch.updated_at) / (24 * 3600)
            if days_old < 7:  # Recent branches get bonus
                score += 0.5
            
            if score > 0:
                scored_branches.append((branch, score))
        
        # Sort by score and return top results
        scored_branches.sort(key=lambda x: x[1], reverse=True)
        return [branch for branch, score in scored_branches[:limit]]
    
    def get_branch_suggestions(self, query: str) -> List[ConversationBranch]:
        """Get branch suggestions based on query."""
        return self.search_branches(query, limit=3)
    
    def archive_branch(self, branch_id: str) -> bool:
        """Archive a branch (mark as inactive)."""
        if branch_id in self.branches:
            self.branches[branch_id].is_active = False
            self.branches[branch_id].updated_at = time.time()
            
            # If archiving current branch, switch to parent or first available
            if branch_id == self.current_branch_id:
                branch = self.branches[branch_id]
                if branch.parent_id and branch.parent_id in self.branches:
                    self.switch_branch(branch.parent_id)
                else:
                    # Find first active branch
                    active_branches = [b for b in self.branches.values() if b.is_active]
                    if active_branches:
                        self.switch_branch(active_branches[0].id)
                    else:
                        self.current_branch_id = None
            
            self._save_branches()
            return True
        return False
    
    def delete_branch(self, branch_id: str, force: bool = False) -> bool:
        """Delete a branch permanently."""
        if branch_id not in self.branches:
            return False
        
        branch = self.branches[branch_id]
        
        # Check if branch has children
        children = [b for b in self.branches.values() if b.parent_id == branch_id]
        if children and not force:
            raise ValueError(f"Branch has {len(children)} children. Use force=True to delete anyway.")
        
        # Delete children first
        for child in children:
            del self.branches[child.id]
        
        # Delete the branch
        del self.branches[branch_id]
        
        # Update current branch if needed
        if branch_id == self.current_branch_id:
            # Switch to parent or first available branch
            if branch.parent_id and branch.parent_id in self.branches:
                self.switch_branch(branch.parent_id)
            else:
                remaining_branches = list(self.branches.values())
                if remaining_branches:
                    self.switch_branch(remaining_branches[0].id)
                else:
                    self.current_branch_id = None
        
        # Remove from history
        self.branch_history = [bid for bid in self.branch_history if bid != branch_id]
        
        self._save_branches()
        return True
    
    def export_branch(self, branch_id: str, format: str = "json") -> str:
        """Export a branch to various formats."""
        if branch_id not in self.branches:
            raise ValueError(f"Branch {branch_id} not found")
        
        branch = self.branches[branch_id]
        
        if format == "json":
            return json.dumps(asdict(branch), indent=2)
        elif format == "markdown":
            return self._branch_to_markdown(branch)
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def _branch_to_markdown(self, branch: ConversationBranch) -> str:
        """Convert branch to markdown format."""
        md = f"# {branch.name}\n\n"
        md += f"**Created**: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(branch.created_at))}\n"
        md += f"**Updated**: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(branch.updated_at))}\n"
        md += f"**Status**: {'Active' if branch.is_active else 'Archived'}\n\n"
        
        if branch.parent_id:
            parent = self.branches.get(branch.parent_id)
            if parent:
                md += f"**Parent Branch**: {parent.name}\n\n"
        
        if branch.tags:
            md += f"**Tags**: {', '.join([f'`{tag}`' for tag in branch.tags])}\n\n"
        
        if branch.messages:
            md += f"## Messages ({len(branch.messages)})\n\n"
            for i, message in enumerate(branch.messages):
                timestamp = time.strftime('%H:%M:%S', time.localtime(message['timestamp']))
                md += f"**{message['role'].title()}** ({timestamp}): {message['content']}\n\n"
        
        if branch.metadata:
            md += "## Metadata\n\n"
            for key, value in branch.metadata.items():
                md += f"- **{key}**: {value}\n"
        
        return md
    
    def _generate_branch_id(self, name: str) -> str:
        """Generate a unique branch ID."""
        timestamp = str(int(time.time() * 1000))
        name_hash = hashlib.md5(name.encode()).hexdigest()[:8]
        return f"branch_{name_hash}_{timestamp}"
    
    def _load_branches(self):
        """Load branches from storage."""
        branches_file = self.storage_dir / "branches.json"
        if branches_file.exists():
            try:
                with open(branches_file, 'r') as f:
                    data = json.load(f)
                    for branch_data in data.values():
                        branch = ConversationBranch(**branch_data)
                        self.branches[branch.id] = branch
            except Exception as e:
                print(f"Warning: Could not load branches: {e}")
    
    def _save_branches(self):
        """Save branches to storage."""
        branches_file = self.storage_dir / "branches.json"
        try:
            with open(branches_file, 'w') as f:
                json.dump({branch.id: asdict(branch) for branch in self.branches.values()}, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save branches: {e}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about branches."""
        total_branches = len(self.branches)
        active_branches = len([b for b in self.branches.values() if b.is_active])
        archived_branches = total_branches - active_branches
        
        total_messages = sum(len(branch.messages) for branch in self.branches.values())
        
        if total_branches > 0:
            avg_messages_per_branch = total_messages / total_branches
        else:
            avg_messages_per_branch = 0
        
        return {
            'total_branches': total_branches,
            'active_branches': active_branches,
            'archived_branches': archived_branches,
            'total_messages': total_messages,
            'avg_messages_per_branch': round(avg_messages_per_branch, 2),
            'current_branch': self.current_branch_id,
            'branch_history_depth': len(self.branch_history),
            'storage_directory': str(self.storage_dir)
        }
