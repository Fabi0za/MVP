#Importing the necessary modules
import logging
from flask import Flask, render_template, request, jsonify
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import json

#Creating the flask application
app = Flask(__name__)

#Configuring logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#Defining the path to the relevant data files
customer_data_path = '/Users/fabioza/Desktop/FinTech/MVP/customer_data.json'
agent_chatcorpus_path = '/Users/fabioza/Desktop/FinTech/MVP/agent_chatcorpus.json'
customer_chatcorpus_path = '/Users/fabioza/Desktop/FinTech/MVP/customer_chatcorpus.json'

#Loading customer data
with open(customer_data_path) as f:
    customer_data = json.load(f)

#Setting global variables that are later used in load_spacy_model and train_chatbot
nlp = None
keywords = None
responses = None

#Function to load the spacy model lazily (the model is only imported and loaded when the function is called)
def load_spacy_model():
    global nlp
    import spacy
    nlp = spacy.load("en_core_web_sm")

#Training the two chatbots
def train_chatbot(agent_chatbot, customer_chatbot):
    try:
        #Technically there could be two different chatcorpus but in this case both are the same
        trainer = ChatterBotCorpusTrainer(agent_chatbot)
        trainer.train(agent_chatcorpus_path)
        trainer = ChatterBotCorpusTrainer(customer_chatbot)
        trainer.train(customer_chatcorpus_path)
    #Sending an exception to the log if training fails
    except Exception as e:
        logger.error(f"An error occurred during training: {e}")

#Creating the two chatbots
def create_chatbot():
    agent_chatbot = ChatBot('AgentFinFluent')
    customer_chatbot = ChatBot('CustomerFinFluent')
    return agent_chatbot, customer_chatbot

def init():
    #Initializing dictionarires with keywords and responses, these will be used from the spacy model to link keywords to responses
    global keywords, responses
    #Creating the two chatbots
    agent_chatbot, customer_chatbot = create_chatbot()
    #Training the chatbots
    train_chatbot(agent_chatbot, customer_chatbot)
    #Loading the spacy model
    load_spacy_model()
    #Defining key words for each questions
    keywords = {
        "set_change_tax_allowance": ["set", "change", "tax", "allowance", "adjust", "modify", "capital", "income", "withholding", "levies", "custodian", "bank", "sale", "loss", "pots"],
        "tax_allowance_used": ["used", "tax", "allowance", "consumed", "remaining", "depleted", "balance"],
        "refund_capital_gains_tax": ["refund", "capital", "gains", "tax", "repaid", "return", "exemption", "order", "retrospectively", "solidarity", "surcharge", "church", "tax"],
        "exemption_order_change": ["exemption", "order", "adjust", "modify", "custodian", "bank", "Baader Bank", "deposited", "securities", "account"],
        "annual_tax_certificate": ["tax", "certificate"],
        "minimum_deposit": ["minimum", "deposit", "intial", "first"],
        "portfolio_transfer": ["portfolio", "transfer", "securities", "account", "time", "complete"],
        "registration_process": ["registration", "process", "workflow", "identification", "PostIdent"],
        "identity_verification": ["identification", "identity", "verification", "ID"]
    }

    responses = {
        "set_change_tax_allowance": 'The final withholding tax on investment income (capital gains tax, solidarity tax, and, where applicable, church tax) is paid on a transaction-by-transaction basis. The respective levies are withheld by the custodian bank after each sale, taking into account tax allowance and loss pots where applicable, and forwarded to the tax office.\n\nThis only applies to customers subject to taxation in Germany. Customers who have a tax residence outside of Germany are obliged to determine and pay the applicable taxes themselves. Please note that Scalable Capital cannot provide tax advice in this regard. If you have any questions regarding your individual tax situation, please contact your tax advisor or your tax office.\n\nYou can find the amount of withholding tax paid by you in your personal customer area. To do this, please log into your Scalable Capital account on our website, open the menu item "Profile" and click on "Taxes".\n\nPlease note that crypto ETPs classified according to §23 are not subject to capital gains tax. You can find more information on this below under "How are crypto ETPs treated for tax purposes?',
        "tax_allowance_used": 'To see how much of your tax allowance has already been used, please log into your Scalable Capital account on our app or online and go to "Profile." In the "Taxes" section you can find all relevant information.',
        "refund_capital_gains_tax": 'If an exemption order is set up retrospectively, taxes already paid (capital gains tax, solidarity surcharge and church tax, if applicable) will be refunded. Please note that the exemption order must still be set up in the current calendar year?',
        "exemption_order_change": 'At the turn of the year from 2022 to 2023, the custodian bank, Baader Bank, will automatically increase all deposited exemption orders of Scalable clients by 24.844%. This change will, for example, increase exemption orders in the amount of 801 euros for individuals to 1,000 euros. The decimal places of the exemption order will be rounded up by 24.844% after rounding. Thus, an exemption order of 500 euros is changed to 625 euros instead of 624.24 euros. As soon as the modified exemption order is deposited in your securities account on 2 January, you can initiate a change to the exemption order in the customer area of your Scalable account.',
        "annual_tax_certificate": 'If you are liable to pay tax in Germany, you will receive an annual tax certificate. This will usually be provided to you electronically for the respective past year by the end of April of the following year. You will find it in the mailbox of your Scalable client area. As a Wealth client with securities account management via ING, you will receive your annual tax certificate by the end of April in your mailbox in INGs internet banking.',
        "minimum_deposit": '  You will select an amount for your initial deposit during the registration process. This amount must be at least 1 euro. Your available balance can be paid out in full or in part at any time. A high deposit is recommended in order to be able to start trading stocks, ETFs and funds immediately.',
        "portfolio_transfer": 'You are welcome to transfer your portfolio to Scalable Broker. You can find all information here . Securities account transfers initiated by your house bank cannot be accepted. Please note that it may take several weeks until the entire process of the transfer is complete.',
        "registration_process": 'The registration is completed online and only takes a few minutes. Registration via iOS or Android mobile app is also possible. You complete the identification via POSTIDENT (Please note: This step is not necessary for existing customers of our wealth management product with custody account management at Baader Bank). The account opening by the custodian bank usually takes up to three working days. As soon as your custody account has been opened and the initial deposit has been made, you can start trading.',
        "identity_verification": 'The Money Laundering Act (MLA) requires us to identify our customers. This identification is also in your interest, as it ensures a higher level of security in the customer relationship. An MLA-compliant identification is carried out conveniently via POSTIDENT video, online identification using your ID (eID), or in the traditional way at your post office. Do you have an NFC-enabled smartphone and a new German ID card with a PIN or a German electronic residence permit? Then we recommend online identification with your ID (eID). With this option, you can identify yourself around the clock and in less than two minutes.'
        }
    return agent_chatbot, customer_chatbot

