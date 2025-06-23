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
    
    # Austria
    AT_DO = (436108, 'Dornbirn Mühlebach Pop Up')
    AT_G = (18438, 'Graz Kalsdorf')
    AT_IL = (2938, 'Innsbruck')
    AT_KL = (8730, 'Klagenfurt')
    AT_L = (14839, 'Linz')
    AT_W = (9340, 'Wien')
    AT_S = (18435, 'Salzburg')

    # Belgium
    BE_AW = (32061, 'Awans')
    BE_BR = (14852, 'Brugge')

    # Czech Republic
    CZ_PR = (14499, 'Praha')

    # Denmark
    DK_AAL = (301419, 'Aalborg Storcenter')
    DK_HER = (436102, 'HerningCentret Pop Up')

    # Finland
    FI_ESP = (438603, 'Espo Pop Up')
    FI_TUR = (9118, 'Turku')
    FI_VAN = (26258, 'Vantaa Petikko')

    # France
    FR_NIC = (446007, 'Boutique éphémère Tesla Nice Cap3000')
    FR_MAR = (26558, 'Centre Tesla Aix-Marseille')
    FR_REN = (30673, 'Rennes Pacé')
    FR_ROU = (26278, 'Rouen Store')
    FR_BAY = (413853, 'Tesla Bayonne')
    FR_PAR = (407259, 'Tesla Paris St-Ouen')
    FR_TLN = (4004152, 'Toulon Delivery Hub')
    FR_VAL = (34251, 'Valenton Delivery Hub')

    # Germany
    DE_A = (3693, 'Augsburg Gersthofen')
    DE_BMOB = (9194, 'Berlin - Mall of Berlin')
    DE_BREI = (18426, 'Berlin Reinickendorf')
    DE_BSCH = (9556, 'Berlin Schönefeld')
    DE_BSCHDEV = (16302, 'Berlin Schönefeld Delivery Hub')
    DE_BS = (25762, 'Braunschweig Ölper')
    DE_HB = (10512, 'Bremen Ottersberg')
    DE_DO = (9467, 'Dortmund Holzwickede')
    DE_DON = (399978, 'Dortmund Innenstadt-Nord')
    DE_DD = (14848, 'Dresden Kesselsdorf')
    DE_DU = (13495, 'Duisburg Obermeiderich')
    DE_D = (14845, 'Düsseldorf Lierenfeld')
    DE_FL = (439754, 'Flensburg Gallerie Pop Up')
    DE_F = (20906, 'Frankfurt Ostend')
    DE_FR = (9093, 'Freiburg Gundelfingen')
    DE_FUE = (28719, 'Fürth Hardhöhe')
    DE_GI = (28725, 'Gießen An der Automeile')
    DE_HH = (4225, 'Hamburg Wandsbek')
    DE_H = (3951, 'Hannover Wülfel')
    DE_HD = (438015, 'Heidelberg Altstadt Pop Up')
    DE_HN = (3692, 'Heilbronn Sontheim')
    DE_IN = (18430, 'Ingolstadt Oberhaunstadt')
    DE_KA = (3690, 'Karlsruhe Rintheim')
    DE_KI = (9095, 'Kiel Gettorf')
    DE_KO = (18422, 'Koblenz Mülheim-Kärlich')
    DE_K = (2841, 'Köln Mülheim')
    DE_MD = (20823, 'Magdeburg Großer Silberberg')
    DE_MA = (1501, 'Mannheim Friedrichsfeld')
    DE_MFR = (2614, 'München Freiham')
    DE_MPA = (18423, 'München Parsdorf')
    DE_NU = (15929, 'Neu-Ulm Schwaighofen')
    DE_N = (1250, 'Nürnberg St. Jobst')
    DE_RO = (439780, 'Rosenheim Innenstadt Pop Up')
    DE_HRONI = (9098, 'Rostock Nienhagen')
    DE_SB = (26292, 'Saarbrücken Brebach-Fechingen')
    DE_SHO = (27044, 'Stuttgart Holzgerlingen Sales, Used Car & Delivery Center')
    DE_SWEI = (28717, 'Stuttgart Weinstadt')

    # Hungary
    HU_BUD = (12240, 'Tesla Center Budapest')

    # Italy
    IT_BOL = (406212, 'Bolzano')
    IT_MILBLO = (424509, 'Milano-Merlata Bloom Pop Up')

    # Netherlands
    NL_TA = (714, 'Tilburg-Asteriastraat')
    NL_ZG = (415466, 'Zeeland - Goes')

    # Norway
    NO_BOD = (26253, 'Bodø')
    NO_OSLSKI = (26256, 'Oslo-Ski')

    # Poland
    PL_KAT = (424807, 'Tesla Center Katowice')
    PL_POZ = (437313, 'Tesla Center Poznań')
    PL_WAR = (155134, 'Tesla Center Warszawa')

    # Romania
    RO_CLU = (444154, 'Pop Up Cluj')
    RO_TIM = (433906, 'Tesla Timișoara Pop Up')

    # Spain
    ES_BAR = (36156, 'Barcelona')
    ES_BIL = (21086, 'Bilbao')
    ES_MAD = (8675, 'Madrid')
    ES_MAL = (14704, 'Málaga')
    ES_MALL = (4001206, 'Mallorca')
    ES_SEV = (8680, 'Sevilla')
    ES_VALL = (35032, 'Valladolid Pop Up')
    ES_VAL = (58521, 'Valencia')
    ES_VIG = (407764, 'Vigo')

    # Sweden
    SE_JKG = (9120, '10 Mogölsvägen Jönköping')
    SE_OER = (413954, '1 Säljarevägen Örebro')

    # Switzerland
    CH_BASMOE = (481, 'Basel Möhlin')
    CH_BASSTA = (918, 'Basel St. Alban')
    CH_CHU = (442271, 'Chur Landquart Pop Up')
    CH_GEN = (26458, 'Geneva')
    CH_GENMEY = (298, 'Geneva Meyrin')
    CH_LAUBUS = (9554, 'Lausanne Bussigny')
    CH_LAULEF = (1425, 'Lausanne Le Flon')
    CH_SCH = (439823, 'Schaffhausen Neuhausen Pop Up')
    CH_STG = (1340, 'St. Gallen')
    CH_ZUEPEL = (505, 'Zürich Pelikanstrasse')
    CH_ZUESCH = (1257, 'Zürich Schlieren')
    CH_ZUEWIN = (236, 'Zürich Winterthur')

    # Turkey
    TR_ANKARM = (425125, 'Tesla Armada AVM')
    TR_ISTFRK = (445210, 'Tesla Ferko Line')
    TR_ISTMYDN = (449153, 'Tesla Istanbul Meydan AVM')
    TR_IZMISTPRK = (451952, 'Tesla İstinyePark İzmir')
    TR_DLVANK = (410805, 'Tesla Ankara Delivery Hub')
    TR_DLVIST = (442359, 'Tesla Delivery Istanbul')
    TR_DLVIZM = (460569, 'Tesla Delivery Gaziemir Izmir')

    # UK
    UK_STA = (14843, 'St Albans')
    UK_BIC = (58510, 'Tesla Centre Bicester')
    UK_MAN = (36192, 'Tesla Centre Manchester Central')
    UK_MIL = (17107, 'Tesla Centre Milton Keynes')
    UK_REA = (14754, 'Tesla Centre Reading')
    UK_SOL = (334993, 'Tesla Centre Solihull')
    UK_WOL = (400821, 'Tesla Centre Wolverhampton')
    UK_BRI = (1039, 'Tesla Certified Pre-Owned Centre Bristol')

    @classmethod
    def from_str(cls, input_str):
        for TeslaStore in cls:
            if TeslaStore.label == input_str:
                return TeslaStore
        raise ValueError(f"{cls.__name__} has no value matching {input_str}")
