alert("JavaScript khdam!");
console.log("JavaScript is working!");
const form = document.getElementById("weather-form");
const cityInput = document.getElementById("question");

const message = document.getElementById("message");
const weatherResult = document.getElementById("weather-result");

const cityName = document.getElementById("city-name");
const temperature = document.getElementById("temperature");
const humidity = document.getElementById("humidity");
const wind = document.getElementById("wind");

form.addEventListener("submit", async function (event) {
    event.preventDefault();

    const city = cityInput.value.trim();

    if (!city) {
        message.textContent = "Veuillez entrer une ville.";
        return;
    }

    message.textContent = "Recherche de la météo...";
    weatherResult.hidden = true;

    try {
        const url = `/weather/city?city=${encodeURIComponent(city)}`;

        const response = await fetch(url);
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Erreur lors de la recherche.");
        }

        cityName.textContent = city;
        temperature.textContent = data.temperature;
        humidity.textContent = data.humidity;
        wind.textContent = data.wind_speed;

        weatherResult.hidden = false;
        message.textContent = "Météo récupérée avec succès !";

    } catch (error) {
        message.textContent = error.message;
    }
});

form.addEventListener("reset", function () {
    weatherResult.hidden = true;
    message.textContent = "";
});
