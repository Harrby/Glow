class MoodDataBase:

    def __init__(self):
        self.client = MongoClient("mongodb+srv://sam_user:9ireiEodVKBb3Owt@glowcluster.36bwm.mongodb.net/?retryWrites=true&w=majority&appName=GlowCluster")
        self.db = self.client["mood_tracker"]
        self.collection = self.db["moods"]

    def get_mood_for_date(self, year, month, day):
        date_str = f"{year}-{month:02d}-{day:02d}"
        result = self.collection.find_one({"date": date_str})
        return result["mood"] if result else None