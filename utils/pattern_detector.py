def detect_high_prob_pattern(data):
    """Detecta se há padrão de velas rasas (ex: 10 ou mais abaixo de 1.5x)"""
    rasas = [c for c in data if c["value"] < 1.5]
    if len(rasas) >= 10:
        return True, 0.95
    return False, 0.0
