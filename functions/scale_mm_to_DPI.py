from functions.mm_to_inch import mm_to_inch


def scale_mm_to_DPI(mm,DPI):


    return int(mm_to_inch(mm)*DPI)