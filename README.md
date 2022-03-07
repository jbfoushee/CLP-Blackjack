# CLP-Blackjack

## Introduction

My project was initially to challenge the [Blackjack Cheat Sheet](https://th.bing.com/th/id/R.939215ae5b7b73e78a613e8d7d8f8855?rik=9V0Yf%2b33050XtQ&pid=ImgRaw&r=0) that you see freely-distributed on the Internet.


I retrieved the dataset "[900,000 Hands of BlackJack Results](https://www.kaggle.com/mojocolors/900000-hands-of-blackjack-results)" from [Kaggle](https://www.kaggle.com).

However, this became more of a discovery of the data I downloaded, because expectations were not met.

## Data Discovery

The author's simple description of the dataset was this:
"The data was generated from the code used to analyse a million hands of Blackjack. The cards are distributed as seen in a casino. Idea is find out patterns and find out a strategy to optimize wins. The different columns are cards distributed to players and dealer and their sum of cards and how that round was won, either by player or by the dealer."

There was no further documentation on how the data was gathered.
- How often was the shoe (set of cards) swapped out?
- How many decks of cards were involved?
- What are the rules for the players to follow?

The dataset is laid out as follows:
- Index: Repeatable numerics of 0 to 5
- PlayerNo: Identifies each player. There are 6 playing each round.
- ![#157500](https://via.placeholder.com/10.png/0f0/fff) card1: First card dealt to the player (range 1 - 11)
- ![#157500](https://via.placeholder.com/10.png/0f0/fff) card2: Second card dealt to the player (range 1 - 11)
- ![#157500](https://via.placeholder.com/10.png/0f0/fff) card3: Third card dealt to player, if needed (range 0 -11)
- card4, card5: subsequent cards dealt to player, if needed (range 0 -11)
- sumofcards: player's sum at end of round
- ![#157500](https://via.placeholder.com/10.png/0f0/fff) dealcard1: First card dealt to the dealer (range 1 - 11)
- dealcard2: Second card dealt to the dealer (range 1 - 11)
- dealcard3, dealcard4, dealcard5: subsequent cards dealt to dealer, if needed (range 0 -11)
- sumofdeal: dealer's sum at end of round
- blkjck: indicates if player initially dealt a Blackjack combo (10 + A)
- ![#157500](https://via.placeholder.com/10.png/0f0/fff) winloss: Indicates if player won or lost { Win, Loss, Push }
- plybustbeat: If player loses, was he beat or did he bust
- dlbustbeat: If dealer loses, was he beat or did he bust
- plwinamt: Total amount won by player each round
- dlwinamt: Total amount won by Dealer each round
- ![#157500](https://via.placeholder.com/10.png/0f0/fff) ply2cardsum: Sum of the first 2 cards dealt to player

I chose just the columns in green.
The first two cards would be the player's hand, and the third card would decide if the player "hit" or "stayed."
The dealcard1 is the dealer's face-up card. The player is not privy to the dealer's second card until a hit/stay decision is made, so I have no use for the dealcard2 column.
I chose the ply2cardsum column only after I realized I built a column to hold the same value.

A few things I immediately noticed:
- An Ace is considered 1 or 11. Although fluid during the player's session, the end value is recorded in the row.
- No data suggests a split occurs. Therefore I would be unable to provide any reasonable advice for player pairs (8/8, A/A, etc).

I assumed the player's actions would be random. I initially built a box for each {My Hand / Dealer Face-Up} scenario
```
For Dealer showing 7, Player has 15 (no ace)

               | Wins/Ties | Losses | Instances
-----------------------------------------------
Player Hits    |         0 |      0 |      0
Player Stays   |      1707 |   3155 |   4862        
```
At this point, I realized the players are following a script for "15 vs 7"
In the real-world, I always have to assume the dealer is hiding a 10.
I would review the other cards on the table. If most are high, I would hope for a small card.
Heck, I might even hit just to "fight" for it, because staying only works 35% of the time.
Although this scenario is not quantifiable in data, I would have liked to see a "Hit vs Stay" argument.

With this, I had to reconsider the entire project. 
There is no way to recreate the Blackjack Cheat Sheet. The actions are fixed.

## Project
This project shows a visual confidence of prescribed actions ("Hit" or "Stay"), based solely on the player's initial two cards.
The data comes from the dataset "[900,000 Hands of BlackJack Results](https://www.kaggle.com/mojocolors/900000-hands-of-blackjack-results)" from [Kaggle](https://www.kaggle.com).

This was built in Python version 3.10 in a venv environment.
After activating the venv environment, please install the libraries in the requirements.txt
```
pip install -r requirements.txt
```

## Requirements satisfied

### Category 1: Python Programming Basics:
Create and call at least 3 functions or methods, at least one of which must return a value that is used somewhere else in your code. To clarify, at least one function should be called in your code, that function should calculate, retrieve, or otherwise set the value of a variable or data structure, return a value to where it was called, and use that value somewhere else in your code

### Category 2: Utilize External Data
Read data from an external file, such as text, JSON, CSV, etc, and use that data in your application.

### Category 3: Data Display
Display data in tabular form

### Category 4: Best Practices
The program should utilize a virtual environment and document library dependencies in a requirements.txt file.

### Stretch Features
Use pandas, matplotlib, and/or numpy to perform a data analysis project. Ingest 2 or more pieces of data, analyze that data in some manner, and display a new result to a graph, chart, or other display.

## Reflection
This was a great project to start with Python and data analysis.

Having real-world knowledge, I was extremely disappointed in the data gathering, and the rules of playing.
The players' actions were solely based on their initially-dealt cards devoid of any influence from the dealer. This is entirely reckless.
