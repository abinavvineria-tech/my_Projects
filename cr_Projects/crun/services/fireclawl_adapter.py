# CRUN adapter — graceful fallback when unavailable
class FireClawlAdapter:
    def __init__(self): pass
    def check(self): return {"available": False, "reason": "FireClawl not installed"}
