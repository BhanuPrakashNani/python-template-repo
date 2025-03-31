from typing import List, Dict, Optional

class AIConversationClient:
    def send_message(self, message: str, context: Optional[Dict] = None) -> str:
        raise NotImplementedError("Implement in concrete class")
    
    def get_history(self, session_id: str, limit: int = 5) -> List[Dict]:
        raise NotImplementedError("Implement in concrete class")