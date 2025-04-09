
import httpx

BASE_URL = "http://16.170.211.11:8000"

class intermediaryScript():
    def getUserID(self, user_id: str):
        url = f"{BASE_URL}/moods/userID/getUserID/{user_id}"
        try:
            response = httpx.get(url)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP error: {e.response.status_code}, {e.response.text}")
        except Exception as e:
            print(f"Error: {str(e)}")

    def getUsername(self, username: str):
        url = f"{BASE_URL}/moods/username/getUsername/{username}"
        try:
            response = httpx.get(url)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP error: {e.response.status_code}, {e.response.text}")
        except Exception as e:
            print(f"Error: {str(e)}")

    ##DO I NEED TO RETURN ANYTHING?
    def insertMood(self, username: str):
        url = f"{BASE_URL}/moods/{username}/insert"
        try:
            response = httpx.get(url)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP error: {e.response.status_code}, {e.response.text}")
        except Exception as e:
            print(f"Error: {str(e)}")

    def getRandomActivity(self, username: str):
        url = f"{BASE_URL}/moods/{username}/random_activity"
        try:
            response = httpx.get(url)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP error: {e.response.status_code}, {e.response.text}")
        except Exception as e:
            print(f"Error: {str(e)}")

    ##DO I NEED TO RETURN ANYTHING?
    def addCustomActivity(self, username: str):
        url = f"{BASE_URL}/accounts/{username}/addActivity"
        try:
            response = httpx.get(url)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP error: {e.response.status_code}, {e.response.text}")
        except Exception as e:
            print(f"Error: {str(e)}")

    def getMonthlyFactorList(self, username: str, month: int, year: int, factor: str):
        url = f"{BASE_URL}/moods/monthly/{username}/{month}/{year}/{factor}"
        try:
            response = httpx.get(url)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP error: {e.response.status_code}, {e.response.text}")
        except Exception as e:
            print(f"Error: {str(e)}")

    ##DO I NEED TO RETURN ANYTHING?
    def updateMood(self, username: str):
        url = f"{BASE_URL}/moods/{username}/update"
        try:
            response = httpx.get(url)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP error: {e.response.status_code}, {e.response.text}")
        except Exception as e:
            print(f"Error: {str(e)}")

    ##DO I NEED TO RETURN ANYTHING?
    def deleteAllMoods(self, username: str):
        url = f"{BASE_URL}/moods/{username}/delete"
        try:
            response = httpx.get(url)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP error: {e.response.status_code}, {e.response.text}")
        except Exception as e:
            print(f"Error: {str(e)}")

    ##DO I NEED TO RETURN ANYTHING?
    def deleteUser(self, username: str):
        url = f"{BASE_URL}/accounts/{username}/delete"
        try:
            response = httpx.get(url)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP error: {e.response.status_code}, {e.response.text}")
        except Exception as e:
            print(f"Error: {str(e)}")

    def hasLoggedIn(self, username: str, date: str):
        url = f"{BASE_URL}/moods/{username}/hasLoggedIn/{date}"
        try:
            response = httpx.get(url)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP error: {e.response.status_code}, {e.response.text}")
        except Exception as e:
            print(f"Error: {str(e)}")

#testywesty = intermediaryScript()
#output = testywesty.getMonthlyFactorList("Kenya Park")
#print(output)
       