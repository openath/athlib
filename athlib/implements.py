"Standard weights and measures"


def get_implement_weight(event_code:str, gender: str, age_group: str) -> str:
    """Return standard weights in KG, as a formatted string

    Because UKA and IAAF have odd and even codes, hopefully
    one function can do both.  

    IAAF weights provided by Edwin Attard of Malta in Aug 2018

    See IAAF rules page 155
    """
    if event_code == "JT":
        if gender == "M":
            if age_group == "U13":
                return "400"
            elif age_group == "U14":
                return "500"
            elif age_group in ["U15", "U16"]:
                return "600"
            elif age_group in ["U17", "U18"]:
                return "700"
            elif age_group in ("U20", "U23", "SEN", "V35", "V40", "V45"):
                return "800"
            elif age_group in ("V50", "V55"):
                return "700"
            elif age_group in ("V60", "V65"):
                return "600"
            elif age_group in ("V70", "V75"):
                return "500"
            elif age_group >= "V80":
                return "400"
        if gender == "F":
            if age_group in ["U13", "U14"]:
                return "400"
            elif age_group in ["U15", "U16"]:
                return "500"
            elif age_group in ["U17", "U18"]:
                return "500"
            elif age_group in ("U20", "U23", "SEN", "V35", "V40", "V45"):
                return "600"
            elif age_group in ("V50", "V55", "V60", "V65", "V70"):
                return "500"
            elif age_group >= "V75":
                return "400"

    elif event_code == "SP":
        if gender == "M":
            if age_group == "U13":
                return "3.25"
            elif age_group == "U14":
                return "3.00"  # Malta
            elif age_group in ["U15", "U16"]:
                return "4.00"
            elif age_group in ["U17", "U18"]:
                return "5.00"
            elif age_group == "U20":
                return "6.00"
            elif age_group in ("U23", "SEN", "V35", "V40", "V45"):
                return "7.26"
            elif age_group in ("V50", "V55"):
                return "6.00"
            elif age_group in ("V60", "V65"):
                return "5.00"
            elif age_group in ("V70", "V75"):
                return "4.00"
            elif age_group >= "V80":
                return "3.00"

        elif gender == "F":
            if age_group == "U13":
                return "2.72"
            elif age_group == "U14":
                return "2.00"
            elif age_group in ["U15", "U16"]:
                return "3.00"
            elif age_group in ["U17", "U18"]:
                return "3.00"
            elif age_group in ("U20", "U23", "SEN", "V35", "V40", "V45"):
                return "4.00"
            elif age_group in ("V50", "V55", "V60", "V65", "V70"):
                return "3.00"
            elif age_group >= "V75":
                return "2.00"

    elif event_code == "DT":
        if gender == "M":
            if age_group in ["U13", "U14"]:
                return "1.00"
            elif age_group in ["U15", "U16"]:
                return "1.25"
            elif age_group in ["U17", "U18"]:
                return "1.50"
            elif age_group == "U20":
                return "1.75"
            elif age_group in ("U23", "SEN", "V35", "V40", "V45"):
                return "2.00"
            elif age_group in ("V50", "V55"):
                return "1.50"
            elif age_group >= "V60":
                return "1.00"

        elif gender == "F":
            if age_group in ["U13", "U14"]:
                return "0.75"
            elif age_group >= "V75":
                return "0.75"
            else:
                return "1.00"

    elif event_code == "HT":
        if gender == "M":
            if age_group in ["U13", "U14"]:
                return "3.00"
            elif age_group in ["U15", "U16"]:
                return "4.00"
            elif age_group in ["U17", "U18"]:
                return "5.00"
            elif age_group == "U20":
                return "6.00"
            elif age_group in ("U23", "SEN", "V35", "V40", "V45"):
                return "7.26"
            elif age_group in ("V50", "V55"):
                return "6.00"
            elif age_group in ("V60", "V65"):
                return "5.00"
            elif age_group in ("V70", "V75"):
                return "4.00"
            elif age_group >= "V80":
                return "3.00"

        elif gender == "F":
            if age_group == "U13":
                return "3.00"
            elif age_group == "U14":
                return "2.00"  # light one in Malta
            elif age_group in ["U15", "U16"]:
                return "3.00"
            elif age_group in ["U17", "U18"]:
                return "3.00"
            elif age_group in ("U20", "U23", "SEN", "V35", "V40", "V45"):
                return "4.00"
            elif age_group in ("V50", "V55", "V60", "V65", "V70"):
                return "3.00"
            elif age_group >= "V75":
                return "2.00"

    elif event_code == "WT":
        if gender == "M":
            if age_group in ("V35", "V40", "V45"):
                return "15.88"
            elif age_group in ("V50", "V55"):
                return "11.34"
            elif age_group in ("V60", "V65"):
                return "9.08"
            elif age_group in ("V70", "V75"):
                return "7.26"
            elif age_group >= "V80":
                return "5.45"
            else:
                return "15.88"

        elif gender == "F":
            if age_group in ("V35", "V40", "V45"):
                return "9.08"
            elif age_group in ("V50", "V55"):
                return "7.26"
            elif age_group in ("V60", "V65", "V70"):
                return "5.45"
            elif age_group >= "V75":
                return "4.00"
            else:
                return "9.08"


    # default is we don't know
    return ""

def get_specific_event_code(generic_event_code: str, gender: str, age_group: str) -> str:
    "Given e.g. 'SP', return 'SP7.26K"

    if generic_event_code not in ["SP", "HT", "JT", "DT", "WT"]:
        return generic_event_code

    txt_weight = get_implement_weight(generic_event_code, gender, age_group)
    # print("    implement weight for %s %s %s as text is %s" % (generic_event_code, gender, age_group, txt_weight))
    mass = float(txt_weight)

    if mass == int(mass):
        mass = int(mass)  # 4.00 becomes integer 4

    formatted = "%s%s" % (generic_event_code, mass)
    if mass < 99:  # kg
        formatted += 'K'
    return formatted
