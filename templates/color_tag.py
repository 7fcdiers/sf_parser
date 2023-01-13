from pandas import DataFrame as df

def color(type: str, value: str):
    if type == "flow":
        if value == "Active":
            return "Green"
        else: 
            return "Red"

    elif type == "object":
        if value == "Custom":
            return "Blue"
        else:
            return "Green"

    elif type == "vr":
        if value == "True":
            return "Green"
        else:
            return "Red"

    else:
        return "Write" 