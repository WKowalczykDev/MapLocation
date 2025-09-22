def map_scale(real_width_m, map_width_mm):
    """
    Oblicza skalę mapy na podstawie szerokości rzeczywistej (metry)
    i szerokości na mapie (milimetry).
    Zwraca skalę w postaci 1:n
    """
    # Zamiana metrów na milimetry
    real_width_mm = real_width_m * 1000
    scale_ratio = real_width_mm / map_width_mm
    return scale_ratio