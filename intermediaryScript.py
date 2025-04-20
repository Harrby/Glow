
import httpx

BASE_URL = "http://16.170.211.11:8000"

class intermediaryScript():
##WORKS
    def getUserID(self, username: str):
        url = f"{BASE_URL}/moods/userID/getUserID/{username}"
        try:
            response = httpx.get(url)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP error: {e.response.status_code}, {e.response.text}")
        except Exception as e:
            print(f"Error: {str(e)}")

##WORKS
    def getUsername(self, user_id: str):
        url = f"{BASE_URL}/moods/username/getUsername/{user_id}"
        try:
            response = httpx.get(url)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP error: {e.response.status_code}, {e.response.text}")
        except Exception as e:
            print(f"Error: {str(e)}")

##NEEDS TO BE FIXED
    def insertMood(self, username: str, body: __dict__):
        url = f"{BASE_URL}/moods/{username}/insert"
        try:
            response = httpx.post(url)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP error: {e.response.status_code}, {e.response.text}")
        except Exception as e:
            print(f"Error: {str(e)}")

##WORKS
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

##CHECK ME
    def addCustomActivity(self, username: str):
        url = f"{BASE_URL}/accounts/{username}/addActivity"
        try:
            response = httpx.post(url)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP error: {e.response.status_code}, {e.response.text}")
        except Exception as e:
            print(f"Error: {str(e)}")

##CHECK ME
    def updateMood(self, username: str):
        url = f"{BASE_URL}/moods/{username}/update"
        try:
            response = httpx.put(url)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP error: {e.response.status_code}, {e.response.text}")
        except Exception as e:
            print(f"Error: {str(e)}")

##CHECK ME
    def deleteAllMoods(self, username: str):
        url = f"{BASE_URL}/moods/{username}/delete"
        try:
            response = httpx.delete(url)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP error: {e.response.status_code}, {e.response.text}")
        except Exception as e:
            print(f"Error: {str(e)}")

##WORKS
    def deleteUser(self, username: str):
        url = f"{BASE_URL}/accounts/{username}/delete"
        try:
            response = httpx.delete(url)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP error: {e.response.status_code}, {e.response.text}")
        except Exception as e:
            print(f"Error: {str(e)}")

##CHECK ME
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

##FAILS
    def nhsSearch(self):
        url = f"{BASE_URL}/nhs-search"
        try:
            response = httpx.get(url)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP error: {e.response.status_code}, {e.response.text}")
        except Exception as e:
            print(f"Error: {str(e)}")

##BASIC WORKS  - BUT TEST END DATE
    def getFactorForLastXDays(self, username: str, factor: str, days: int):
        url = f"{BASE_URL}/moods/lastXDays/{username}/{factor}/{days}"
        try:
            response = httpx.get(url)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP error: {e.response.status_code}, {e.response.text}")
        except Exception as e:
            print(f"Error: {str(e)}")
##WORKS
    def getAverageFactorForLastXDays(self, username: str, factor: str, days: int):
        url = f"{BASE_URL}/moods/average/{username}/{factor}/{days}"
        try:
            response = httpx.get(url)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP error: {e.response.status_code}, {e.response.text}")
        except Exception as e:
            print(f"Error: {str(e)}")

##WORKS
    def getTopFactorForLastXDays(self, username: str, days: int):
        url = f"{BASE_URL}/moods/mostPopularMood/{username}/{days}"
        try:
            response = httpx.get(url)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP error: {e.response.status_code}, {e.response.text}")
        except Exception as e:
            print(f"Error: {str(e)}")

##CHECK ME
    def getAccount(self, username: str):
        url = f"{BASE_URL}/account/{username}"
        try:
            response = httpx.get(url)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP error: {e.response.status_code}, {e.response.text}")
        except Exception as e:
            print(f"Error: {str(e)}")

##CHECK ME
    def getMoodEntry(self, username: str, date: str):
        url = f"{BASE_URL}/moods/{username}/getMoodEntry/{date}"
        try:
            response = httpx.get(url)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP error: {e.response.status_code}, {e.response.text}")
        except Exception as e:
            print(f"Error: {str(e)}")

##CHECK ME - BODY
    def addExerciseEntry(self, username: str, body: __dict__):
        url = f"{BASE_URL}/exercise/{username}/insert"
        try:
            response = httpx.post(url)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP error: {e.response.status_code}, {e.response.text}")
        except Exception as e:
            print(f"Error: {str(e)}")

##CHECK ME - BODY
    def tryLogin(self, body: __dict__):
        url = f"{BASE_URL}/accounts/login"
        try:
            response = httpx.post(url)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP error: {e.response.status_code}, {e.response.text}")
        except Exception as e:
            print(f"Error: {str(e)}")

##CHECK ME - BODY
    def trySignup(self, body: __dict__):
        url = f"{BASE_URL}/accounts/signup"
        try:
            response = httpx.post(url)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP error: {e.response.status_code}, {e.response.text}")
        except Exception as e:
            print(f"Error: {str(e)}")

##CHECK ME - BODY
    def addCustomHobby(self, username: str, body: __dict__):
        url = f"{BASE_URL}/accounts/{username}/addHobby"
        try:
            response = httpx.post(url)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP error: {e.response.status_code}, {e.response.text}")
        except Exception as e:
            print(f"Error: {str(e)}")

##CHECK ME
    def updateProfile(self, username: str):
        url = f"{BASE_URL}/accounts/{username}/update"
        try:
            response = httpx.put(url)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP error: {e.response.status_code}, {e.response.text}")
        except Exception as e:
            print(f"Error: {str(e)}")

#testywesty = intermediaryScript()
#output = testywesty.hasLoggedIn("sammy", "01-01-2025")
#print(output)

##VALIDATE DATE FUNCTION HAS LOGGED IN!!
##VALIDATE MOOD FORMAT INSTER MOOD
##LOOK INTO BODY THING