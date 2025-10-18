from time import sleep
import requests

class ProximaProject:
    """
    Main application class for the ProximaProject.
    This class provides all the functions to run the application. 

    Notes:
        This class relies on 'time' and 'requests' libraries.
    """

    def iss_tracking(self):
        """
        Track the International Space Station with it's latitude and longitude.

            Return:
                    Coordinates (list): Current ISS coordinates as [latitude, longitude].
        
        """

        ISS_TRACKING_URL = "http://api.open-notify.org/iss-now.json"
        self.iss_location = []

        # Fetch request response
        iss_tracking_response = requests.get(ISS_TRACKING_URL)
        
        # Response status code verification
        if iss_tracking_response.status_code == 200:
            # Fetch the current location
            iss_tracking_data = iss_tracking_response.json()
            iss_longitude = iss_tracking_data["iss_position"]["longitude"]
            iss_latitude = iss_tracking_data["iss_position"]["latitude"]

            # Adding longitude & lattitude in a list
            self.iss_location.append(iss_longitude)
            self.iss_location.append(iss_latitude)

            return self.iss_location

        else:
            print(f"Error {iss_tracking_response.status_code}")

    def astronauts_tracking(self):
        """
        Track astronauts who are currently in the space station.
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
            print(f"Error {astronauts_tracking_response.status_code}")

if __name__ == "__main__":
    p = ProximaProject()
    p.astronauts_tracking()