#!/usr/bin/env python3
import os
import requests
import openai
from datetime import datetime
import subprocess
import json

with open("secrets.json", "r") as f:
    secrets = json.load(f)

API_KEY = secrets["API_KEY"]
OPENAI_API_KEY = secrets["OPENAI_API_KEY"]
GITHUB_TOKEN = secrets["GITHUB_TOKEN"]
CITY = "New York"
URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
openai.api_key = OPENAI_API_KEY
REPO_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(REPO_DIR, "results")

if not GITHUB_TOKEN or len(GITHUB_TOKEN) < 10:
    raise ValueError("GitHub token appears to be invalid or missing")

def fetch_weather_data():
    """Fetch weather data from OpenWeatherMap API."""
    response = requests.get(URL)
    if response.status_code == 200:
        data = response.json()
        return {
            "date": datetime.now().strftime('%Y-%m-%d'),
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "weather": data["weather"][0]["description"],
            "chance_of_rain": data.get("rain", {}).get("1h", 0), 
            "uv_index": data.get("uvi", 0), 
            "wind_speed": data["wind"]["speed"]
        }
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}")

def generate_recommendations(weather_data):
    """Generate recommendations using OpenAI API."""
    prompt = f"""
    Today's weather in {CITY}:
    - Temperature: {weather_data['temperature']}°C
    - Humidity: {weather_data['humidity']}%
    - Weather: {weather_data['weather']}
    - Chance of Rain: {weather_data['chance_of_rain']}%
    - UV Index: {weather_data['uv_index']}
    - Wind Speed: {weather_data['wind_speed']} m/s

    Provide personalized recommendations for the day based on the weather. Include suggestions for clothing, outdoor activities, and any precautions.
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that provides daily recommendations based on weather data."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=200
    )

    return response['choices'][0]['message']['content'].strip()

def save_recommendations(recommendations, weather_data):
    """Save recommendations to a file in the results folder."""
    if not os.path.exists(RESULTS_DIR):
        os.makedirs(RESULTS_DIR)

    filename = os.path.join(RESULTS_DIR, f"recommendations_{weather_data['date']}.txt")
    with open(filename, "w") as file:
        file.write(f"Weather Data for {weather_data['date']}:\n")
        file.write(f"- Temperature: {weather_data['temperature']}°C\n")
        file.write(f"- Humidity: {weather_data['humidity']}%\n")
        file.write(f"- Weather: {weather_data['weather']}\n")
        file.write(f"- Chance of Rain: {weather_data['chance_of_rain']}%\n")
        file.write(f"- UV Index: {weather_data['uv_index']}\n")
        file.write(f"- Wind Speed: {weather_data['wind_speed']} m/s\n\n")
        file.write("Recommendations:\n")
        file.write(recommendations)

def git_commit_and_push():
    try:
        print("Starting git operations...")
        
        # Basic git config
        subprocess.run(["git", "config", "--global", "user.name", "jayanth"], check=True)
        subprocess.run(["git", "config", "--global", "user.email", "jayanth.sattineni@gmail.com"], check=True)
        
        # Setup remote
        repo_url = f"https://{GITHUB_TOKEN}@github.com/wassupjay/smart-daily-planner.git"
        subprocess.run(["git", "remote", "remove", "origin"], check=False)
        subprocess.run(["git", "remote", "add", "origin", repo_url], check=True)
        
        # Fetch remote files
        subprocess.run(["git", "fetch", "origin"], check=True)
        
        # Get today's file name
        today = datetime.now().strftime('%Y-%m-%d')
        today_file = f"results/recommendations_{today}.txt"
        
        # Check if file exists in remote
        remote_files = subprocess.run(["git", "ls-remote", "--heads", "origin"], 
                                    capture_output=True, text=True).stdout
        
        if today_file in remote_files:
            print(f"File {today_file} already exists in remote. Skipping...")
            return
            
        subprocess.run(["git", "add", today_file], check=True)
        subprocess.run(["git", "commit", "-m", f"Add recommendations for {today}"], check=True)
        subprocess.run(["git", "push", "-u", "origin", "main"], check=True)
            
        print(f"Successfully pushed new file {today_file}")
    except subprocess.CalledProcessError as e:
        print(f"Git operation failed: {e}")
        raise

def main():
    try:
        weather_data = fetch_weather_data()
        print("Fetched weather data:", weather_data)

        recommendations = generate_recommendations(weather_data)
        print("Generated recommendations:", recommendations)

        save_recommendations(recommendations, weather_data)
        print("Recommendations saved to file.")

        git_commit_and_push()
        print("Changes pushed to GitHub.")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()