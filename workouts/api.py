import requests
#import dotenv
import os

#dotenv.load_dotenv()



def get_exercises(muscle, e_type, difficulty, offset=0):
    url = f"https://api.api-ninjas.com/v1/exercises"
    params = {
        "muscle": muscle,
        "type": e_type,
        "difficulty": difficulty,
        "offset": offset
    }
    headers = {'X-Api-Key': "dH6cEBILcZsil7497iM5/g==R4o7bqPizPy6G2CP" }
    req = requests.get(url, headers=headers, params=params)
    if req.status_code == 200:
        exercises = req.json()
        # for i, exercise in enumerate(exercises):
        #     image = google_image_search(exercise['name'] + " exercise stock graphic")
        #     exercises[i]['image'] = image
        return exercises
    else:
        print("Error", req.status_code, req.text)
        return None


"""
Possible types:
- cardio
- olympic_weightlifting
- plyometrics
- powerlifting
- strength
- stretching
- strongman

Parameters: type and offset. Returns 10 results. Offset default 0
"""
def exercise_by_type(e_type, offset=0):
    url = f"https://api.api-ninjas.com/v1/exercises?type={e_type}&offset={offset}"
    headers = {'X-Api-Key': os.getenv("dH6cEBILcZsil7497iM5/g==R4o7bqPizPy6G2CP") }
    req = requests.get(url, headers=headers)
    if req.status_code == 200:
        exercises = req.json()
        for i, exercise in enumerate(exercises):
            image = google_image_search(exercise['name'] + " exercise stock graphic")[0]
            exercises[i]['image'] = image
        return exercises
    else:
        print("Error", req.status_code, req.text)
        return None
    
def get_exercise_types():
    return ["cardio", "olympic_weightlifting", "plyometrics", "powerlifting", "strength", "stretching", "strongman"]
    
"""
Possible muscles:
- abdominals
- abductors
- adductors
- biceps
- calves
- chest
- forearms
- glutes
- hamstrings
- lats
- lower_back
- middle_back
- neck
- quadriceps
- traps
- triceps

Parameters: muscle and offset. Returns 10 results. Offset default 0
"""
def exercise_by_muscle(muscle, offset=0):
    url = f"https://api.api-ninjas.com/v1/exercises?muscle={muscle}&offset={offset}"
    headers = {'X-Api-Key': os.getenv("EXERCISE_API_KEY") }
    req = requests.get(url, headers=headers)
    if req.status_code == 200:
        exercises = req.json()
        for i, exercise in enumerate(exercises):
            image = google_image_search(exercise['name'] + " exercise stock graphic")[0]
            exercises[i]['image'] = image
        return exercises
    else:
        print("exercise_by_muscle Error", req.status_code)
        return None
    

def get_exercise_muscles():
    return ["abdominals", "abductors", "adductors", "biceps", "calves", "chest", "forearms", "glutes", "hamstrings", \
            "lats", "lower_back", "middle_back", "neck", "quadriceps", "traps", "triceps"]


"""
Possible difficulties:
- beginner
- intermediate
- expert

Parameters: difficulty and offset. Returns 10 results. Offset default 0
"""
def exercise_by_difficulty(difficulty, offset=0):
    url = f"https://api.api-ninjas.com/v1/exercises?difficulty={difficulty}&offset={offset}"
    headers = {'X-Api-Key': os.getenv("EXERCISE_API_KEY") }
    req = requests.get(url, headers=headers)
    if req.status_code == 200:
        exercises = req.json()
        for i, exercise in enumerate(exercises):
            image = google_image_search(exercise['name'] + " exercise stock graphic")[0]
            exercises[i]['image'] = image
        return exercises
    else:
        print("exercise_by_difficulty Error", req.status_code)
        return None
    
def get_exercise_difficulties():
    return ["beginner", "intermediate", "expert"]
    

def google_image_search(query):
    GCS_DEVELOPER_KEY = os.getenv('GCS_DEVELOPER_KEY')
    GCS_CX = os.getenv('GCS_CX')
    url = f"https://customsearch.googleapis.com/customsearch/v1?key={GCS_DEVELOPER_KEY}&cx={GCS_CX}&q={query}&searchType=image"
    headers = {'Accept': 'application/json'}
    req = requests.get(url, headers=headers)
    if req.status_code == 200:
        images = []
        for item in req.json()['items']:
            images.append(item['link'])
        return images
    else:
        print("google_image_search Error", req.status_code)
        return None


if __name__ == '__main__':
    print(exercise_by_muscle("biceps"))