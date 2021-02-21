## 2.3 Project

With this python code you can make POST requests to https://motorscraper.herokuapp.com/predict in a flask app to get predictions from a trained model on the prices for motorcycles form autoscout.nl.



Table of content
* [Installation](#installation)
* [Getting Started](#getting-started)
* [Technologies Used](#technologies)
* [Contributing](#contributing)
* [License](#license)


### Installation
To run the code please take a look at the following instructions

1. Download or clone this repo

2. Run `flask run <main.py> --host='localhost' --port=9000` in the terminal

3. Make requests with the requests library like so:
   
```
requests.post("http://localhost:9000/predict", data=json.dumps({"inputs": [4.60000000e+04, 2.50000000e+01, 1.98500000e+03, 7.86409627e+02,0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 1.00000000e+00,0.00000000e+00, 1.00000000e+00, 0.00000000e+00, 0.00000000e+00,0.00000000e+00, 0.00000000e+00, 0.00000000e+00]}))
```


### Getting Started
This flask app is connected to Heroku. 
To get started you must 

1. Firstly, go to the main folder of the project and run `heroku login`. If running this causes an error make sure you have the Heroku CLI installed on your machine.
2. Create a Heroku app `heroku create`
3. Initialize git `git init`
4. Add everything to git `git add .`
5. Commit `git commit -m "My first commit"`
6. Push to Heroku `git push heroku master`
7. Now you can do `heroku open` to see your flask app live 


### Technologies
For the used packages and technologies view the [requirements.txt](requirements.txt) file.


### Contributing
Please let me know if you encounter a bug by filing an issue, all contributions are appreciated!

If you plan to contribute new features please send a PR.

### License
Calculator has a MIT-style license, as found in the [LICENSE](LICENSE) file.