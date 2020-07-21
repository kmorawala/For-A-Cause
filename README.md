# For-A-Cause

- [About this project](#about-this-project)
- [Inspiration](#inspiration)
- [What it does and How we built it](#what-it-does-and-how-we-built-it)
- [How to use it](#how-to-use-it)
- [Challenges we ran into](#challenges-we-ran-into)
- [Accomplishments that we're proud of](#accomplishments-that-we're-proud-of)
- [What we learned](#what-we-learned)
- [What's next for our project](#what's-next-for-our-project)
- [How to test it](#how-to-test-it)
- [How we set up the Alexa Skill](#how-we-set-up-the-alexa-skill)
- [How we set up DynamoDB](#how-we-set-up-dynamoDB)
- [How we set up the Flask App](#how-we-set-up-the-flask-app)

## About this project
This project is part of the AWS Hackathon submissions that enables users to discover and donate to charities that speaks to them (yes, literally!) via any Amazon smart device with voice enabled capabilities! We have developed a full eco-system to support charities to help raise funds:
* A front-end for charities to register with us and provide us with their information to share with users
* An AWS DynamoDB database that stores the information
* An Alexa voice skill that allows the users to easily discover charities that are meaningful to them with an option to make a donations via Amazon Pay.

The following describes how the entire eco-system works:
<table><tr><td>
    <img src="https://github.com/kmorawala/For-A-Cause/blob/master/Images/How_it_works.JPG" />
</td></tr></table>

## Inspiration
Our project’s inspiration came from when we were looking for a way to donate to a certain charity in a quick and easy manner via voice interactions. In this world of technology, we did not come across any skill that was comprehensive enough to support both users and charities while allowing donations to be made via voice commands. Once we discovered this gap, we quickly brainstormed some ideas and decided to create a blueprint for this project. We wanted to provide charities with an avenue of voice activated donations that would help charities of any size, location, technology, and type, and our eco-system does just that!

## What it does and How we built it
Our design is broken into three tiers:

* **Charity Interactions:** A front-end is dedicated for the charities to register with us and provide us with valuable information to share with users.
* **Storage:** An AWS (DynamoDB) NoSQL database is utilized that stores the information provided by the charities and later retrieved by the Alexa skill.
* **User Interactions via Alexa voice skill:** The user interacts with the app using an Amazon smart device via Alexa voice skill - **For A Cause**. Python is used for the back-end logic for the skill development. The back-end retrieves necessary information from the database, uses Amazon Pay for processing donation payments, and handles other requests as made by the users. **Amazon Pay** is integrated in the Alexa Skill to enable seamless payment processing between the user and us.  

The system architechure and data flow are as follows:
<table><tr><td>
    <img src="https://github.com/kmorawala/For-A-Cause/blob/master/Images/System%20Diagram.png" />
</td></tr></table>

We used the following technologies:
* Alexa ASK (Alexa Skills Kit)
* Python
* AmazonPay
* AWS DynamoDB
* HTML
* CSS
* Jquery
* Bootstrap
* Flask
* Route53
* Application Load Balancer
* AWS Certificate Manager
* AWS CLI
* noSQL Workbench
* Slack
* Google Meet
* Github

## How to use it
Please refer to the "How to test" section before testing it. Judges are given beta tester and developer level access to the Alexa skill. A user access is created for the judges for DynamoDB. The user ID and passwords are provided in the original hackathon submission.

For donors/users, the skill can be used by invoking the wake word "Alexa, open for a cause", the user can simply get started. The app provides necessary help instructions as the users interact. It handles various situations, such as exploring more charities, donating to a charity or providing more information about charity, processing payments using Amazon Pay, etc.

The charities can access the registration form [here](https://www.for-a-cause.net/). The charity form collects various information from the charity for the Alexa skill to use and their e-mail address to arrange for the funding to be distributed periodically.

## Challenges we ran into
All of our team members do not have extensive experience in developing an Alexa skill and integrating it various AWS services, such as DynamoDB, AmazonPay, AWS certificate manager, etc. The challenge was to familiarize ourselves quickly with new concepts/technologies, research, build and test a fully functioning application. We found this challenge to be fun and rewarding and hoping that it would help charities to raise funding in future.

## Accomplishments that we're proud of
We feel proud to be able to develop a multi-facet system that the charities can use to raise funding, while making it easier for the users to donate to their favorite charities!

## What we learned
We learned an abundance of things from where we started. A few of the highlights are as follows:
* Alexa Voice Skills
* AWS DynamoDB and its integration to Alexa skills
* AmazonPay and its integration to Alexa skills
* Various front-end technologies
* Collaboration
* Time management
* Communication/interpersonal skills

## What's next for our project
We would like to add features such as monthly subscription, ability for charities to obtain user addresses to send appreciation gifts, and so forth. We think this app has a huge potential to help non-profits!

## How to test it
* Alexa Skill
Since this app has not been published to public, the hackathon judges have been provided the access to [Alexa Developer Console](https://developer.amazon.com/alexa/console/ask) and as beta testers. Once they login to [Alexa Developer Console](https://developer.amazon.com/alexa/console/ask), click on **Cause** and quickly make their way to the "Test" tab to test the app. Best way to test the app is by speaking to it rather than typing to avoid any non-word inputs (i.e. $1 instead of one dollar).

* DynamoDB
DyanmoDB can be accessed on [AWS Management Console](https://820223306190.signin.aws.amazon.com/console) using the username and password provided in the Devpost submission.

* Amazon Pay
Amazon Pay can be accessed on [Seller Central](https://sellercentral.amazon.com/invitation/accept?merchantId=A2G5K08S7KTD5R&invitationId=6daebb51-4159-452e-8371-34e3bc08bdd3) using the username and password provided in the Devpost submission. Select sandbox view upon login.

## How we set up the Alexa Skill
We wanted to provide some simple set up instructions for anyone who wanted to follow along!

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

#### Build Tab
Give an appropriate **invocation** word under **Skill Invocation Name** field for your app. This word will start the skill when uttered by the user.

<table><tr><td>
    <img src="https://github.com/kmorawala/For-A-Cause/blob/master/Images/Invocations_Intents_Slots.png" />
</td></tr></table>

Under **Intents**, use the files from **Alexa Skill/Slots_Intents** folder to name and import various **Utterances**.

Similarly, use **Categories-values-slots.csv** file to create custom slot values.

Finally, click on **Save Model** and then **Build Model**. This step needs to be performed every time a change on the **Build** tab is made.

<table><tr><td>
    <img src="https://github.com/kmorawala/For-A-Cause/blob/master/Images/Save_Build_Model.png" />
</td></tr></table>

Under "MakeDonationIntent," be sure to create a slot as follows:
<table><tr><td>
    <img src="https://github.com/kmorawala/For-A-Cause/blob/master/Images/MakeDonationIntentSlot.png" />
</td></tr></table>

Click on "Edit Dialogue" and set it up as follows:
<table><tr><td>
    <img src="https://github.com/kmorawala/For-A-Cause/blob/master/Images/DonationAmountSlotSetUp.png" />
</td></tr></table>

#### Code Tab

Upload all of the remaining files to this tab, unless any of these files already exist and look identical. All the .txt files represent various categories of coding questions, one per line of the file. Further, the categories would match up to the slot values of **Categories** under the Build tab.

<table><tr><td>
    <img src="https://github.com/kmorawala/For-A-Cause/blob/master/Images/Code_Files_2.png" />
</td></tr></table>

You will also need to establish a keys.py file that would include CarKeys class, under which "__role_creds" variable is set up to create an AWS IAM Policy to Grant AWS Lambda Access to an Amazon DynamoDB Table. See further details [here](https://aws.amazon.com/blogs/security/how-to-create-an-aws-iam-policy-to-grant-aws-lambda-access-to-an-amazon-dynamodb-table/)

Click on **Save** first. Once successfully saved, click on **Deploy**. This step may require additional configuration on AWS lambda when doing it for the first time. Every time something under the **Build** tab changes, these steps have to be performed.

<table><tr><td>
    <img src="https://github.com/kmorawala/For-A-Cause/blob/master/Images/Save_Deploy.png" />
</td></tr></table>

#### Test Tab
This is where you can type in or speak to test your app on the left side and you will see JSON response on the right side.

<table><tr><td>
    <img src="https://github.com/kmorawala/For-A-Cause/blob/master/Images/Test.png" />
</td></tr></table>

<table><tr><td>
    <img src="https://github.com/kmorawala/For-A-Cause/blob/master/Images/Test_JSON.png" />
</td></tr></table>

If you reached this point, you have successfully made a wonderful app on your Alexa device. Test it out now! Be sure that you are using the same amazon account for your device as well as for the developer console. If for some reason, the app does not work, be sure that "English-US" is selected as language under your Alexa App settings.

## How we set up DynamoDB

* DynamoDB
For testing purposes, or to follow along with the creation process, these are the steps to set up DynamoDB like we did.
(AWS Management Console -> DynamoDB) and click on **Create table**

<table><tr><td>
    <img src="https://github.com/kmorawala/For-A-Cause/blob/master/Images/DynamoDB/DynamoDBCreateTable.png" />
</td></tr></table>

Name the table "CharityInfo" and set the Primary Key to ID as a Number and then hit **Create**.
DynamoDB doesn't need to know the other rows yet, unlike a regular RDS.

<table><tr><td>
    <img src="https://github.com/kmorawala/For-A-Cause/blob/master/Images/DynamoDB/DynamoDBTableNameandID.png" />
</td></tr></table>

## How we set up the Flask App

* AWS Elastic Beanstalk
Luckily, Elastic Beanstalk takes care of most of the heavy lifting, spinning up everything needed to deploy our Flask App.

You will need to make sure to install EB CLI first, which can be done with Homebrew on a Mac:


`$ brew update`

`$ brew install awsebcli`


Once the EB CLI is installed, you can take the files downloaded from github, and easily deploy them to Elastic Beanstalk (Make sure to download only the folder labelled "Flask App", as this was run independently in it's own environment for deployment, and not tested with the bundle of "For-A-Cause").


`~/ForACauseFlaskApp$ eb init -p python-3.6 ForACauseFlaskApp --region us-east-1`

`~/ForACauseFlaskApp$ eb create flask-env`


Then we will open the app:


`~/ForACauseFlaskApp$ eb open`


From here, once the form is submitted, it will append the needed columns to the existing DynamoDB table that we created earlier.

### IAM Permissions

Lastly, we make sure each app has access to each other app. 

The Alexa_Lambda and aws-elasticbeanstalk-ec2-role role will need DynamoDBFullAccess.




