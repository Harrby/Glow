
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

##WORKS
    def insertMood(self, username: str, body: dict):
        url = f"{BASE_URL}/moods/{username}/insert"
        try:
            response = httpx.post(url, json=body)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP error: {e.response.status_code}, {e.response.text}")
        except Exception as e:
            print(f"Error: {str(e)}")

##WORKS
    def getRandomExercise(self, username: str):
        url = f"{BASE_URL}/accounts/{username}/getRandomExercise"
        try:
            response = httpx.get(url)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP error: {e.response.status_code}, {e.response.text}")
        except Exception as e:
            print(f"Error: {str(e)}")

##WORKS
    def addCustomExercise(self, username: str, exercise: str):
        url = f"{BASE_URL}/accounts/{username}/addExercise"
        try:
            response = httpx.post(url, params={"exercise": exercise})
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP error: {e.response.status_code}, {e.response.text}")
        except Exception as e:
            print(f"Error: {str(e)}")

##WORKS
    def updateFactor(self, username: str, date: str, body: dict):
        url = f"{BASE_URL}/moods/{username}/updateFactor"
        try:
            response = httpx.put(url, params={"date": date}, json=body)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP error: {e.response.status_code}, {e.response.text}")
        except Exception as e:
            print(f"Error: {str(e)}")

##WORKS
    def deleteAllMoods(self, username: str):
        url = f"{BASE_URL}/moods/{username}/deleteAll"
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

##WORKS
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

##WORKS    
    def nhsSearch(self, keywords: str):
        url = f"{BASE_URL}/nhs-search"
        try:
            response = httpx.get(url, params={"keywords": keywords})
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP error: {e.response.status_code}, {e.response.text}")
        except Exception as e:
            print(f"Error: {str(e)}")

##WORKS
    def getFactorForLastXDays(self, username: str, factor: str, days: int, end_day: str | None ):
        url = f"{BASE_URL}/moods/lastXDays/{username}/{factor}/{days}"
        try:
            response = httpx.get(url, params={"end_day": end_day})
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP error: {e.response.status_code}, {e.response.text}")
        except Exception as e:
            print(f"Error: {str(e)}")

##WORKS
    def getAverageFactorForLastXDays(self, username: str, factor: str, days: int, end_day: str | None ):
        url = f"{BASE_URL}/moods/average/{username}/{factor}/{days}"
        try:
            response = httpx.get(url, params={"end_day": end_day})
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP error: {e.response.status_code}, {e.response.text}")
        except Exception as e:
            print(f"Error: {str(e)}")

##WORKS
    def getTopFactorForLastXDays(self, username: str, days: int, end_day: str | None ):
        url = f"{BASE_URL}/moods/mostPopularMood/{username}/{days}"
        try:
            response = httpx.get(url, params={"end_day": end_day})
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP error: {e.response.status_code}, {e.response.text}")
        except Exception as e:
            print(f"Error: {str(e)}")

##WORKS
    def getAccount(self, username: str, detail: str | None ):
        url = f"{BASE_URL}/account/{username}"
        try:
            response = httpx.get(url, params={"detail": detail})
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP error: {e.response.status_code}, {e.response.text}")
        except Exception as e:
            print(f"Error: {str(e)}")

##WORKS
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

##WORKS
    def getMoodEntryByYear(self, username: str, year: str):
        url = f"{BASE_URL}/moods/{username}/getMoodEntryByYear/{year}"
        try:
            response = httpx.get(url)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP error: {e.response.status_code}, {e.response.text}")
        except Exception as e:
            print(f"Error: {str(e)}")

##WORKS
    def addExerciseEntry(self, username: str, body: dict):
        url = f"{BASE_URL}/exercise/{username}/insert"
        try:
            response = httpx.post(url, json=body)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP error: {e.response.status_code}, {e.response.text}")
        except Exception as e:
            print(f"Error: {str(e)}")

##WORKS
    def tryLogin(self, body: dict):
        url = f"{BASE_URL}/accounts/login"
        try:
            response = httpx.post(url, json=body)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP error: {e.response.status_code}, {e.response.text}")
        except Exception as e:
            print(f"Error: {str(e)}")

##WORKS
    def trySignup(self, body: dict):
        url = f"{BASE_URL}/accounts/signup"
        try:
            response = httpx.post(url, json=body)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP error: {e.response.status_code}, {e.response.text}")
        except Exception as e:
            print(f"Error: {str(e)}")

##WORKS
    def addCustomHobby(self, username: str, hobby: str):
        url = f"{BASE_URL}/accounts/{username}/addHobby"
        try:
            response = httpx.post(url, params={"hobby": hobby})
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP error: {e.response.status_code}, {e.response.text}")
        except Exception as e:
            print(f"Error: {str(e)}")

##WORKS
    def updateProfile(self, username: str, body: dict):
        url = f"{BASE_URL}/accounts/{username}/update"
        try:
            response = httpx.put(url, json=body)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP error: {e.response.status_code}, {e.response.text}")
        except Exception as e:
            print(f"Error: {str(e)}")


#keyworder = "sick"
#hobby = "starving"
#exercise = "hanging"
#body = {
#    "factor": "alcohol",
#    "value": 2
#  "mood": "stressed",
#  "sleep": 2,
#  "screen": 12,
#  "exercise": 0,
#  "alcohol": 14,
#  "date": "03-01-2025",
#  "diary": "noooooooooo"
#}


#testywesty = intermediaryScript()
#output = testywesty.getUserID("TestDummy01")
#print(output)

##VALIDATE DATE FUNCTION HAS LOGGED IN!!
##VALIDATE MOOD FORMAT INSTER MOOD
##LOOK INTO BODY THING