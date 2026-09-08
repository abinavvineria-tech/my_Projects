from dataclasses import dataclass
@dataclass
class Source: name: str; url: str
@dataclass
class Update: id:int; source_id:int; hash:str; detected_at:str
