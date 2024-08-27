from enum import Enum

class TeslaStore(int, Enum):
    def __new__(cls, value, label):
        obj = int.__new__(cls, value)
        obj._value_ = value
        obj.label = label
        return obj
    
    @classmethod
    def _missing_(cls, value):
        # This method is called when a value is not found in the enum
        return cls.NA

    NA = (0, 'N/A')
    A = (3693, 'Augsburg Gersthofen')
    BMOB = (9194, 'Berlin - Mall of Berlin')
    BREI = (18426, 'Berlin Reinickendorf')
    BSCH = (9556, 'Berlin Schönefeld')
    BSCHDEV = (16302, 'Berlin Schönefeld Delivery Hub')
    # Bielefeld ID?
    BS = (25762, 'Braunschweig Ölper')
    HB = (10512, 'Bremen Ottersberg')
    DO = (9467, 'Dortmund Holzwickede')
    DD = (14848, 'Dresden Kesselsdorf')
    DU = (13495, 'Duisburg Obermeiderich')
    D = (14845, 'Düsseldorf Lierenfeld')
    # Erfurt ID?
    FL = (439754, 'Flensburg Gallerie Pop Up')
    F = (20906, 'Frankfurt Ostend')
    FR = (9093, 'Freiburg Gundelfingen')
    FUE = (28719, 'Fürth Hardhöhe')
    GI = (28725, 'Gießen An der Automeile')
    HH = (4225, 'Hamburg Wandsbek')
    H = (3951, 'Hannover Wülfel')
    HD = (438015, 'Heidelberg Altstadt Pop Up')
    HN = (3692, 'Heilbronn Sontheim')
    IN = (18430, 'Ingolstadt Oberhaunstadt')
    KA = (3690, 'Karlsruhe Rintheim')
    KI = (9095, 'Kiel Gettorf')
    KO = (18422, 'Koblenz Mülheim-Kärlich')
    K = (2841, 'Köln Mülheim')
    # Leipzig ID?
    MD = (20823, 'Magdeburg Großer Silberberg')
    MA = (1501, 'Mannheim Friedrichsfeld')
    # Memmingen ID?
    MFR = (2614, 'München Freiham')
    MPA = (18423, 'München Parsdorf')
    NU = (15929, 'Neu-Ulm Schwaighofen')
    N = (1250, 'Nürnberg St. Jobst')
    # Oldenburg ID?
    # Regensburg ID?
    RO = (439780, 'Rosenheim Innenstadt Pop Up')
    # Rostock Altstadt Pop Up ID?
    HRONI = (9098, 'Rostock Nienhagen')
    SB = (26292, 'Saarbrücken Brebach-Fechingen')
    SHO = (27044, 'Stuttgart Holzgerlingen Sales, Used Car & Delivery Center')
    SWEI = (28717, 'Stuttgart Weinstadt')

    @classmethod
    def from_str(cls, input_str):
        for TeslaStore in cls:
            if TeslaStore.label == input_str:
                return TeslaStore
        raise ValueError(f"{cls.__name__} has no value matching {input_str}")