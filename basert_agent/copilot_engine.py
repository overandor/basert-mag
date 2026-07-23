import os
import re
from typing import List, Dict, Any, Optional

class CopilotContextHarvester:
    """GitHub Copilot Reverse-Engineered Context Harvesting Engine.
    
    Inspired by github.copilot-1.57.7193 extension architecture:
    1. Harvests prefix & suffix surrounding cursor.
    2. Ranks open neighboring editor tabs by Jaccard path & import similarity.
    3. Formats prompt with path headers ('// Path: relative/file.ext').
    4. Truncates context to token budget.
    """

    def __init__(self, max_prompt_tokens: int = 2048):
        self.max_prompt_tokens = max_prompt_tokens

    def token_estimate(self, text: str) -> int:
        return max(1, len(text) // 4)

    def rank_neighboring_tabs(self, active_path: str, open_tabs: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """Rank neighboring editor tabs based on path proximity and shared imports."""
        active_dir = os.path.dirname(active_path)
        active_ext = os.path.splitext(active_path)[1]
        
        ranked = []
        for tab in open_tabs:
            tab_path = tab.get("path", "")
            if tab_path == active_path:
                continue
            
            score = 0.0
            # Same directory bonus
            if os.path.dirname(tab_path) == active_dir:
                score += 3.0
            # Same extension bonus
            if os.path.splitext(tab_path)[1] == active_ext:
                score += 2.0
                
            content = tab.get("content", "")
            # Word token overlap
            active_words = set(re.findall(r'\w+', active_path))
            tab_words = set(re.findall(r'\w+', tab_path))
            jaccard = len(active_words & tab_words) / float(max(1, len(active_words | tab_words)))
            score += jaccard * 5.0
            
            ranked.append((score, tab))
            
        ranked.sort(key=lambda x: x[0], reverse=True)
        return [item[1] for item in ranked[:3]]

    def construct_copilot_prompt(
        self,
        active_path: str,
        prefix: str,
        suffix: str = "",
        neighboring_tabs: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """Construct structured Copilot prompt payload."""
        prompt_parts = []
        
        # 1. Neighboring context tabs
        if neighboring_tabs:
            top_neighbors = self.rank_neighboring_tabs(active_path, neighboring_tabs)
            for tab in top_neighbors:
                path = tab.get("path", "file.py")
                code = tab.get("content", "").strip()
                if code:
                    prompt_parts.append(f"// Path: {path}\n{code}\n")

        # 2. Active file header & prefix
        rel_active = os.path.basename(active_path)
        prompt_parts.append(f"// Path: {rel_active}\n{prefix}")
        
        full_prompt = "\n\n".join(prompt_parts)
        
        # 3. Token budget enforcement
        tokens = self.token_estimate(full_prompt)
        
        return {
            "active_path": active_path,
            "full_prompt": full_prompt,
            "token_count": tokens,
            "prefix_length": len(prefix),
            "suffix_length": len(suffix),
            "has_suffix": bool(suffix)
        }

class GhostTextPostProcessor:
    """Post-processes raw LLM outputs into clean ghost text inline completions."""
    
    @staticmethod
    def process_candidate(raw_completion: str, stop_sequences: Optional[List[str]] = None) -> str:
        stops = stop_sequences or ["\n\n", "def ", "class ", "function ", "import "]
        result = raw_completion
        for stop in stops:
            if stop in result:
                result = result.split(stop)[0]
        return result.strip()
