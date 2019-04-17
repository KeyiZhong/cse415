from re import *   # Loads the regular expression module.

def introduce():
    return "Hello! \n"\
            "My name is Nina Tea, and I sell tea! \n"\
            "I was programmed by Yvonne Lai. \n"\
            "If you can't find the tea you want, it's not my fault but hers! \n"\
            "You can contact her at hlai98@uw.edu. \n"\
            "How can I help you?"

def agentName():
    return "Nina"

class Name:
    result =""

    def __init__(self):
        self.result = ""

    def add_name(self, input_name):
        self.result = self.result + input_name

    def recall(self):
        return self.result

result = Name()

class Order:
    order_list =""

    def __init__(self):
        self.order_list = ""

    def add_order(self, order):
        self.order_list = self.order_list + order

    def recall(self):
        return self.order_list

order_list = Order()

def respond(the_input):
    wordlist = split(' ', remove_punctuation(the_input))
    wordlist[0] = wordlist[0].lower()
    mapped_wordlist = you_me_map(wordlist)
    mapped_wordlist[0] = mapped_wordlist[0].capitalize()
    if wordlist[0:3] == ["my", "name", "is"]:
        name = wordlist[3]
        result.add_name(name)
        return "Hello, " + name + ". " + "What do you want to drink today?"
    if wordlist[0] == '':
        return "Please say something!"
    if 'where' in wordlist and 'pick' in wordlist and 'up' in wordlist:
        return "You can pick it up here!"
    if 'tea' in wordlist and \
            ('black' in wordlist or 'oolong' in wordlist or 'green' in wordlist or
            'herbal' in wordlist or 'yellow' in wordlist or 'white' in wordlist) == False:
        if 'tea' not in order_list.recall():
            order_list.add_order(" tea")
        return "What tea base do you want?"
    if 'tea' in wordlist and ('black' in wordlist or 'oolong' in wordlist or 'green' in wordlist or
            'herbal' in wordlist or 'yellow' in wordlist or 'white' in wordlist) == True:
        if 'black'in wordlist and 'black' not in order_list.recall():
            order_list.add_order(" black")
        if 'yellow'in wordlist and 'yellow' not in order_list.recall():
            order_list.add_order(" yellow")
        if 'oolong'in wordlist and 'oolong' not in order_list.recall():
            order_list.add_order(" oolong")
        if 'green'in wordlist and 'green' not in order_list.recall():
            order_list.add_order(" green")
        if 'herbal'in wordlist and 'herbal' not in order_list.recall():
            order_list.add_order(" herbal")
        if 'white'in wordlist and 'white' not in order_list.recall():
            order_list.add_order(" white")
        if 'tea' not in order_list.recall():
            order_list.add_order(" tea")
        return "Ok I got it! Anything else?"
    if match('bye', the_input):
        return 'Goodbye!'
    if match('hi', the_input) or match('hello', the_input):
        return greeting()
    if wordlist[0:2] == ['i','want']:
        return "Are you sure you want " +\
              stringify(wordlist[2:]) + '?'
    if 'sure' in wordlist:
        return "Ok I got it! You can perhaps finish your order."
    if wordlist[0:2] == ['you','are']:
        return "Oh yeah, I am " +\
              stringify(wordlist[2:]) + '!'
    if 'recommendation' in wordlist:
        return "I like Oolong tea. It is really good!!!"
    if 'hot' in wordlist:
        if 'hot' not in order_list.recall() and 'cold' not in order_list.recall():
            order_list.add_order(" hot")
        return "There is a 15 minute wait for the hot drinks."
    if 'cold' in wordlist:
        if 'hot' not in order_list.recall() and 'cold' not in order_list.recall():
            order_list.add_order(" cold")
        return "Cold tea is really good!"
    if 'finish' in wordlist or 'done' in wordlist:
        if result.recall() == "":
            return 'Please tell me your name.'
        if order_list.recall() == "" or 'tea' not in order_list.recall():
            return 'Please tell me what you want so I can place your order.'
        return "Ok, " + result.recall() + ", I got your order as" + order_list.recall() + "."\
                " You can pick it up later."
    if 'promotion' in wordlist or "cheaper" in wordlist:
        return promotion()
    #if 'you' in mapped_wordlist or 'You' in mapped_wordlist:
     #   return stringify(mapped_wordlist) + '.'
    if wordlist[0:2]==['can','you'] or wordlist[0:2]==['could','you']:
        return "Off course I " + wordlist[0] + ' ' +\
             stringify(mapped_wordlist[2:]) + '. Customers are always right!'
    if wordlist[0] == "ok":
        return 'Oh, I am sorry. All teas just sold out'
    if match('no', the_input):
        return 'Ok. I am sorry. I cannot process your order right now.'
    return punt()

promotion_option = ['Buy one get two free!',
                    'Buy two get five free!',
                    "50 percent off!"]
promotion_count=0
def promotion():
    global promotion_count
    promotion_count += 1
    return promotion_option[promotion_count % 3]

greeting_option = ["Hi, this is Nina. What can I get for yuo today?",
                   "Good to see you here. How can I help you today?",
                   "Hello! This is Nina. What is your name?",
                   "Hello! Can you tell me your name?"]
greeting_count=0
def greeting():
    global greeting_count
    greeting_count += 1
    return greeting_option[greeting_count % 4]

punctuation_pattern = compile(r"\,|\.|\?|\!|\;|\:")

def remove_punctuation(text):
    'Returns a string without any punctuation.'
    return sub(punctuation_pattern,'', text)

def stringify(wordlist):
    return ' '.join(wordlist)

PUNTS = ['Please tell me what you want.',
         'Do you want any tea to drink?',
         'Our tea is very good!',
         'Just tell me what you want.',
         'We do not sell that here.',
         'I like Oolong milk tea.',
         'Can you tell me what you want?',
         'What tea would you like?',
         'We only have tea here.',
         'Our tea is the best.',
         'Tea is good for your health.',
         'White tea is very special.',
         'Our signature tea is Oolong tea.',
         'Tell me your order please. We will close soon.',
         'Are you here to order tea?',
         "We take tea orders."]

punt_count=0
def punt():
    global punt_count
    punt_count += 1
    return PUNTS[punt_count % 6]

CASE_MAP = {'i':'you', 'I':'you', 'me':'you','you':'me',
            'my':'your','your':'my',
            'yours':'mine','mine':'yours','am':'are'}

def you_me(w):
    'Changes a word from 1st to 2nd person or vice-versa.'
    try:
        result = CASE_MAP[w]
    except KeyError:
        result = w
    return result

def you_me_map(wordlist):
    'Applies YOU-ME to a whole sentence or phrase.'
    return [you_me(w) for w in wordlist]

