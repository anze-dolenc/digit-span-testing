# Digit Span Testing

This repository is for Digit Span testing and training (in Estonian and in English), as well as training the phonetic number system in Estonian. It was initially developed for the Artificial and Natural Intelligence (ANI) course at the University of Tartu.

## Digit Span testing

Digit span is a common measure of working memory and short term memory. Current program allows to test the forward span where a sequence of digits is given as audio, and recall is done through typing. 

This program allows to measure it using a method described by Woods and colleagues (2011), where participants go through 14 trials, beginning with 3 digits for Forward Span (FS). Correcly recalling a sequence increases the length of the next sequence by one. Incorrectly recalling two consecutive sequences reduces the length of the next sequence by one.

```
# optional - create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# install requirements
pip install -r requirements.txt

# run
python3 digit_span.py
```

## Digit Span training

Artificial and Natural Intelligence (ANI) course has offered group projects where participants train their Digit Span across 25 days, 1 hour each day. This is inspired by Chase and Ericsson (1982), where SF increased his digit span from 7 to over 80 through practice.

```
# run
python3 mnemonic_training.py
```

## Mnemonic training - Estonian phonetic number system

The program includes functionality to train mapping digit sequences to corresponding words according to the Estonian phonetic number system. Included digit to letter mapping was created by Taavi Kivisik in 2008.

## About

This project was initially created as part of the Artificial and Natural Intelligence couse at the University of Tartu. In 2023, initial code was contributed by Tamur Talviku, Gregor Nepste, Kirill Jurkov, Madis Peterson, Kristjan Solmann. In 2024, Matthias Reima contributed parts. The project has been supervised by Taavi Kivisik.

## Contributions

Contributions are welcome. Anyone making a pull request agrees to allow their contribution to be licenced under the same licence as the rest of the code in this repository.

# References

Chase, W. G., & Ericsson, K. A. (1982). Skill and Working Memory. In Psychology of Learning and Motivation (Vol. 16, pp. 1–58). Elsevier. https://doi.org/10.1016/S0079-7421(08)60546-0

Woods, D. L., Kishiyama, M. M., Yund, E. W., Herron, T. J., Edwards, B., Poliva, O., Hink, R. F., & Reed, B. (2011). Improving digit span assessment of short-term verbal memory. Journal of Clinical and Experimental Neuropsychology, 33(1), 101–111. https://doi.org/10.1080/13803395.2010.493149