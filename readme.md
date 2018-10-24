Beeline
--------
final Hackbright project

**Description**

Beeline is a itinerary-building app that helps vacationers find the optimal driving route for up to 5 destinations, including the origin. "Optimal" is defined as always choosing the nearest stop in relation to user's current location.

![demo_gif](/static/img/demo.gif)

### Table of Contents
- [Features](#features)
- [Technology Stack](#tech-stack)
- [Testing Coverage](#testing)
- [How To Run Locally](#run-local)
- [Current Optimization](#optimization)

## <a name='features'></a>Features

- Location Submission (up to 5 incl. origin)
- Autocomplete Location Submissions
- Greedy algorithm: always choose next closest location 


## <a name="tech-stack"></a>Technology Stack

**Application:** Python, Flask, Jinja

**Front-End:** JavaScript, HTML/CSS, Bootstrap,   

**APIs:** Google Maps Distance Matrix API, Google Places API Web Service, Google Maps Directions API, Google Maps Geocoding API, Google Maps Javascript API


## <a name='testing'></a>Testing Coverage

<img src="static/img/coverage.png" height="350">


## <a name="run-local"></a>How To Run Locally

Need TWO Google Maps API keys: Browser Key and Server Key
https://console.developers.google.com
Make sure to store keys in a secrets.sh and put the file in your `.gitignore`.

Create a virtual environment

```
> virtualenv env
> source env/bin/activate
```

Install the dependencies

```
> pip install -r requirements.txt
```

In a new Terminal run App
```
> python server.py
```

## <a name="optimization"></a>Current Optimization

- Profiled application 
- Decrease number of API calls
	- Building db to store distance results
	- Update logic to search db first for every new request
	- If not found, then make API call
- Refactor using Dijkstra's algorithm


Author: [Katia Wu](https://www.linkedin.com/in/katiayx)
