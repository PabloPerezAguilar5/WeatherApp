from flask import Flask, render_template, request
from weather import main as get_weather, get_random_city

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    data = None
    random_city_data = None
    random_city_name = None
    random_country_name = None
    error = None

    # Obtener una ciudad aleatoria
    random_city_name, random_country_name = get_random_city()
    try:
        random_city_data = get_weather(random_city_name, random_country_name)
    except Exception as e:
        error = f"An error occurred while getting random city weather: {e}"

    if request.method == 'POST':
        city = request.form.get('cityName')
        country = request.form.get('countryName')

        if not city or not country:
            error = "Please enter both city and country names."
        else:
            try:
                data = get_weather(city, country)
                if data is None:
                    error = "Location not found. Please try again."
            except Exception as e:
                error = f"An error occurred: {e}"

    return render_template('index.html', data=data, error=error, 
                           random_city_data=random_city_data, 
                           random_city_name=random_city_name, 
                           random_country_name=random_country_name)

if __name__ == '__main__':
    app.run(debug=True)
