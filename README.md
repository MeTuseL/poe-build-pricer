# POE Pricer
Project to create a web application to price full build from Path of Exile.

## SUMMARYS
1. [Contexte](#1-Contexte)
2. [Current state of the project](#2-Current-state-of-the-project)
3. [Future of the project](#3-Future-of-the-project)
4. [Documentation](#4-Documentation)
5. [Credits](#5-Credits)

## 1. Contexte
This project is born out of the idea that pricing a full build could be useful to PoE players, taking into account all items buyable in the build and totaling the price automatically.

With this idea, the proposed format of application would be a web application that would permit the core features :
- Import a build from a PoB link, pobb.in or other format of build sharing
- Load the build with a graphique interface that shows items of the build
- Display price of each item in correspondence with option selected (League, Softcore or Hardcore, a specific date, ...etc )
- Connect to an account with your PoE account
  - Save your build with configuration to look at later
  - Import a build from your account or another account with secure use of the POESESSID.
- Get general price and market data linked to your loaded build

## 2. Current state of the project
### What is done
Currently, the project only has a fonctional demo, working launching a first local server from the python/django backend and a second local server from the React backend.\
Features currently working :
1. A webpage to input a PoB code
2. Loading a PoB code and decoding it to an XML
3. Transforming the XML to a JSON file readable in the frontend
4. Fetching price of the different items of the build
5. Graphically displaying items and their price in the webpage 

### What it currently looks like
todo
### Current limitation
todo

## 3. Future of the project
todo

## 4. Documentation
Documentation is located in **_docs/_** folder.\
You'll find a lot of information no here there (Detail on backend and frontend, instruction on launching server, conception details, ...etc)

It can contain some general information about the project + specific information to backend and frontend in their respective folders (**_docs/backend/_** and **_docs/frontend/_**).

## 5. Credits
The Project was founded by [Erico Labare](https://github.com/Erico-Labare) and [MeTuseL](https://github.com/MeTuseL).

We thank Grinding Gear Games for their [game](https://www.pathofexile.com/) and for freely sharing their API to fetch market data.
In the same way, we thank [poe.ninja](https://poe.ninja/) for the data they provide with their API and their general work.



