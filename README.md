# For-A-Cause

## About this project
This project is part of the AWS Hackathon submissions that enables users to discover and donate to charities that speaks to them (yes, literally!) via any Amazon smart device with voice enabled capabilities! We have developed a full eco-system to support charities to help raise funds:
* A front-end for charities to register with us and provide us with their information to share with users
* An AWS DynamoDB database that stores the information
* An Alexa voice skill that allows the users to easily discover charities that are meaningful to them with an option to make a donations via Amazon Pay.

Our system architechure is as follows:
<table><tr><td>
    <img src="https://github.com/kmorawala/For-A-Cause/blob/master/Images/System%20Diagram.png" />
</td></tr></table>

## Inspiration
Our project’s inspiration came from when we were looking for a way to donate to a certain charity in a quick and easy manner via voice interactions. In this world of technology, we did not come across any skill that was comprehensive enough to support both users and charities while allowing donations to be made via voice commands. Once we discovered this gap, we quickly brainstormed some ideas and decided to create a blueprint for this project.

## What it does and How we built it
Our design is broken into three tiers:

* **Charity Interactions:** A front-end is dedicated for the charities to register with us and provide us with valuable information to share with users.
* **Storage:** An AWS (DynamoDB) NoSQL database is utilized that stores the information provided by the charities and later retrieved by the Alexa skill.
* **User Interactions via Alexa voice skill:** The user interacts with the app using an Amazon smart device via Alexa voice skill - **For A Cause**. Python is used for the back-end logic for the skill development. The back-end retrieves necessary information from the database, uses Amazon Pay for processing donation payments, and handles other requests as made by the users.

We used the following technologies:
* Python
* Github
* Alexa SDK
* AWS DynamoDB
* HTML/CSS/Javascript template

## How to use it:

Please refer to the "How to set up" section to set up before using it.

By invoking the wake word "Alexa, open for a cause", the user can simply get started. The app provides necessary help instructions as the users interact.

Similarly, the charities can access the registration form here: TBD

## Challenges we ran into
All of our team members do not have extensive experience in this area, and some of us are completely new to developing a voice skill. The challenge was to familiarize ourselves quickly with new concepts, build and test an app. We found this challenge to be fun and rewarding.

## Accomplishments that we're proud of
We feel proud to be able to develop a multi-facet system that the charities can use to raise funding, while making it easier for the users to donate to their favorite charities!

## What we learned
We learned an abundance of things from where we started. A few of the highlights are as follows:
* Alexa Voice Skills
* AWS DynamoDB and its integration to Alexa skills
* AmazonPay and its integration to Alexa skills
* Various front-end technologies

## What's next for our project
We would like to add features such as monthly subscription, charity of the month, ability for charities to obtain user address to send appreciation gifts, and so forth. We think this app has a huge potential to help non-profits!

## References
TBD


## How we set it up:

* Alexa Skill
Since this app has not been published into the market place, if you would like to use it on your Alexa devices, go to [Alexa Developer Console](https://developer.amazon.com/alexa/console/ask) and click on **Create a Skill**

<table><tr><td>
    <img src="https://github.com/kmorawala/For-A-Cause/blob/master/Images/Create_Skill.png" />
</td></tr></table>

Click on **Custom** 

<table><tr><td>
    <img src="https://github.com/kmorawala/For-A-Cause/blob/master/Images/Skill%20Name.png" />
</td></tr></table>

Choose **Start from scratch**.

<table><tr><td>
    <img src="https://github.com/kmorawala/For-A-Cause/blob/master/Images/Choose_Template.png" />
</td></tr></table>

### Tabs
There are three tabs that we will work in this tutorial: Build, Code and Test. Feel free to work with more and use additional functionalities as you like. 

<table><tr><td>
    <img src="https://github.com/kmorawala/For-A-Cause/blob/master/Images/Build_Test_Code.png" />
</td></tr></table>

### Build Tab
Give an appropriate **invocation** word under **Skill Invocation Name** field for your app. This word will start the skill when uttered by the user.

<table><tr><td>
    <img src="https://github.com/kmorawala/For-A-Cause/blob/master/Images/Invocations_Intents_Slots.png" />
</td></tr></table>

Under **Intents**, use the files from **Skill Invocation Name** folder to name and import various **Utterances**.

Similarly, use **Categories-values-slots.csv** file to create custom slot values.

Finally, click on **Save Model** and then **Build Model**. This step needs to be performed every time a change on the **Build** tab is made.

<table><tr><td>
    <img src="https://github.com/kmorawala/For-A-Cause/blob/master/Images/Save_Build_Model.png" />
</td></tr></table>

### Code Tab

Upload all of the remaining files to this tab, unless any of these files already exist and look identical. All the .txt files represent various categories of coding questions, one per line of the file. Further, the categories would match up to the slot values of **Categories** under the Build tab.

<table><tr><td>
    <img src="https://github.com/kmorawala/For-A-Cause/blob/master/Images/Code_Files.png" />
</td></tr></table>

Click on **Save** first. Once successfully saved, click on **Deploy**. This step may require additional configuration on AWS lambda when doing it for the first time. Every time something under the **Build** tab changes, these steps have to be performed.

<table><tr><td>
    <img src="https://github.com/kmorawala/For-A-Cause/blob/master/Images/Save_Deploy.png" />
</td></tr></table>

### Test Tab
This is where you can type in or speak to test your app on the left side and you will see JSON response on the right side.

<table><tr><td>
    <img src="https://github.com/kmorawala/For-A-Cause/blob/master/Images/Test.png" />
</td></tr></table>

<table><tr><td>
    <img src="https://github.com/kmorawala/For-A-Cause/blob/master/Images/Test_JSON.png" />
</td></tr></table>

If you reached this point, you have successfully made a wonderful app on your Alexa device. Test it out now! Be sure that you are using the same amazon account for your device as well as for the developer console.

* AmazonPay 

* Flask App
