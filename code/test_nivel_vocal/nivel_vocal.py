import numpy as np

def get_nivel_vocal(data: list[np.ndarray], cal: float) -> list[float]:
    """Dada una lista con las grabaciones, calcular el nivel vocal del archivo a 85,
    80 y 70 dBHL."""

    audios_calibrados = [record/cal for record in data] #Calibro los audios

    return list(map(lambda x: np.sqrt(np.mean(x**2)), audios_calibrados)) #Calculo el nivel vocal