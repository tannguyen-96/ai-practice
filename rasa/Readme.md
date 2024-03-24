### **References**
- [https://rasa.com/docs/](https://rasa.com/docs/)
- [https://www.youtube.com/watch?v=Ap62n_YAVZ8&list=PL75e0qA87dlEjGAc9j9v3a5h1mxI2Z9fi&index=1](https://www.youtube.com/watch?v=Ap62n_YAVZ8&list=PL75e0qA87dlEjGAc9j9v3a5h1mxI2Z9fi&index=1)

### **Get started**

Install rasa: ```pip install --update rasa```  

Project structure:
- domain.yml: all the thing that the assistant know to say, configurations, variables
- config.yml: nlu pipeline
- data/nlu.yml: example user input
- data/stories: actions
- data/rules: conditional

Create rasa project: ```rasa init```  
Train model: ```rasa train```  
Test model: ```rasa shell```  
Debug: ```rasa shell --debug```

##### **Domain (domain.yml)**  

The domain file is a directory of everything your assistant 'knows':
- *Responses*: These are the things the assistant can say to users
- *Intents*: These are categories of things users say
- *Slots*: These are variables remembered over the course of a conversation
- *Entities*: These are pieces of information extracted from incoming text
- *Forms and Actions*: These add application logic and extend what your assistant can do

*Responses*
This is the responses generated and the assistant will response to user by this without any model
```yml
responses:
  utter_greet:
  - text: "Hey! How are you?"

  utter_cheer_up:
  - text: "Here is something to cheer you up:"
    image: "https://i.imgur.com/nGF1K8f.jpg"

  utter_did_that_help:
  - text: "Did that help you?"

  utter_happy:
  - text: "Great, carry on!"

  utter_goodbye:
  - text: "Bye"
  
  utter_iamabot:
  - text: "I am a bot, powered by Rasa."
```

Let add multiple text to the response
```yml
responses:
  utter_greet:
  - text: "Hey {name}! How are you?"
  - text: "Hey {name}! How is your day going?"
```

When this response is triggered, one of the responses will be randomly selected. Then the {name} will be filled with the value of the name ("None" until it's filled)

We can also add button and image
```yml
responses:
  utter_greet:
  - text: "Hey! How are you?"
	buttons:
	- title: "great"
	  payload: "/mood_great"
	- title: "super sad"
	  payload: "mood_sad"

  utter_cheer_up:
  - text: "Here is something to cheer you up:"
    image: "https://i.imgur.com/nGF1K8f.jpg"
```

Channel selected
```yml
responses:
  utter_ask_game:
  - text: "Which game would you like to play on Slack?"
    channel: "slack"
  - text: "Which game would you like to play"
```

Custom output payloads
```yml
responses:
  utter_book_time:
  - custom:
	  blocks:
	  - type: section
	    text:
		  text: "Book a time for your appointment:"
		  type: mrkdwn
		accessory:
		  type: datepicker
		  initial_date: "2024-03-23"
		  placeholder:
		    type: plain_text
		    text: Select a date
```

*Intents*
Store the classes mapping with nlu training data to detect user input
```yml
intents:
  - greet
  - goodbye
  - affirm
  - deny
  - mood_great
  - mood_unhappy
  - bot_challenge
```

##### **Data**

What is "**data**" in conversational Al?
- The text data used to pretrain any models or features you're using (e.g. language models, word embeddings, etc.)
- User-generated text
- Patterns of conversations
- Examples:
    - Customer support logs (assuming data collection & reuse is covered in your privacy policy)
	- User conversations with your assistant

*Stories (data/stories.yml)*
It is training data to teach your assistant what it should do next.
```yml
stories:
  - story: happy path
    steps:
	- intent: greet # User input
	- action: utter_greet # Assistant action
	- intent: moood_great
	- action: utter_happy
```

OR statements
```yml
stories:
  - story: newsletter signup with OR
    steps:
	- intent: signup_newsletter
	- action: utter_ask_confirm_signup
	- or:
	  - intent: affirm
	  - intent: thanks
	- action: action_signup_newsletter
```

Use checkpoint
```yml
stories:
  - story: begining of conversation
    steps:
	- intent: greet
	- action: utter_greet
	- intent: goodbye
	- action: utter_goodbye
	- checkpoint: ask_feedback

  - story: user provides feedback
	steps:
	- checkpoint: ask_feedback
	- action: utter_ask_feedback
	- intent: inform
	- action: utter_thank_you
	- action: utter_anything_else

  - story: user doesn't have feedback
	steps:
	- checkpoint: ask_feedback
	- action: utter_ask_feedback
	- intent: deny
	- action: utter_no_problem
	- action: utter_anything_else
```

*Rules (data/rules.yml)*
A way to describe short pieces of conversations that always go the same way

| Do                                                                                       | Don't                                                      |
| ---------------------------------------------------------------------------------------- | ---------------------------------------------------------- |
| Use actual user conversations as stories                                                 | Use rules for multi-turn interactions                      |
| Have small stories that aren't full conversations                                        | Use OR statements and checkpointing often                  |
| Use rules for one-off interactions (checking account balance, checking if this is a bot) | Write out every possible conversation flow start to finish |
|                                                                                          | Delay user testing!                                        |

*Natural-language understanding (data/nlu.yml)*
The examples are the input of the user might ask
```yml
nlu:
- intent: greet
  examples: |
    - hey
    - hello
    - hi
    - hello there
    - good morning
    - good evening
    - moin
    - hey there
    - let's go
    - hey dude
    - goodmorning
    - goodevening
    - good afternoon
```

Paring down intents
```yml
book_train:
  - One train ticket
  - Need to book a train ride
  - A rail journey please
book_plane:
  - One plane ticket
  - Need to book a plane ride
```

Don't use intents as a way to store information (Storing information = slots)
Do a lot of the same tokens show up in training data for two intents? Consider if they can be combined
```yml
make_booking:
• One [train] (train) ticket
• Need to book a [train] (train) ride
• A [rail] (train) journey please
• One [plane](air) ticket
• Need to book a [plane] (air) ride
• i'd like to book a trip
• Need a vacation
```

Training data for the intent
- User-generated > synthetic
- Each utterance should unambiguously match to a single intent
	- You can verify this using human sorting & inter-rater reliability
- Is an utterance ambiguous?
	- Use end-to-end instead (the raw text as training data w/out classifying it)
```yml
Unambiguous:
  - Hi there
  - Hola
  - said, helllllloooooo!!!!
  - What is up?
  - ayyyy whaddup
  - hello robot
  - hello sara
  - merhaba
  - ola sara
Ambiguous (goes in end to end):
  - good day
  - ciao
  - alhoa
```

##### **Entities**

Entities are structured pieces of information inside of a user message. An entity can be any important detail that your assistant could use later in a conversation:
- Numbers
- Dates
- Country names
- ...
- Product names

Example the user input is: "My account number is 123456789", the number 123456789 should be an entity
```yml
nlu:
- intents: inform
  examples: |
    My account number is [123456789](account_number)
```

There are 3 ways entities can be extracted in Rasa:

*Using pre-built models*:
- Duckling for extracting numbers, dates, url, email addresses 
- SpaCy - for extracting names, product names, locations, etc
Example input: I am looking for a flight to ==Canada== that is under ==$500==
```json
{
	entity: location,
	value: Canada,
	component: SpaCyEntityExtractor
}

{
	entity: number,
	value: 500,
	component: DucklingHttpExtractor
}
```

*Using regex*
- For entities that match a specific pattern (e.g. phone numbers, postcodes, etc.)
Example input: My account number is ==1234567891==

```json
regex: \d{10,12}
```

```yml
nlu:
  - regex: account_number
    examples:
	- \d{10, 12}
  - intent: inform
    examples: |
    - My account number is [1234567891] (account_number)
```

*Using machine learning*
- For extracting custom entities
Example input: I would like to check my ==savings account==
```json
{
	entity: account_type,
	value: savings_account,
	component: DIETClassifier
}
```

```yml
nlu:
  - intent: check_balance
    examples: |
    - I would like to check my [savings account] (account_type)
    - Can you show me the balance of my [current account] (account_type)
```


Output
```json
{
	"entities": [{
		"value": "New York Ciry",
		"start": 20,
		"end": 33,
		"confidence": 0.78,
		"entity": "city",
		"extractor": "DIETClassifier"
	}]
}
```

---

*Synonyms*
Synonyms can be used to map the extracted values to a single standardized value
```
nlu:
  - synonym: credit
    examples:|
    - credit card account
    - credit account
```

```
nlu:
  - intent: check_balance
    examples:|
    - I would like to check my [credit card account] {"entity": "account", "value": "credit"}
    - How do I check the [credit account] {"entity": "account", "value": "credit"}
```

*Lookup tables*
Lookup tables are lists of words used to generate case-sensitive regular expression patterns
```yml
nlu:
  - lookup: country
    examples: |
    - Afghanistan
    - Albania
    - Zambia
    - ...
    - Zimbabwe
```

*Entity Roles*
Allow you to define the roles of the entities of the same groups.
Example input: I am looking for a flight from ==New York== to ==Boston==.

Extracted data:
```json
{
	entity: location,
	value: New York,
	role: origin
}

{
	entity: location,
	value: Boston,
	role: destination
}
```

```yml
nlu:
  - intent: book_a_flight
    examples: |
    - I am looking for a flight from [New York] {"entity":"location", "role":"origin"} to [Boston] {"entity":"location", "role": "destination"}.
```

*Entity Groups*
Allow you to put extracted entities under a specific group.
Example input: I would like a large pepperoni with ==cheese== and ==mushrooms==.

Extracted data:
```json
{
	entity: toppings,
	value: cheese,
	role: 1
}

{
	entity: toppings,
	value: mushrooms,
	role: 1
}
```

```yml
nlu:
  - intent: order_pizza
    examples: |
    - I would like a large pepperoni with [cheese] {"entity":"toppings", "group":"1"} and [mushrooms] {"entity":"toppings", "group":"1"}.
```


##### **Slots**
Slots are your assistant's memory. Slots enable your assistant to store important details and later use them in a specific context.
Example input: I would like to book  a flight to ==Sydney==

Extracted data:
```json
{
	slot: destination,
	value: Sydney
}
```

Response: Booking a ticket to ==Sydney==!

*Configuring slots*
Slots are defined inside of your `domain.yml` file:
```yml
slots:
  destination:
    type: text
	influence_conversation: false
	mappings:
	- type: custom
```

*Setting slots*
1 - Using NLU: Value from extracted entities
```yml
entities:
  destination

slots:
  destination:
    type: text
    influence_conversation: false
	mappings:
	- type: from_entity
	  entity: destination
```
2 - Using custom action

*Influencing the conversation*
Slots can be configured to influence the flow of the conversation. How and when this should happen depends on the type of the slot.
```yml
slots:
  destination:
    type: text
    influence_conversation: true
	mappings:
	- type: custom
```

`influence_conversation = true`
Defines that the slot will influence how the dialogue management model makes the prediction for the next action. Depending on the type of the slot the flow can be influenced by the value of the slot or whether the value of this slot is present.

| Approach 1                                          | Approach 2                                      |
| --------------------------------------------------- | ----------------------------------------------- |
| **User**: I would like to book a flight to New York | **User**: I would like to book a flight ticket. |
| **Bot**: Sure! Looking for the options.             | **Bot**: What is your destination?              |

`influence_conversation = false`
Defines that the slot would not influence the flow of the conversation and should only be used for storing the value of the slot.

| Approach 1                                                         | Approach 2                                           |
| ------------------------------------------------------------------ | ---------------------------------------------------- |
| **User**: Hello, I am Anna. I'd like to book a flight to New York. | **User**: Hi, I'd like to book a flight to New York. |
| **Bot**: Hello! Which date would you like to travel?               | **Bot**: Hello! Which date you like to travel?       |

*Configuring the stories*
If your slots are configured to influence the flow of the conversation, you have to include them in your training stories.
```yml
stories:
- story: booking a flight ticket
  steps:
  - intent: book_a_ticket
  - or:
	- slot_was_set:
	  - destination: Toronto
	- slot_was_set:
	  - destination: London
```

*Note*: More or statement more time to train

*Slot mapping*
Slots mappings allow you to define how each slot will be filled in. Slot mappings are applied after each user message.
```yml
entities:
  - entity_name
slots:
  amount_of_money:
    type: any
    mappings:
	- type: from_entity
	  entity: number
	  intent: make_transaction
	  not_intent: check_transaction
```

Example input: Send ==$200== to Ben.
Extracted data:
```json
{
	entity: number,
	value: 200
}
```

Classified as `make_transaction` -> Slot is set

Example input: Did I receive the ==$1000== that Alice sent me yesterday?
Extracted data:
```json
{
	entity: number,
	value: 1000
}
```

Classified as `check_transaction` -> Slot not set

*Slot mappings: `from_entity`*
The `from_entity` slot mapping fills in the slots based on the extracted entities.
```yml
entities:
- entity_name
slots:
  slot_name:
	type: any
	mappings:
	- type: from_entity
	  entity: entity_name
	  role: role_name
	  group: group name
	  intent: intent_name
	  not_intent: excluded_intent
```

| Key        | Usage                                                                   |
| ---------- | ----------------------------------------------------------------------- |
| role       | Only applies the mapping if the extracted entity has this role.         |
| group      | Only applies the mapping if the extracted entity belongs to this group. |
| intent     | Only applies the mapping when this intent is predicted.                 |
| not_intent | Does not apply the mapping when this intent is predicted.               |

*Slot mappings: `from_text`*
The `from_text` slot mapping will use the text of the last user message to fill in the slot.
```yml
slots:
  slot_name:
    type: text
	mappings:
	- type: from_text
	  intent: intent_name
	  not_intent: excluded_intent
```

*Slot mappings: `from_intent`*
The `from_intent` slot mapping fills in the slot with a specific defined value if a specific intent is predicted.
```yml
slots:
  slot_name:
	type: any
	mappings:
	- type: from_intent
	  value: my_value
	  intent: intent_name
	  not_intent: excluded_intent
```

*Slot mappings: `from_trigger_intent`*
The `from_trigger_intent` mapping will fill a slot with a specific defined value if a form is activated by a user message with a specific intent.
```yml
slots:
  slot_name:
	type: any
	mappings:
	- type: from_trigger_intent
	  value: my_value
	  intent: intent_name
	  not_intent: excluded_intent
```

*Slot mappings: `custom`*
If none of the predefined slot mappings fit your use case, you can create `custom` slot mapping using slot validation actions.
```yml
slots:
  day_of_week:
	type: text
	mappings:
	- type: custom
	  action: action_calculate_day_of_week
```

---

*Slot type*

*Slot type: `text`*
Slot type `text` can be used to store any text information. It can influence the conversation based on whether or not the slot has been set.
```yml
slots:
  destination:
	type: text
	influence_conversation: true
	mappings:
	- type: from_entity
	  entity: destination
```

*Slot type: `boolean`*
Slot type `boolean` can be used to store information that can get the values True or False.
```yml
slots:
  authenticated:
	type: boolean
	influence_conversation: true
	mappings:
	- type: custom
```

*Slot type: `categorical`*
Slot type `categorical` can be used to store values that can get one of the possible N values.
```yml
slots:
  price_range:
	type: categorical
	values:
	  - low
	  - medium
	  - high
	mappings:
	- type: custom
```

*Slot type: `float`*
Slot type `float` can be used to store numerical values.
```yml
slots:
  radius:
	type: float
	min_value: 0
	max_value: 100
	mappings:
	- type: custom
```

*Slot type: `list`*
Slot type `list` can be used to store a list of values. When configured, only the presence of the slot can have influence on the flow of the conversation
```yml
slots:
  items:
	type: list
	mappings:
	- type: from_entity
	  entity: shopping_item
```

*Slot type: `any`*
Slot type `any` can be used to store any arbitrary values. Slots of this type don't have any influence on the conversation flow which means that the value and the presence of the slot doesn't have any influence on how the conversation goes.
```yml
slots:
  shopping_items:
	type: any
	mappings:
	- type: custom
```

---

*Additional configurations: `initial_value`*
You can set a default initial value to your slot by configuring the `initial_value` parameter. The value will be assigned to the slot from the beginning of the conversation and can be reset later on by NLU or custom actions.
```yml
slots:
  current_account:
	type: float
	initial_value: 100
	mappings:
	- type: custom
```

##### **Responses**
Responses are simple messages that your assistant can send back to your users. Response templates are defined in the `domain.yml` file
```yml
responses:
  utter_greet:
    - text: "Hello! How are you?"
  utter_goodbye:
	- text: "Bye bye!"
```

*Creating multiple responses*
You can include more than one possible response for a specific template. Rasa will then randomly select which response to pick.
```yml
responses:
  utter_greet:
	- text: "Hello! How are you?"
	- text: "Hello there :)"
	- text: "Hi. How can I help you today?"
  utter_goodbye:
	- text: "Bye bye!"
```

*Using variables*
You can create more dynamic responses by including slots in the responses.
```yml
# domain.yml

entities:
  - name

slots:
  name:
	type: any
	mappings:
	- type: from_entity
	  entity: name
	
responses:
  utter_greet:
	- text: "Hello {name}! How are you?"
	- text: "Hello {name} :)"
	- text: "Hi {name}. How can I help you today?"
```

```yml
# data/nlu.yml
nlu:
- intent: greet
  examples: |
    - hey
    - hello
    - hi my name is [Tan](name)
```

Output:
```json
user: "hi"
bot: "Hey None! How are you?"
user: "hi my name is Tan"
bot: "Hi Tan. How can I help you today?"
user: "hi my name is Eddie"
bot: "Hi Tan. How can I help you today?"
```

*Including images*
You can make the responses more engaging by including the urls of the images you'd like to be included in the responses. How they will be rendered depends on the frontend you are using.
```yml
responses:
  utter_cheer_up:
	- text: "Here's something to cheer you up"
	- image: "https://i.imgur.com/1j2h3j4j5.com"
```

Output:
```json
user: "hi my name is Tan"
bot: "Hey Tan! How are you?"
user: "I am sad"
bot: "Here is something to cheer you up:"
"Image: https://i.imgur.com/1j2h3j4j5.com"
"Did that help you?"
```

To render the image instead the link, use built in UI `rasa x`
==Running Rasa X in local mode is no longer supported as Rasa has stopped supporting the Community Edition (free version) of 'Rasa X'==
![[rasaX.png]]

*Adding buttons*
You can enrich your assistant's responses by including buttons for specific options. You can configure the text that is visible on the buttons as well as the payload that is being sent to Rasa after a specific button is pressed.
```yml
# domain.yml

responses:
  utter_greet:
	- text: "Hey! How are you?"
	buttons:
	- title: "great"
	  payload: "/mood_great"
	- title: "bad"
	  payload: "/mood_bad"
```

Output:
```json
user: "hi"
bot: "Hey! How are you?"
"1: great (/mood_great)"
"2: bad (/mood_bad)"
user: "1: great (/mood_great)"
bot: "Great, carry on!"
```

*Custom payload*
If you prefer, you can get your assistant to send a custom payload to your frontend.
```yml
# domain.yml

responses:
  utter_take_bet:
  - custom:
	  blocks:
	  - type: section
		text:
		  text: "Make a bet on when the world will end:"
		  type: mrkdwn
		accessory:
		  type: datepicker
		  initial_date: 2019-05-21'
		  placeholder:
			type: plain_text
			text: Select a date
```

*Channel specific responses*
You can define responses that will be sent to a specific output channel.
```yml
# domain.yml

responses:
  utter_ask_game:
  - text: "Which game would you like to play on Slack?"
	channel: "slack"
  - text: "Which game would you like to play?"
```

*Training your assistant to use the responses*
To enable your assistant to actually use the defined responses, you have to include them into your training stories.
```yml
# domain.yml

stories:
- story: greet user
  steps:
  - intent: greet
  - action: utter_greet
```


##### Pipeline & Policy Configuration
NLU pipeline and dialogue policy configuration are the core of your assistant
```json
user: "Hello. I would like to check my account balance."
<... NLU pipeline processing steps...>
(intent: check_balance)
<... Dialogue Policy predictions...>
(next_best_action: ask_user_id)
bot: "Hello. Can you tell me your user id?"
```

NLU pipeline and dialogue policies are defined inside of your `config.yml` file
```yml
# config.yml

language: en # Define spoken language

pipeline: # Define nlu training pipeline - important
# will be selected by the Suggested Config feature

policies: # Define dialog management techniques and models use to responses - important
- name: MemoizationPolicy
- name: TEDPolicy
  max_history: 5
  epochs: 10
- name: RulePolicy
```

*NLU pipeline*
NLU pipeline defines the steps user messages will be passed through until a decision on what user's message is about is made
```json
user: "Hello. I would like to check my account balance."
<Tokenization>
<Featurization>
<intent classification & Entity Extraction>
(intent: check_balance)
```

Rasa comes with a number of components you can use to define your custom pipeline
```yml
# config.yml

language: en

pipeline:
  - name: WhitespaceTokenizer
  - name: Regex Featurizer
  - name: LexicalSyntactic Featurizer
  - name: CountVectors Featurizer
  - name: CountVectors Featurizer
	analyzer: char_wb
	min_ngram: 1
	max_ngram: 4
  - name: DIETClassifier
	epochs: 100
```

*Tokenizers*
They are used to parse user inputs into separate tokens (e.g. words)
```json
user: "Hello. I would like to check my account balance."
<Tokenizers>
[Hello, I, would, like, to, check, my, account, balance]
```

*Featurizers*
They are used to extract features from the tokens (convert token to vector)

*Classifiers*
Models used to assign a label to the user's input

---

*Training policies*
Training policies are techniques your assistant uses to decide on how to respond back to the user

*Policy priority*
Policy priority defines how assistant makes decisions when multiple policies predict the next actin with the same accuracy
Default policy priority in Rasa:
- 6 - `RulePolicy`
- 3 - `MemoizationPolicy` or `AugmentedMemoizationPolicy`
- 1 - `TEDPolicy`

Two types of policies available in Rasa
- Rule Policies: Assistant makes the decision on how to respond based on rules defined inside of your `rules.yml` file
- Machine Learning policies: Assistant makes the decision on how to respond by learning from the data defined inside of the `stories.yml` file.

*Rule Policy*
Rule Policy is the policy that allows you to impose a strict rule-based behavior on your assistant.
```yml
# rules.yml

rules:
- rule: Chitchat
  steps:
  - intent: chitchat
  - action: utter_chitchat
```




##### **Custom Actions**
What do we want virtual assistants to do?
-  Pick up what the user wants from the assistant.
-  Respond appropriately
	- Send back appropriate message
	- Send an email
	- Make a calendar appointment
	- Fetch relevant information from a database
	- Check information from an API
	- Calculate something specific

Approach:
```json
user: "Hey, what time is it in Amsterdam right now?"
<Extracted entity>
(Entity: Place)
<Call Custom Action>
(Take the place entity and return the current time)
bot: "It's currently 15:01."
```

Build Custom Action:
```yml
# data/nlu.yml

nlu:
- intent: inquire_time
  examples: |
    - what time is it?
    - what time is it in [Amsterdam)(place)?
    - what time is it in [London](place)?
    - tell me the time in [Lisbon](place)
    - what is the current time in [Berlin](place)
    - what time is it in [amsterdam](place)[amsterdam](place)

- lookup: place
  examples: |
    - brussels
    - zagreb
    - london
    - lisbon
    - amsterdam
    - seattle
```

```yml
# data/rules.yml

rules:
- rule: Tell the time
  steps:
  - intent: inquire_time
  - action: action_tell_time
```

```yml
# domain.yml

intents:
  - inquire_time

entities:
  - place

slots:
  location:
    type: text
    influence_conversation: true
    mappings:
    - type: from_entity
      entity: place

actions:
  - action_tell_time
```

```yml
# config.yml

pipeline:
  - name: RegexEntityExtractor
	use_lookup_tables: True
```

```python
# actions/actions.py
from typing import Any, Text, Dict, List
import arrow
import dateparser
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

city_db = {
    'brussels': 'Europe/Brussels',
    'zagreb': 'Europe/Zagreb',
    'london': 'Europe/Dublin',
    'lisbon': 'Europe/Lisbon',
    'amsterdam': 'Europe/Amsterdam',
    'seattle': 'US/Pacific'
}

class ActionTellTime(Action):
  
    def name(self) -> Text:
        return "action_tell_time"

    def run(self, dispatcher: CollectingDispatcher, # Send Messages
            tracker: Tracker, # Fetch Infor (Intent, Entities, Conversation,...)
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]: # domain.yml
        current_place = next(tracker.get_latest_entity_values("place"), None)
        utc = arrow.utcnow()

        if not current_place:
            msg = f"It's {utc.format('HH:mm')} utc now. You can also give me a place."
            dispatcher.utter_message(text=msg)
            return []

        tz_string = city_db.get(current_place, None)
        if not tz_string:
            msg = f"It's I didn't recognize {current_place}. Is it spelled correctly?"
            dispatcher.utter_message(text=msg)
            return []

        msg = f"It's {utc.to(city_db[current_place]).format('HH:mm')} in {current_place} now."
        dispatcher.utter_message(text=msg)

        return [] # Set Slots
```

```yml
# endpoints.yml

action_endpoint:
 url: "http://localhost:5055/webhook"
```

To run actions API: `rasa run actions`
To test the actions: `rasa train` -> `rasa shell`

Output:
```json
user: "what time is it in london?"
bot: "It's 08:07 in london now."
user: "what time is it in vietnam?"
bot: "It's 08:07 utc now. You can also give me a place."
user: "what time is it in isbon"
bot: "It's 08:08 utc now. You can also give me a place."
user: "what time is it in Lisbon"
bot: "It's I didn't recognize Lisbon. Is it spelled correctly?"
user: "what time is it in Amsterdam"
bot: "It's I didn't recognize Amsterdam. Is it spelled correctly?"
user: "what time is it in amsterdam"
bot: "It's 09:24 in amsterdam now."
```

---

There is one more thing that a Custom Action can do.
Additional approach:
```json
user: "Please remember that I live in Amsterdam"
<Save the current user location>
bot: "Will do!"
user: "What is the time difference with Berlin?"
<Compare the locations>
bot: "There is no time difference between Amsterdam and Berlin"
```

Update Custom Action:
```yml
# data/nlu.yml

- intent: where_i_live
  examples: |
    - please remember that i live in [Amsterdam](place)?
    - my house is in [London](place)?
    - reminder. i live in [Lisbon](place)
    - my residence is in [Berlin](place)
    - remember that i live in [london](place)

- intent: inquire_time_difference
  examples: |
    - time difference between [Amsterdam](place)?
    - what is my time difference with [London](place)?
    - how big is the time delta with [Berlin](place)?
    - is there a time difference with [Lisbon](place)?
    - what is the time difference with [amsterdam](place)
```

```yml
# data/rules.yml

- rule: Where I live intent
  steps:
  - intent: where_i_live
  - action: action_remember_where

- rule: Time Difference Intent
  steps:
  - intent: inquire_time_difference
  - action: action_time_difference
```

```yml
# domain.yml

intents:
  - where_i_live
  - inquire_time_difference

actions:
  - action_remember_where
  - action_time_difference
```

```python
# actions/actions.py

class ActionRememberWhere(Action):

    def name(self) -> Text:
        return "action_remember_where"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        current_place = next(tracker.get_latest_entity_values("place"), None)
        utc = arrow.utcnow()
        
        if not current_place:
            msg = "I didn't get where you lived. Are you sure it's spelled correctly?"
            dispatcher.utter_message(text=msg)
            return []
        
        tz_string = city_db.get(current_place, None)
        if not tz_string:
            msg = f"I didn't recognize {current_place}. Is it spelled correctly?"
            dispatcher.utter_message(text=msg)
            return []
        
        msg = f"Sure thing! I'll remember that you live in {current_place}."
        dispatcher.utter_message(text=msg)
        
        return [SlotSet("location", current_place)]


class ActionTimeDifference(Action):

    def name(self) -> Text:
        return "action_time_difference"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        timezone_to = next(tracker.get_latest_entity_values("place"), None)
        timezone_in = tracker.get_slot("location")
        
        if not timezone_in:
            msg = "To calculuate the time difference I need to know where you live."
            dispatcher.utter_message(text=msg)
            return []
        
        if not timezone_to:
            msg = "I didn't the timezone you'd like to compare against. Are you sure it's spelled correctly?"
            dispatcher.utter_message(text=msg)
            return []
        
        tz_string = city_db.get(timezone_to, None)
        if not tz_string:
            msg = f"I didn't recognize {timezone_to}. Is it spelled correctly?"
            dispatcher.utter_message(text=msg)
            return []
        
        t1 = arrow.utcnow().to(city_db[timezone_to])
        t2 = arrow.utcnow().to(city_db[timezone_in])
        max_t, min_t = max(t1, t2), min(t1, t2)
        diff_seconds = dateparser.parse(str(max_t)[:19]) - dateparser.parse(str(min_t)[:19])
        diff_hours = int(diff_seconds.seconds/3600)
        
        msg = f"There is a {min(diff_hours, 24-diff_hours)}H time difference."
        dispatcher.utter_message(text=msg)
        
        return []
```

To know slots that are being set, use: `rasa interactive`
After training by `rasa interactive` the result of training will be update in `nlu.yml`, `stories.yml` and `domain.yml`
Visualization: `http://localhost:5006/visualization.html`

##### **Forms**
Getting Data From Users
Approach 1:
```json
user: "I want to buy a pizza."
<rule>
(PIZZA-FORM: active, [ ] pizza-type slot, [ ] pizza-size slot)
bot: "What kind of pizza?"
user: "veggie"
<entity: pizza-type>
(PIZZA-FORM: active, [X] pizza-type slot =veggie, [ ] pizza-size slot)
bot: "What size?"
user: "large"
<entity: pizza-size>
(PIZZA-FORM: inactive, [X] pizza-type slot =veggie, [X] pizza-size slot =large)
bot: "Done!"
<custom-action>
```

Approach 2:
```json
user: "I want to buy a veggie pizza."
<rule>
<entity: pizza-type>
(PIZZA-FORM: active, [X] pizza-type slot =veggie, [ ] pizza-size slot)
bot: "What size?"
user: "large"
<entity: pizza-size>
(PIZZA-FORM: inactive, [X] pizza-type slot =veggie, [X] pizza-size slot =large)
bot: "Done!"
<custom-action>
```

Approach 3:
```json
user: "I want to buy a pizza."
<rule>
(PIZZA-FORM: active, [ ] pizza-type slot, [ ] pizza-size slot)
bot: "What kind of pizza?"
user: "fruit"
<entity: pizza-type>
(PIZZA-FORM: active, [ ] pizza-type slot =veggie, [ ] pizza-size slot)
bot: "What kind of pizza?"
```

Sample rule:
```yml
# rule to active pizza form
- rule: Activate Pizza Form
  steps:
  - intent: buy_pizza
  - action: simple_pizza_form
  - active_loop: simple_pizza_form

# rule to deactive
- rule: Submit Pizza Form
  condition:
  - active_loop: simple_pizza_form
  steps:
  - action: simple_pizza_form
  - active_loop: null
  - slot_was_set:
    - requested_slot: null
  - action: utter_submit
  - action: utter_pizza_slots
```

Build Custom Action:
```yml
# data/nlu.yml

- intent: buy_pizza
  examples: |
    - i'd like to buy a pizza
    - i want a pizza
    - can i buy a pizza
    - I'm interested in a savory round flattened bread of Italian origin
    - i want to buy a pizza
- intent: inform
  examples: |
    - i'd like a [large](pizza_size) pizza
    - i want to order a [xl](pizza_size) [hawai](pizza_type) pizza
    - [medium](pizza_size) pizza
    - [xl](pizza_size)
    - [small](pizza_size)
    - [s](pizza_size)
    - [pepperoni](pizza_type)
    - give me a [mozerella](pizza_type) pizza
    - [hawaii](pizza_type) pizza
    - [smol](pizza_size)
    - [hawaii](pizza_type)
    - i want a [large](pizza_size) pizza
    - [mozzarella](pizza_type)
    - [hawai](pizza_type)
    - [veggie](pizza_type)
    - [fungi](pizza_type)
    - i want a [large](pizza_size) pizza
    - [vegggie](pizza_type)
    - [veggie](pizza_type)
```

```yml
# data/rules.yml

- rule: Activate Pizza Form
  steps:
  - intent: buy_pizza
  - action: simple_pizza_form
  - active_loop: simple_pizza_form

- rule: Submit Pizza Form
  condition:
  - active_loop: simple_pizza_form
  steps:
  - action: simple_pizza_form
  - active_loop: null
  - slot_was_set:
    - requested_slot: null
  - action: utter_submit
  - action: utter_pizza_slots
```

```yml
 # domain.yml

intents:
- buy_pizza
- request_pizza_form

entities:
- pizza_size
- pizza_type

slots:
  pizza_size:
    type: text
    influence_conversation: true
    mappings:
    - type: from_entity
      entity: pizza_size
  pizza_type:
    type: text
    influence_conversation: true
    mappings:
    - type: from_entity
      entity: pizza_type

forms:
  simple_pizza_form:
    required_slots:
      - pizza_size
      - pizza_type

responses:
  utter_pizza_slots:
  - text: I will order a {pizza_size} {pizza_type} pizza.
  utter_ask_pizza_size:
  - text: What size would you like your pizza to be?
  utter_ask_pizza_type:
  - text: What kind of pizza would you like to buy?

actions:
- utter_pizza_slots
- utter_submit
- validate_simple_pizza_form
```

```python
# actions/actions.py

from typing import Text, List, Any, Dict

from rasa_sdk import Tracker, FormValidationAction, Action
from rasa_sdk.events import EventType
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict

ALLOWED_PIZZA_SIZES = ["small", "medium", "large", "extra-large", "extra large", "s", "m", "l", "xl"]
ALLOWED_PIZZA_TYPES = ["mozzarella", "fungi", "veggie", "pepperoni", "hawaii"]

class ValidateSimplePizzaForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_simple_pizza_form"

    def validate_pizza_size(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `pizza_size` value."""

        if slot_value.lower() not in ALLOWED_PIZZA_SIZES:
            dispatcher.utter_message(text=f"We only accept pizza sizes: s/m/l/xl.")
            return {"pizza_size": None}
        dispatcher.utter_message(text=f"OK! You want to have a {slot_value} pizza.")
        return {"pizza_size": slot_value}

    def validate_pizza_type(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `pizza_type` value."""

        if slot_value not in ALLOWED_PIZZA_TYPES:
            dispatcher.utter_message(text=f"I don't recognize that pizza. We serve {'/'.join(ALLOWED_PIZZA_TYPES)}.")
            return {"pizza_type": None}
        dispatcher.utter_message(text=f"OK! You want to have a {slot_value} pizza.")
        return {"pizza_type": slot_value}
```

##### **Custom Forms**
Handle the un-happy path
Approach 1:
```json
user: "I want to buy a pizza."
<rule>
(PIZZA-FORM: active, [ ] pizza-type slot, [ ] pizza-size slot)
bot: "What kind of pizza?"
user: "Are you a bot?"
<rule>
(Handle Chit-Chat)
bot: "I'm a virtual assistant made with Rasa"
<rule>
(PIZZA-FORM: active, [ ] pizza-type slot =veggie, [ ] pizza-size slot)
bot: "What kind of pizza?"
```

To handle it:
```yml
- rule: Interruption in Pizza Form
  condition:
  # Condition that form is active.
  - active_loop: simple_pizza_form
  steps:
  # The case of an intent `bot_challenge`.
  - intent: bot_challenge
  - action: utter_iamabot
  # Return to form
  - action: simple_pizza_form
  - active_loop: simple_pizza_form
```

Approach 2:
```json
user: "I want to buy a pizza."
<rule>
(PIZZA-FORM: active, [ ] pizza-type slot, [ ] pizza-size slot)
bot: "What kind of pizza?"
user: "veggie"
<entity: pizza-type>
(PIZZA-FORM: active, [X] pizza-type slot=veggie, [ ] pizza-size slot)
bot: "What size?"
user: "I've changed my mind, I don't want to buy a pizza."
bot: "Are you sure?"
user: "Yes"
(PIZZA-FORM: inactive, [X] pizza-type slot=veggie, [ ] pizza-size slot)
bot: "OK. What else Can I do for you?"
```

To handle it:
```yml
- story: User doesn't want to continue form
  steps:
  - intent: greet
  - action: utter_greet
  - intent: buy_pizza
  - action: simple_pizza_form
  - active_loop: simple_pizza_form
  - intent: stop
  - action: utter_ask_continue
  - or:
    - intent: stop
	- intent: affirm
  - action: action_deactivate_loop
  - active_loop: null
```

But the problem is either user say "yes" or "no" the action `action_deactivate_loop` always deactivate the loop (rasa only support single step referring to an intent per rule, to prevent rules from getting overused), so we can not use the rules for this case. Let try the stories

```yml
- story: interactive_story_5
  steps:
  - intent: greet
  - action: utter_greet
  - intent: buy_pizza  
  - action: simple_pizza_form
  - active_loop: simple_pizza_form
  - slot_was_set:
	- requested_slot: pizza_size
  - intent: bot_challenge
  - action: utter_iamabot
  - action: simple_pizza_form
  - slot_was_set:
	- requested_slot: pizza_size
  - intent: stop
  - action: utter_ask_continue
  - intent: affirm
  - action: action_deactivate_loop
  - active_loop: null
  - slot_was_set:
	- requested_slot: null
  - intent: goodbye
  - action: utter_goodbye

- story: interactive_story_6
  steps:
  - intent: greet
  - action: utter_greet
  - intent: buy_pizza  
  - action: simple_pizza_form
  - active_loop: simple_pizza_form
  - slot_was_set:
	- requested_slot: pizza_size
  - intent: bot_challenge
  - action: utter_iamabot
  - action: simple_pizza_form
  - slot_was_set:
	- requested_slot: pizza_size
  - intent: stop
  - action: utter_ask_continue
  - intent: deny
  - action: simple_pizza_form
  - ...
```

Approach 3:
```json
bot: "How do you feel?"
user: "Medium. I've been better."
<entity: pizza-size>
(slot =medium)
```

To handle it:
```yml
slots:
  pizza_size:
	type: text
	influence_conversation: true
	mappings:
	  - type: from_entity
	    entity: pizza_size
		conditions:
		- active_loop: pizza_form
		  requested_slot: pizza_size
```

The `conditions` will make the slot capture the entity in the `pizza-form` loop only.

*Making forms dynamic*
Approach 1:
```json
bot: "Would you like to order a vegetarian pizza?"
[button]"yes" [button]"no"
user: "yes"
bot: "What kind of pizza do you want?"
[button]"mozzarella" [button]"fungi" [button]"veggie"
```

Approach 2:
```json
bot: "Would you like to order a vegetarian pizza?"
[button]"yes" [button]"no"
user: "no"
bot: "What kind of pizza do you want?"
[button]"hawaii" [button]"pepperoni"
```

Update Custom Action:
```yml
# domain.yml

forms:
  fancy_pizza_form:
    required_slots:
    - vegetarian
    - pizza_size
    - pizza_type

slots:
  vegetarian:
    type: bool
    influence_conversation: true
    mappings:
    - type: from_intent
      value: true
      intent: affirm
    - type: from_intent
      value: false
      intent: deny
```

```yml
# rules.yml

- rule: Activate Fancy Pizza Form
  steps:
  - intent: buy_fancy_pizza
  - action: fancy_pizza_form
  - active_loop: fancy_pizza_form

- rule: Submit Fancy Pizza Form
  condition:
  - active_loop: fancy_pizza_form
  steps:
  - action: fancy_pizza_form
  - active_loop: null
  - slot_was_set:
    - requested_slot: null
  - action: utter_submit
  - action: utter_pizza_slots
```

```python
# actions/actions.py
...
VEGETARIAN_PIZZAS = ["mozzarella", "fungi", "veggie"]
MEAT_PIZZAS = ["pepperoni", "hawaii"]

...

class AskForVegetarianAction(Action):
    def name(self) -> Text:
        return "action_ask_vegetarian"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        dispatcher.utter_message(
            text="Would you like to order a vegetarian pizza?",
            buttons=[
                {"title": "yes", "payload": "/affirm"},
                {"title": "no", "payload": "/deny"},
            ],
        )
        return []


class AskForPizzaTypeAction(Action):
    def name(self) -> Text:
        return "action_ask_pizza_type"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        if tracker.get_slot("vegetarian"):
            dispatcher.utter_message(
                text=f"What kind of pizza do you want?",
                buttons=[{"title": p, "payload": p} for p in VEGETARIAN_PIZZAS],
            )
        else:
            dispatcher.utter_message(
                text=f"What kind of pizza do you want?",
                buttons=[{"title": p, "payload": p} for p in MEAT_PIZZAS],
            )
        return []


class ValidateFancyPizzaForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_fancy_pizza_form"

    def validate_vegetarian(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `pizza_size` value."""
        if tracker.get_intent_of_latest_message() == "affirm":
            dispatcher.utter_message(
                text="I'll remember you prefer vegetarian."
            )
            return {"vegetarian": True}
        if tracker.get_intent_of_latest_message() == "deny":
            dispatcher.utter_message(
                text="I'll remember that you don't want a vegetarian pizza."
            )
            return {"vegetarian": False}
        dispatcher.utter_message(text="I didn't get that.")
        return {"vegetarian": None}

    def validate_pizza_size(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `pizza_size` value."""

        if slot_value not in ALLOWED_PIZZA_SIZES:
            dispatcher.utter_message(text=f"We only accept pizza sizes: s/m/l/xl.")
            return {"pizza_size": None}
        dispatcher.utter_message(text=f"OK! You want to have a {slot_value} pizza.")
        return {"pizza_size": slot_value}

    def validate_pizza_type(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `pizza_type` value."""

        if slot_value not in ALLOWED_PIZZA_TYPES:
            dispatcher.utter_message(
                text=f"I don't recognize that pizza. We serve {'/'.join(ALLOWED_PIZZA_TYPES)}."
            )
            return {"pizza_type": None}
        if not slot_value:
            dispatcher.utter_message(
                text=f"I don't recognize that pizza. We serve {'/'.join(ALLOWED_PIZZA_TYPES)}."
            )
            return {"pizza_type": None}
        dispatcher.utter_message(text=f"OK! You want to have a {slot_value} pizza.")
        return {"pizza_type": slot_value}
```

##### Integration with a Website
References:
- [https://rasa.com/docs/rasa/http-api/](https://rasa.com/docs/rasa/http-api/)
- [https://rasa.com/docs/rasa/pages/http-api/](https://rasa.com/docs/rasa/pages/http-api/)
- [https://github.com/scalableminds/chatroom](https://github.com/scalableminds/chatroom)
To expose api: `rasa run --enable-api`
Endpoint: `http://localhost:5005/version`

Example with `chatroom.js`
Run chatbot: `rasa run --enable-api --cors="*"`
