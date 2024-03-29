import requests
import json


session = requests.Session()

def ensure_trailing_slash(url):
    """Ensure the URL ends with a slash."""
    return url if url.endswith('/') else url + '/'

def login(url):
    username = input("Enter username: ")
    password = input("Enter password: ")
    data = {"username": username, "password": password}
    response = session.post(f"{ensure_trailing_slash(url)}api/login", data=data)
    print(response.text)

def logout(url):
    csrf_token = session.cookies.get('csrftoken')

    if csrf_token is None:
        print("CSRF token not found. Are you logged in?")
        return

    headers = {
        'X-CSRFToken': csrf_token,
        'Referer': url,
    }

    response = session.post(f"{ensure_trailing_slash(url)}api/logout", headers=headers)
    
    if response.status_code == 200:
        print("Successfully logged out.")
    elif response.status_code == 400:
        print("You were never logged in.")
    else:
        print("Logout failed: ", response.text)

def post(url):
    headline = input("Enter headline: ")
    category = input("Enter category (pol, art, tech, trivia): ")
    region = input("Enter region (uk, eu, w): ")
    details = input("Enter details: ")
    data = {"headline": headline, "category": category, "region": region, "details": details}

    csrf_token = get_csrf_token(url)
    headers = {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrf_token,
    }

    response = session.post(f"{ensure_trailing_slash(url)}api/stories/", data=json.dumps(data), headers=headers)
    print(response.text)

def get_stories(url, id=None, cat=None, reg=None, date=None):
    params = {}
    if id:
        params["id"] = id
    if cat is not None:
        params["story_cat"] = cat if cat else "*"
    else:
        params["story_cat"] = "*"
    if reg is not None:
        params["story_region"] = reg if reg else "*"
    else:
        params["story_region"] = "*"
    if date:
        params["story_date"] = date
    else:
        params["story_date"] = ""  

    response = requests.get(f"{ensure_trailing_slash(url)}api/stories", params=params)

    if response.status_code == 200:
        stories = response.json()
        for story in stories:
            print(f"Key: {story['id']}")
            print(f"Headline: {story['headline']}")
            print(f"Category: {story['category']}")
            print(f"Region: {story['region']}")
            print(f"Author: {story['author']}")
            print(f"Date: {story['date']}")
            print(f"Details: {story['details']}")
            print("---")
    else:
        print(response.text)

def list_agencies():
    directory_url = "https://newssites.pythonanywhere.com/api/directory/"
    response = requests.get(directory_url)
    if response.status_code == 200:
        agencies = response.json()  
        for agency in agencies:  
            print(f"Name: {agency['agency_name']}\nURL: {agency['url']}\nCode: {agency['agency_code']}\n")
    else:
        print("Failed to fetch the list of agencies:", response.text)


def delete_story(url, story_key):
    csrf_token = get_csrf_token(url)
    headers = {
        'X-CSRFToken': csrf_token,
    }

    response = session.delete(f"{ensure_trailing_slash(url)}api/stories/{story_key}", headers=headers)
    print(response.text)

def get_csrf_token(url):
    response = session.get(url)
    csrf_token = session.cookies.get('csrftoken')
    return csrf_token

# The rest of your functions modified to use `session` instead of `requests` directly

def main():
    url = input("Enter the URL of the news agency: ")
    url = ensure_trailing_slash(url)  # Ensure the URL is correctly formatted
    while True:
        action = input("Enter action (login, logout, post, news, list, delete): ")
        if action == "login":
            login(url)
            get_csrf_token(url)
        elif action == "logout":
            logout(url)
        elif action == "post":
            post(url)
        elif action == "news":
            id = input("Enter agency ID (or leave blank for all): ") or None
            cat = input("Enter category (or leave blank for all): ") or None
            reg = input("Enter region (or leave blank for all): ") or None
            date = input("Enter date (or leave blank for all): ") or None
            get_stories(url, id, cat, reg, date)
        elif action == "list":
            list_agencies()
def main():
    url = input("Enter the URL of the news agency: ")
    url = ensure_trailing_slash(url)

    while True:
        action = input("Enter action (login, logout, post, news, list, delete): ")
        if action == "login":
            login(url)
            get_csrf_token(url)
        elif action == "logout":
            logout(url)
        elif action == "post":
            post(url)
        elif action == "news":
            id = input("Enter agency ID (or leave blank for all): ") or None
            cat = input("Enter category (or leave blank for all): ") or None
            reg = input("Enter region (or leave blank for all): ") or None
            date = input("Enter date (or leave blank for all): ") or None
            get_stories(url, id, cat, reg, date)
        elif action == "list":
            list_agencies() 
        elif action == "delete":
            story_key = input("Enter story key: ")
            delete_story(url, story_key)
        else:
            print("Invalid action")

if __name__ == "__main__":
    main()
