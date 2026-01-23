import logging
import sys

# Logger centralizado para toda la herramienta
def get_logger(name="qa_engine"):
    """Obtiene o crea el logger centralizado"""
    logger = logging.getLogger(name)
    
    # Solo configurar si no tiene handlers
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
        ch.setFormatter(formatter)
        logger.addHandler(ch)
    
    return logger
