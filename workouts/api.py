import requests
import dotenv
import os
import concurrent.futures
from bs4 import BeautifulSoup


dotenv.load_dotenv()

exercise_types = ["cardio", "olympic_weightlifting", "plyometrics", "powerlifting", "strength", "stretching", "strongman"]

exercise_muscles = ["abdominals", "abductors", "adductors", "biceps", "calves", "chest", "forearms", "glutes", "hamstrings", \
            "lats", "lower_back", "middle_back", "neck", "quadriceps", "traps", "triceps"]

exercise_difficulties = ["beginner", "intermediate", "expert"]


"""
Gets a list exercises by specifying a specific muscle, type, and difficulty
Arguments: muscle, type, difficulty, images, pages, offset
- pages is how many multiples of 10 results to get
- images is boolean whether to get images
"""
def get_exercises(name=None, muscle=None, e_type=None, difficulty=None, images=False, pages=1, offset=0):
    params = {
        "name": name,
        "muscle": muscle,
        "type": e_type,
        "difficulty": difficulty,
        "offset": 0
    }
    
    threads = []
    # get multiple pages at once using threading
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for page in range(pages):
            # offset is number of pages * 10 + offset amount
            current_params = params.copy()
            current_params['offset'] = (page * 10) + offset
            threads.append(executor.submit(request_exercise, current_params, images))
    results = [t.result() for t in threads]

    exercises = []
    for result in results:
        if result:
            exercises.extend(result)
    #print(exercises)
    return exercises

    
"""
Use the google search api to get google images search results
query: query to search
"""
def image_search(query):
    url = f"https://www.bing.com/images/search?q={query}"
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    # get all image tags
    links = soup.find_all('img')
    max_width = 0
    largest = None
    # loop through all images to find one with the highest resolution
    for link in links:
        if link.get('width'):
            width = int(link.get('width'))
            if width > max_width:
                if link.get('src'):
                    max_width = width
                    largest = link.get('src')
    return largest

def fetch_exercise_image(query):
    try:
        images = image_search(query + " exercise stock graphic")
        if images:
            return images
    except Exception as e:
        print(f"Error in fetch_exercise_image: {e}")
        return None
    

"""
Sends a request to the exercises api given the parameters
Fetches images if images = True
"""
def request_exercise(params, images):
    try:
        url = "https://api.api-ninjas.com/v1/exercises"
        headers = {'X-Api-Key': os.getenv("EXERCISE_API_KEY") }
        req = requests.get(url, params=params, headers=headers)
        if req.status_code == 200:
            exercises = req.json()
            if len(exercises) == 0:
                return None

            if images:
                # send google api requests in threads
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    threads = [executor.submit(fetch_exercise_image, exercise['name']) for exercise in exercises]
                images = [t.result() for t in threads]

                # add images to exercise request
                for i, image in enumerate(images):
                    exercises[i]['image'] = image 
            
            return exercises
        else:
            print("request_exercise api Error", req.status_code)
            return None
    except Exception as e:
        print(f"Error in request_exercise: {e}")
        return None


"""
Use the youtube api to search for youtube videos
query: query to search
"""
def fetch_youtube_link(query):
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        'key': os.getenv('GCS_DEVELOPER_KEY'),
        'part': "snippet",
        'q': query,
        'type': 'video',
        'videoDuration': 'short'
    }
    headers = {'Accept': 'application/json'}
    req = requests.get(url, params=params, headers=headers)
    if req.status_code == 200:
        result = req.json()['items'][0]
        youtube = {
            'title': result['snippet']['title'],
            'id': result['id']['videoId'],
            'thumbnail': result['snippet']['thumbnails']['high']['url']
        }
        return youtube
    else:
        print(req.json())
        print("fetch_youtube_link api Error", req.status_code)
        return None


if __name__ == '__main__':
    print(fetch_youtube_link("test"))