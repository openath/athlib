"Standard weights and measures"


def get_implement_weight(event_code, gender, age_group):
    """Return standard weights in KG, as a formatted string

    Because UKA and IAAF have odd and even codes, hopefully
    one function can do both.  Still looking for IAAF junior weights.

    See IAAF rules page 155
    """

    if event_code == "JT":
        if gender == "M":
            if age_group == "U13":
                return "400"
            elif age_group == "U15":
                return "600"
            elif age_group == "U17":
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
                return "700"
        if gender == "F":
            if age_group == "U13":
                return "400"
            elif age_group == "U15":
                return "500"
            elif age_group == "U17":
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
            elif age_group == "U15":
                return "4.00"
            elif age_group == "U17":
                return "5.00"
            elif age_group == "U20":
                return "6.00"
            elif age_group in ("U23", "SEN", "V35", "V40", "V45"):
                return "7.26"
            elif age_group in ("V50", "V55"):
                return "6.00"
            elif age_group in ("V60", "V65", "V70"):
                return "5.00"
        elif gender == "F":
            if age_group == "U13":
                return "2.72"
            elif age_group == "U15":
                return "3.00"
            elif age_group == "U17":
                return "3.00"
            elif age_group in ("U20", "U23", "SEN", "V35", "V40", "V45"):
                return "4.00"
            elif age_group >= "V50":
                return "3.00"

    elif event_code == "DT":
        if gender == "M":
            if age_group == "U13":
                return "1.00"
            elif age_group == "U15":
                return "1.25"
            elif age_group == "U17":
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
            if age_group == "U13":
                return "0.75"
            elif age_group >= "V75":
                return "0.75"
            else:
                return "1.00"

    elif event_code == "HT":
        if gender == "M":
            if age_group == "U13":
                return "3.00"
            elif age_group == "U15":
                return "4.00"
            elif age_group == "U17":
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
            elif age_group == "U15":
                return "3.00"
            elif age_group == "U17":
                return "3.00"
            elif age_group in ("U20", "U23", "SEN", "V35", "V40", "V45"):
                return "4.00"
            elif age_group in ("V50", "V55", "V60", "V65", "V70"):
                return "3.00"
            elif age_group >= "V75":
                return "2.00"


        # default is we don't know
        return ""
