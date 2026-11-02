import requests

LEETCODE_GRAPHQL_URL = "https://leetcode.com/graphql"

def fetch_leetcode_profile(username):
    query = """
    query getUserProfile($username: String!) {
      matchedUser(username: $username) {
        username
        submitStatsGlobal {
          acSubmissionNum {
            difficulty
            count
          }
        }
        profile {
          ranking
        }
      }
    }
    """
    variables = {"username": username}
    try:
        response = requests.post(
            LEETCODE_GRAPHQL_URL,
            json={"query": query, "variables": variables},
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            user_data = data.get("data", {}).get("matchedUser")
            if not user_data:
                return None
            
            stats = user_data["submitStatsGlobal"]["acSubmissionNum"]
            solved = {item["difficulty"]: item["count"] for item in stats}
            
            return {
                "username": username,
                "all": solved.get("All", 0),
                "easy": solved.get("Easy", 0),
                "medium": solved.get("Medium", 0),
                "hard": solved.get("Hard", 0),
                "ranking": user_data["profile"].get("ranking", "N/A")
            }
        return None
    except Exception as e:
        print(f"Error fetching {username}: {e}")
        return None