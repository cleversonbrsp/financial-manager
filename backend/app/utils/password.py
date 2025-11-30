"""
Validação de senhas
"""
import re
from typing import Tuple

def validate_password_strength(password: str) -> Tuple[bool, str]:
    """
    Valida força da senha:
    - Mínimo 12 caracteres
    - Mínimo 2 letras maiúsculas
    - Mínimo 2 letras minúsculas
    - Mínimo 2 números
    - Mínimo 1 caractere especial
    """
    if len(password) < 12:
        return False, "A senha deve ter no mínimo 12 caracteres"
    
    uppercase_count = len(re.findall(r'[A-Z]', password))
    if uppercase_count < 2:
        return False, "A senha deve ter no mínimo 2 letras maiúsculas"
    
    lowercase_count = len(re.findall(r'[a-z]', password))
    if lowercase_count < 2:
        return False, "A senha deve ter no mínimo 2 letras minúsculas"
    
    digit_count = len(re.findall(r'[0-9]', password))
    if digit_count < 2:
        return False, "A senha deve ter no mínimo 2 números"
    
    special_count = len(re.findall(r'[!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>/?]', password))
    if special_count < 1:
        return False, "A senha deve ter no mínimo 1 caractere especial"
    
    return True, "Senha válida"

