import requests

class Requests:

    def __init__(self, worldId=0):
        self.base_url = "https://www.notexponential.com/aip2pgaming/api/rl/"
        self.team_id = "1438"
        self.user_id = "3609"
        self.api_key = '4eb91eeb4e1eaf04f2d3'
        self.worldId = worldId
        self.USER_AGENT = '\'User-Agent\': \'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36\''


    def _request(self, method, endpoint, payload=None):
        url = self.base_url + endpoint
        headers = {
            'userId': self.user_id,
            'x-api-key': self.api_key,
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': self.USER_AGENT
        }
        response = requests.request(method, url, headers=headers, data=payload)
        jsonResponse = response.json()
        return jsonResponse

    def enter_world(self, worldId=None):
        payload = {'type': 'enter', 'worldId': self.worldId, 'teamId': self.team_id}
        response = self._request("POST", "gw.php", payload)
        if response["code"] == "FAIL":
            print(response)
            return -1
        elif response["code"] == "OK":
            print(response)
            return 0
        else:
            print('Error in enter_world()')   
            return -1

    def make_move(self, move='N', worldId=None):
        payload = {'type': 'move', 'teamId': self.team_id, 'move': move, 'worldId': self.worldId}
        response = self._request("POST", "gw.php", payload)
        return response
   
    def get_location(self):
        response = self._request("GET", f"gw.php?type=location&teamId={self.team_id}")
        if response["code"] == "FAIL":
            print("Error")
            return -1
        elif response["code"] == "OK":
            world = response["world"]
            state = response["state"]
            return world, state
        else:
            print('Error in get_location()')   
            return -1
    
    def get_learning_score(self):
        response = self._request("GET", f"score.php?type=score&teamId={self.team_id}")
        if response["code"] == "FAIL":
            print(response)
            return -1
        elif response["code"] == "OK":
            score = response["score"]
            return score
        else:
            print('Error')   
            return -1

    def get_last_x_runs(self, count=10):
        response = self._request("GET", f"score.php?type=runs&teamId={self.team_id}&count={count}")
        if response["code"] == "FAIL":
            print(response)
        elif response["code"] == "OK":
            runs = response["runs"]
            return runs 
        else:
            print('Error')   

    def reset_agent(self):
        response = self._request("GET", f"reset.php?teamId={self.team_id}&otp=5712768807")
        print(response.text)
        if response["code"] == "FAIL":
            print(response)
            return -1
        elif response["code"] == "OK":
            runs = response
            return 0
        else:
            print('Error')   
            return -1
