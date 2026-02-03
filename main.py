import requests

class ProjetProxima:
    """
    Main application class for the ProjetProxima.
    This class provides all the functions to run the application.

    Notes:
        This class relies on 'datetime' and 'requests' libraries.
    """

    def iss_tracking(self) -> dict:
        """
        Track the International Space Station with it's latitude and longitude.

            Return:
                Coordinates (list): Current ISS coordinates as [latitude, longitude].
        """

        ISS_TRACKING_URL = "http://api.open-notify.org/iss-now.json"
        iss_location = {}

        # Fetch request response
        iss_tracking_response = requests.get(ISS_TRACKING_URL)

        # Response status code verification
        if iss_tracking_response.status_code == 200:
            # Fetch the current location
            iss_tracking_data = iss_tracking_response.json()
            iss_longitude = iss_tracking_data["iss_position"]["longitude"]
            iss_latitude = iss_tracking_data["iss_position"]["latitude"]

            # Adding longitude & lattitude in a list
            iss_location["longitude"] = iss_longitude
            iss_location["latitude"] = iss_latitude

            return iss_location

        else:
            return {"Error": iss_tracking_response.status_code}

    def astronauts_tracking(self) -> dict:
        """
        Track astronauts who are currently in the space station.
            
            Return:
                astronauts_dictionary(dict): Countain all astronauts in the ISS and the number of astronauts onboard.

        """

        ASTRONAUTS_TRACKING_API_URL = "http://api.open-notify.org/astros.json"

        astronauts_tracking_response = requests.get(ASTRONAUTS_TRACKING_API_URL)

        # Dictionary for all astronauts
        astronauts_dictionary: dict[str, object] = {"astronauts": []}

        # Response status code verification
        if astronauts_tracking_response.status_code == 200:
            # Fetching all astronauts in space
            astronauts_tracking_data = astronauts_tracking_response.json()

            # Astronauts sorting
            astronauts_in_iss = [astronaut for astronaut in astronauts_tracking_data["people"] if astronaut.get("craft") == "ISS"]
            astronauts_number = str(len(astronauts_in_iss))

            for astronaut in astronauts_in_iss:
                del astronaut["craft"]

            # Stocking astronauts onboard the ISS in the dictionnary
            astronauts_dictionary["astronauts"] = astronauts_in_iss
            astronauts_dictionary["number"] = astronauts_number

            return astronauts_dictionary

        else:
            return {"Error": astronauts_tracking_response.status_code}

    def picture_of_the_day(self) -> dict:
        """Fetch the astronomy picture of the day (APOD) from the NASA Open APIs.
                Return:
                    apod_data(dict): Every useful information for the Astronomy Picture Of the Day.
                
                Informations returned: Date, explanation, media_type, 
                    title, url, hdurl (if present), copyright (if present).
            """

        APOD_API_KEY_FILE = ".env"
        PICTURE_OF_THE_DAY_URL = "https://api.nasa.gov/planetary/apod"

        # Fetching API key
        with open(APOD_API_KEY_FILE, "r") as key_file:
            APOD_API_KEY = key_file.read().split()

        # Concatenate the full API request link
        full_api_link = (f"{PICTURE_OF_THE_DAY_URL}?api_key={APOD_API_KEY[-1]}")

        apod_response = requests.get(full_api_link)

        if apod_response.status_code == 200:
            apod_data = apod_response.json()

            # Removing useless information
            del apod_data["service_version"]

            return apod_data
        else:
            return {"Error": apod_response.status_code}

if __name__ == "__main__":
    p = ProjetProxima()
    print(p.astronauts_tracking())