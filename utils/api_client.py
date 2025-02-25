import requests
from config.settings import SOURCE_API_BASE_URL, DESTINATION_API_BASE_URL, SOURCE_API_KEY, DESTINATION_API_KEY

class APIClient:
    def __init__(self, instance="source"):
        if instance == "source":
            self.base_url = SOURCE_API_BASE_URL
            self.session_key = SOURCE_API_KEY
        elif instance == "destination":
            self.base_url = DESTINATION_API_BASE_URL
            self.session_key = DESTINATION_API_KEY
        else:
            raise ValueError("Invalid instance type. Use 'source' or 'destination'.")

        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {self.session_key}"})

    def get(self, endpoint):
        response = self.session.get(f"{self.base_url}{endpoint}")
        response.raise_for_status()
        return response.json()

    def post(self, endpoint, data):
        try:
            response = self.session.post(f"{self.base_url}{endpoint}", json=data)
            response.raise_for_status()  # ✅ This ensures HTTP errors are caught in the except block
            return response.json()  # ✅ If successful, return JSON response

        except requests.exceptions.HTTPError as e:
            print("❌ HTTP Error occurred!")

            # Extract detailed error message from response
            error_message = ""
            if e.response is not None:
                try:
                    error_json = e.response.json()  # Try to parse JSON error message
                    error_message = error_json if isinstance(error_json, dict) else str(error_json)
                except ValueError:
                    error_message = e.response.text  # If not JSON, return raw text
            else:
                error_message = str(e)

            print(f"❌ HTTP Error: {error_message}")
            return None  # Return None to indicate failure

        except requests.exceptions.RequestException as e:
            print(f"❌ Request Exception: {str(e)}")
            return None  # Return None to indicate failure


    def put(self, endpoint, data):
        response = self.session.put(f"{self.base_url}{endpoint}", json=data)
        response.raise_for_status()
        return response.json()

    def delete(self, endpoint):
        response = self.session.delete(f"{self.base_url}{endpoint}")
        response.raise_for_status()
        return response.json()
