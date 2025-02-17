# Smart Daily Planner

A Python-based daily planner that provides personalized recommendations based on weather conditions and generates daily activity suggestions.


## Features

🌤️ Real-time weather data integration using OpenWeatherMap API
📝 Daily activity recommendations based on weather conditions
📊 Automatic saving of daily recommendations
🔄 Automatic GitHub synchronization of results
📅 Date-based file organization

## Setup

1. Clone the repository:

```bash
git clone https://github.com/wassupjay/smart-daily-planner.git
cd smart-daily-planner
```
 
2. Create a `secrets.json` file in the root directory with your API keys:

```json
{
    "OPENWEATHERMAP_API_KEY": "your_weather_api_key",
    "GITHUB_TOKEN": "your_github_token"
} 
```

3. Install required dependencies:

```bash
pip install requests
```

4. Run the script:

```bash
python daily_planner.py             
```

## Usage

The script will generate a daily recommendation based on the weather conditions and save it to the `results` directory.

## Contributing

1. Fork the repository
2. Create a new branch
3. Make your changes and commit them
4. Push to your fork
5. Create a pull request   

## License

This project is licensed under the MIT License. 