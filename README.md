# Dice Relabeler
A python script to calculate a relabeling of 2 dice that preserves the original probability distribution.
This project was developed as a research project for MA421 Modern Algebra at Eastern Nazarene College.

## Getting Started

The simulation is written in Python 3 using several common libraries including numpy and sympy. 
The easiest way to install python with the packages required is to install the Anaconda distribution.


## Running the Simulation

The python script is designed as a command line utility, so the easiest way to lean to use it is to look at the help files. 
Clone the repository and run:

```bash
$ python3 dice.py --help

usage: dice.py [-h] [-v | -q] [-s SIDES]

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Enable verbose output
  -q, --quiet           Enable quiet output
  -s SIDES, --sides SIDES
                        set the number of sides on each die
```
This will show all of the options for running the simulation. 
The only required field is `-s ` which specifies the number of sides to calculate.

## Built With

* [Anaconda](https://anaconda.org/) - The Python distribution used

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

## Authors

* All mathematical theory and code were initially developed by [**Caleb Vatral**](https://github.com/kbvatral)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Acknowledgments

* Special thanks to Dr. Marcus Fries, who guided me in the process of developing the math behind this simulation
