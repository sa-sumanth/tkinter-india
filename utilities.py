import geocoder
import pandas as pd

xlsx_data = {}

def get_all_data():
    """Returns the state data dictionary captured from the xlsx file"""
    return xlsx_data

def get_xlsx_data():
    """Read state_data.xlsx and populate dictionary for use in program"""
    global xlsx_data

    file = r"data\state_data.xlsx"
    df = pd.read_excel(file).fillna("NA")

    columns = ["State", "Capital", "Markers","NSEW Zone", "Tier", "Population",	
               "Development Level", "Size (in KM)",	"Climate", "Rainfall (in mm)",
               "Languages Spoken", "Food", "Tourist Places"]

    for col in columns:
        xlsx_data[col] = df[col].values.tolist()


def get_distance_bw_cities(city1, city2):
    """Provides the geocoder distance between two cities"""
    g1 = geocoder.osm((city1.strip().title() + ", India"))
    g2 = geocoder.osm((city2.strip().title() + ", India"))

    return str(int(geocoder.distance((g1.lat, g1.lng), (g2.lat, g2.lng))))


def get_state_capital_dct():
    """Returns the capital of state and state of capital dictionaries"""
    global xlsx_data
    
    states = xlsx_data["State"]
    capitals = xlsx_data["Capital"]
    markers = xlsx_data["Markers"]
    captial_of_state = {} # State: Capitals
    state_of_capital = {} # Capital: State

    for index in range(len(states)):
        captial_of_state[states[index]] = capitals[index]

        if "," in markers[index]:
            for c in list(markers[index].strip().split(",")):
                state_of_capital[c.strip()] = states[index]
    
    return captial_of_state, state_of_capital


def get_city_markers():
    """Generates a list of markers to populate on the map"""
    global xlsx_data

    markers = xlsx_data["Markers"]
    lst = []

    for city in markers:
        if "," in city:
            temp_l = [c.strip() for c in city.strip().split(",")]
            lst.extend(temp_l)
        else:
            lst.append(city)

    return lst


def get_city_data():
    """Returns dictionary used to populate information about a city"""
    global xlsx_data

    markers = xlsx_data["Markers"]
    lang = xlsx_data["Languages Spoken"]
    food = xlsx_data["Food"]
    tourism = xlsx_data["Tourist Places"]
    dct = {}

    for index, city in enumerate(markers):
        temp_l = {"Languages Spoken": lang[index], "Food": food[index], "Tourist Places": tourism[index]}

        if "," in city:
            for c in city.strip().split(","):
                dct[c.strip()] = temp_l
        else:
            dct[city] = temp_l

    return dct


def lat_lng_to_str(lat, lng):
    """Utility function to convert latitude and longitude to a unique string"""
    return str(lat) + "," + str(lng)