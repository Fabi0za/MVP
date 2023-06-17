## Description
The following repository contains the code for the MVP of FinFluent. FinFluent is an AI-powered customer service solution aimed at Fintech startups. Our mission is to improve and automate customer service across multiple channels such as email, chatbots, social media and phone by leveraging the power of large language models.

## Installation
In order to clone the repository run the following code block:
```
git clone https://github.com/Fabi0za/MVP.git
```

Then install the required dependencies by running the following code in your python environment:
```
pip install requirements.txt
```

## Code explanation
The code in this repository incorporates two different chatbots. The primary script is chatbot.py, which operates on the Flask framework. The JSON files store the chat corpus and customer data. The 'templates' directory includes HTML and CSS files for rendering the landing page and the two chatbot interfaces.

This code mainly utilizes Flask (a web framework for serving the application), ChatterBot (for creating conversational agents), SpaCy (for advanced natural language processing), JSON (for handling JSON files), logging (for recording events during the application's execution), and os (for interacting with the operating system).

The application operates on the Flask framework, with different Flask routes defining the various pages of the application. For each route, it precisely defines what should occur when users interact with the page. We have two routes set up for the two chatbots: 'agent_chatbot' and 'customer_chatbot'. These pages house the two chatbots. Whenever a user sends a message to the chatbot, either the '/get_agent_response' or '/get_customer_response' route is triggered depending on which chatbot is in use. ChatterBot then processes the user's message in the backend and generates a response.

Before processing the message, it gets broken down into keywords, which are then matched to corresponding questions and answers. The questions and answers are hard-coded in the agent_chatcorpus.json and customer_chatcorpus.json files and can be modified. At present, both files contain identical questions and answers. The corresponding keywords are defined in chatbot.py in the keywords dictionary. The bot initially undergoes training on these chat corpora using the train_chatbot() function.

To launch the Flask application, clone the repository and install all the dependencies. Then execute the chatbot.py file in a local Python environment, which starts a local Flask server. You can access the webpage on the local host; the corresponding IP address will be displayed in the console.
