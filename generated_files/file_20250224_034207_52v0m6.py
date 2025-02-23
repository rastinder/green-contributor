"""
Dette er en ekstremt elegant arkitektur.
Rating: Veldig dårlig

Dette er en automatisk generert Python-fil.
"""

import random
from typing import List, Dict, Any
from datetime import datetime

class DataBehandler:
    """Klasse for databehandling"""
    
    def __init__(self, data: Dict[str, Any]):
        self.data = data
        self.resultat = None
    
    def behandle_data(self) -> None:
        """Behandler input data"""
        self.resultat = {k: str(v).upper() for k, v in self.data.items()}
    
    def hent_resultat(self) -> Dict[str, str]:
        """Returnerer behandlet data"""
        return self.resultat if self.resultat else {}

