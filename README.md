# For-A-Cause

## About this project
This project is part of the AWS Hackathon submissions that enables users to discover and donate to charities that speaks to them (yes, literally!) via any Amazon smart device with voice enabled capabilities! We have developed a full eco-system to support charities to help raise funds:
* A front-end for charities to register with us and provide us with their information to share with users
* An AWS DynamoDB database that stores the information
* An Alexa voice skill that allows the users to easily discover charities that are meaningful to them with an option to make a donations via Amazon Pay.

## Inspiration
Our project’s inspiration came from when we were looking for a way to donate to a certain charity in a quick and easy manner via voice interactions. In this world of technology, we did not come across any skill that was comprehensive enough to support both users and charities while allowing donations to be made via voice commands. Once we discovered this gap, we quickly brainstormed some ideas and decided to create a blueprint for this project.

## What it does and How we built it
Our design is broken into three tiers:

* Charity Interactions: A front-end is dedicated for the charities to register with us and provide us with valuable information to share with users.
* Storage: An AWS (DynamoDB) noSQL database is utilized that stores the information provided by the charities and later retrieved by the Alexa skill.
* User Interactions via Alexa voice skill: The user interacts with the app using an Amazon smart device via Alexa voice skill - For A Cause. Python is used for the back-end logic for the skill development. The back-end retrieves necessary information from the database, uses Amazon Pay for processing donation payments, and handles other requests as made by the users.

We used the following technologies:
* Python
* Github
* Alexa SDK
* AWS DynamoDB
* HTML/CSS/Javascript template

## How to use it:

By invoking the wake word "Alexa, open for a cause", the user can simply get started. The app provides necessary help instructions as the users interact.

Similarly, the charities can access the front-end here: TBD

## Challenges we ran into
All of our team members do not have extensive experience in this area, and some of us are completely new to developing a voice skill. The challenge was to familiarize ourselves quickly with new concepts, build and test an app. We found this challenge to be fun and rewarding.

## Accomplishments that we're proud of
We feel proud to be able to develop a multi-facet system that the charities can use to raise funding, while making it easier for the users to donate to their favorite charities!

## What we learned
We learned an abundance of things from where we started. A few of the highlights are as follows:
Alexa Voice Skills
AWS DynamoDB and its integration to Alexa skills
AmazonPay and its integration to Alexa skills
Various front-end technologies

## What's next for our project
We would like to add features such as monthly subscription, charity of the month, ability for charities to obtain user address to send appreciation gifts, and so forth. We think this app has a huge potential to help non-profits!

## References
