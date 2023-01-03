# Surviving Cotonou - A PyGame Project

## Project Summary

This project is my interpretation of the "Alien Invasion" challenge (chapters 12 - 14) of the book "Python Crash Course" by Eric Matthes, which I named "Surviving Cotonou". It is a tribute to #Cotonou (the economic centre of #Benin), where we had the pleasure of living for three months in spring 2022, and its unsung heroes - the countless #Zem (motorbike) riders.

I found the following steps particularly challenging:

- Generating the motorbikes at random positions without overlapping.
- Time-limited display of the buttons in case of a crash or reaching a next round
- Continuous increase of the number of motorbikes and their speed

## Demonstration Video

https://user-images.githubusercontent.com/61935581/210384867-143ab6a3-37b6-4177-af0c-a6f8eda78d84.mp4

## Installation

Clone the repository and create a new virtual environment

```bash
python3 -m venv envname # to create the virtual env
source envname/bin/activate # activate it
```

Afterwards install the libraries specified in requirements.txt

```bash
pip install -r requirements.txt
```

Run the main project file surviving_cotonou.py

```bash
python3 surviving_cotonou.py
```

## Usage

Use the up, down, left and right arrows to control the person. Try to get as fast as possible to the right side of the screen without hitting a Zem driver. There are three levels in total.

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