#Initiliazing the two chatbots
agent_chatbot, customer_chatbot = init()

#Defining the routes for the web application
#This defines the landing page, the corresponding html code can be found in select.html
@app.route("/")
def home():
    return render_template("select.html")

#Defining the route for the agent chatbot
#Defining the message that is shown first once the chat is started
@app.route("/agent_chatbot")
def agent_chatbot_page():
    bot_message = 'Hello! Please enter a client number to load customer information, or enter "None" to proceed without loading customer information.'
    return render_template("agent_chatbot.html", bot_message=bot_message)

#Defining the route for the customer chatbot
#Defining the message that is shown first once the chat is started
@app.route("/customer_chatbot")
def customer_chatbot_page():
    bot_message = 'Hello, how can I assist you today?'
    return render_template("customer_chatbot.html", bot_message = bot_message)

#Setting up a route that responds to http GET requests on the get_agent_response path
@app.route("/get_agent_response", methods=["GET"])
def get_agent_bot_response():
    #Collecting the message that was sent by the user
    user_text = request.args.get('msg')
    #Logging the user text (logs can be accessed in the browsers console, usually by hitting F12)
    logger.info('Received agent message: %s', user_text)

    #Message if the user doesn't want any client information
    if user_text.lower() == "none":
        response = 'Proceeding without loading customer information.'
        return response
    #If first user input is client number
    elif user_text in customer_data:
        #Returning corresponding customer data, then displaying the initital question
        customer_info = customer_data[user_text]
        customer_info['customer_id'] = user_text
        response = {
            'customer_info': customer_info,
            'additional_message': 'How can I assist you with the customer request?'
        }
        return jsonify(response)
    else:
        #Otherwise proceed as normal, by gathering the right response from the json
       response = {
        'response': str(agent_chatbot.get_response(user_text))
        }
    return jsonify(response)

#Defining the route for response to the agent
@app.route("/get_agent_response", methods=["POST"])
def get_agent_response():
    #Accesing the JSON data sent in the POST
    data = request.json 
    #Extracting the user message from the json
    user_text = data.get('msg')
     #Extracting customer data from the json, default to empty dict if not present
    customer_data = data.get('customer_data', {})  # Extract customer data, default to empty dict if not present

    #Getting the chatbot response based on the user request
    chatbot_response = agent_chatbot.get_response(user_text)
    
    #If chatbot confidence is high enough, the chatbot's response is used (meaning that the exact question can be found in the chatcorpus)
    if chatbot_response.confidence > 0.5:
        response = str(chatbot_response)
    #Otherwise keyword matching with spacy is used
    else:
        #Parsing the user input
        doc = nlp(user_text)
        #Lemmatizing the user input (converting to stems, removing punctuation and stopwords)
        user_keywords = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]

        # Counting how many of the previously defined key words can be found in the user request and assigning scores
        scores = {key: 0 for key in keywords}
        for keyword in user_keywords:
            for key, values in keywords.items():
                if keyword in values:
                    scores[key] += 1

        #The best answer has the highest score (most keywords match)
        best_match = max(scores, key=scores.get)

        #If no matching words are found
        if scores[best_match] == 0:
            response = 'Sorry, I did not understand that. Could you please rephrase your question?'
        #Otherwise the best match is used as response and sent to the frontend
        else:
            response = responses[best_match]
            agent_chatbot.append(user_text, response)

    return jsonify({"response": response})

#Defining the route for the response to the customer
@app.route("/get_customer_response", methods=["POST"])
def get_customer_response():
    #Accesing the JSON data sent in the POST
    data = request.json
    #Extracting the user request
    user_text = data.get('msg')
    #Getting a response for the usser request
    chatbot_response = customer_chatbot.get_response(user_text)

    #If chatbot confidence is high enough, the chatbot's response is used
    if chatbot_response.confidence > 0.5:  
        response = str(chatbot_response)
    #Else keyword matching with spacy is used
    else:
        doc = nlp(user_text)
        #Lemmatizing the user input
        user_keywords = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]

        #Counting how many of the previously defined key words can be found in the user request and assigning scores
        scores = {key: 0 for key in keywords}
        for keyword in user_keywords:
            for key, values in keywords.items():
                if keyword in values:
                    scores[key] += 1

        #The best answer has the highest score (most keywords match)
        best_match = max(scores, key=scores.get)

        #If no matching words are found
        if scores[best_match] == 0:
                response = 'Sorry, I did not understand that. Could you please rephrase your question?'
        #Else the best match is streamed to the front end
        else:
            response = responses[best_match]
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run()