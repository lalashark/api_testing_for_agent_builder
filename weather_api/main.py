import functions_framework
import requests
import json

@functions_framework.http
def get_weather(request):
    """HTTP Cloud Function to get the weather for a specified location.
    
    Args:
        request (flask.Request): The request object.
    Returns:
        JSON: Weather information for the specified location.
    """
    
    # Get the location from the request
    try:
        location = request.args.get('location')
        if not location:
            return json.dumps({"error": "Location is required"}), 400
    except Exception as e:
        return json.dumps({"error": "Invalid request format"}), 400
    
    # Call the OpenWeatherMap API to get weather data based on the location
    weather_api_key = 'your_api_key'
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={weather_api_key}&units=metric"
    weather_response = requests.get(weather_url)
    weather_data = weather_response.json()
    
    # Check if the location was valid and weather data was retrieved
    if weather_response.status_code != 200:
        return json.dumps({"error": "Unable to fetch weather data for the location"}), 400
    
    # Prepare the response
    response_dict = {
        "location": f"{weather_data['name']}, {weather_data['sys']['country']}",
        "temperature": weather_data['main']['temp'],
        "weather": weather_data['weather'][0]['description']
    }
    
    # Return the response as JSON
    return json.dumps(response_dict)
