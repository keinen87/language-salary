# Programming vacancies compare

The script shows average salary for popular programmer vacancies by 30 days

# How to start

Python3 should be already installed. Then use pip (or pip3, if there is a conflict with Python2) to install dependencies:

```bash
pip install -r requirements.txt
```

### Environment variables.

- TOKEN


.env example:

```
TOKEN=v3.r.122857201.8f0cg543b36467ef22c8a234ae54290f700f836c.804fhh73cce5e8hgyr7n5c2397cgtracf570b7f2
```
### How to get

* Register an application [API Superjob](https://api.superjob.ru/) and get the `Secret Key`


### Run

Launch on Linux(Python 3.5) or Windows as simple

```bash

$ python main.py

# You will see

┌HeadHunter Moscow──────┬──────────────────┬─────────────────────┬──────────────────┐
│ Язык программирования │ Вакансий найдено │ Вакансий обработано │ Средняя зарплата │
├───────────────────────┼──────────────────┼─────────────────────┼──────────────────┤
│ Java                  │ 1745             │ 430                 │ 163728           │
│ C#                    │ 1088             │ 348                 │ 145706           │
│ Objective-C           │ 175              │ 52                  │ 179730           │
│ Python                │ 1369             │ 334                 │ 144901           │
│ C++                   │ 170              │ 84                  │ 129965           │
│ Go                    │ 366              │ 95                  │ 171563           │
│ Scala                 │ 183              │ 40                  │ 221327           │
│ PHP                   │ 1146             │ 552                 │ 118483           │
│ JavaScript            │ 2631             │ 799                 │ 136277           │
│ Typescript            │ 422              │ 153                 │ 164365           │
│ C                     │ 365              │ 199                 │ 127320           │
│ Swift                 │ 242              │ 81                  │ 175555           │
│ Ruby                  │ 205              │ 66                  │ 157121           │
└───────────────────────┴──────────────────┴─────────────────────┴──────────────────┘

┌SuperJob Moscow────────┬──────────────────┬─────────────────────┬──────────────────┐
│ Язык программирования │ Вакансий найдено │ Вакансий обработано │ Средняя зарплата │
├───────────────────────┼──────────────────┼─────────────────────┼──────────────────┤
│ Java                  │ 20               │ 490                 │ 14932            │
│ C#                    │ 28               │ 438                 │ 23607            │
│ Objective-C           │ 2                │ 57                  │ 11925            │
│ Python                │ 14               │ 394                 │ 16476            │
│ C++                   │ 25               │ 164                 │ 46492            │
│ Go                    │ 0                │ 95                  │ 1805             │
│ Scala                 │ 0                │ 40                  │ 5533             │
│ PHP                   │ 49               │ 637                 │ 14373            │
│ JavaScript            │ 64               │ 949                 │ 18979            │
│ Typescript            │ 5                │ 173                 │ 22915            │
│ C                     │ 19               │ 244                 │ 18000            │
│ Swift                 │ 1                │ 81                  │ 2167             │
│ Ruby                  │ 1                │ 71                  │ 14536            │
└───────────────────────┴──────────────────┴─────────────────────┴──────────────────┘

```

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)