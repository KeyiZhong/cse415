from re import *
import random


def introduce():
    return("My name is Dale Vandermeer, I am a college advisor. \n"
           "I was programmed by Keyi Zhong. If you don't like the way I talk \n"
           "please contact him at kz25@uw.edu. \n"
           "How can I help you?\n")


class College:
    college_list = []

    def __init__(self):
        self.college_list = []

    def add_college(self, name):
        self.college_list = self.college_list + [name]

    def recall(self):
        return self.college_list


college_list = College()


def respond(the_input):
    wordlist = split(' ', the_input)
    wordlist[0] = wordlist[0].lower()
    mapped_wordlist = you_me_map(wordlist)
    mapped_wordlist[0] = mapped_wordlist[0].capitalize()

    if match('bye', the_input):
        return 'Goodbye'
    if match('hi', the_input):
        return 'Hello this is Dale Vandermeer'
    if 'Good morning' in the_input:
        return 'Good morning, this is Dale Vandermeer, how can I help you?'
    if wordlist[0] == '':
        return "Please make some noise."
    if 'major' in wordlist:
        return collegeSentence()
    if 'college' in wordlist or 'university' in wordlist and len(wordlist) <= 3:
        college_list.add_college(stringify(wordlist))
        return collegeSentence()
    if 'college' in wordlist or 'university' in wordlist:
        return 'Please specify the name of university/college.'
    if 'suggestion' in wordlist or 'advice' in wordlist:
        if len(college_list.recall()) == 0:
            return 'please tell me what college is in your mind.'
        return random.choice(college_list.recall()) + ' would be a good choice!'
    if wordlist[0:2] == ['i', 'am']:
        return "Tell me why and when you are " +\
              stringify(mapped_wordlist[2:])
    if wpred(wordlist[0]):
        return "There is no exact " + wordlist[0]
    if 'because' in wordlist:
        return "Please reconsider this carefully."
    if 'yes' in wordlist:
        return "Are you really sure?"
    if wordlist[0:2] == ['you', 'are']:
        return "I am truly " +\
              stringify(mapped_wordlist[2:])
    if verbp(wordlist[0]):
        return"I will " + stringify(mapped_wordlist) + ' if I have time.'
    if wordlist[0:3] == ['do', 'you', 'think']:
        return "I don't know, but I am more interested in your opinion."
    if wordlist[0:2] == ['can', 'you'] or wordlist[0:2] == ['could', 'you']:
        return 'Yes I ' + wordlist[0] + ' ' + stringify(mapped_wordlist[2:])
    if 'maybe' in the_input:
        return random.choice(['Please be sure.',
                              'Do not hesitate',
                              'Give a hit',
                              'Come on'])
    if 'good' in the_input:
        return random.choice(['Tell me what is good about it',
                             'I would like to hear about it',
                              'What make you think this way',
                              'Nice!'])
    if 'name' in wordlist[-1]:
        return 'My name is Dale Vandermeer'
    ##if 'you' in mapped_wordlist or 'You' in mapped_wordlist:
        ##return stringify(mapped_wordlist)
    return uselessSentence()


def agentName():
    return 'Vandermeer'


useless_count = -1


def uselessSentence():
    sentence = ['Please be more specific',
                'Please tell me more about it',
                'I know right',
                'Please continue',
                'Keep going',
                'Good for you',
                'Cool',
                'I like your jacket',
                'Let me think about it and I will let you know when I figure it out',
                'You really get to the point where I cannot answer',
                'Cheer up dude!',
                'You won',
                'What do you want',
                'Please ask a more related question.'
                ]
    global useless_count
    useless_count += 1
    return sentence[useless_count % len(sentence)]


college_count = -1


def collegeSentence():
    sentence = ['It is always hard to get to a college.',
                'It is hard to get to a major',
                'Always be hopeful to the future.',
                'Being in a college is not easy.',
                'Sometimes you need to be patient.',
                'Enjoy your college life']
    global college_count
    college_count += 1
    return sentence[college_count % len(sentence)]


def stringify(wordlist):
    'Create a string from wordlist, but with spaces between words.'
    return ' '.join(wordlist)


def wpred(w):
    'Returns True if w is one of the question words.'
    return w in ['when','why','where','how']


def dpred(w):
    'Returns True if w is an auxiliary verb.'
    return w in ['do','can','should','would']


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


def verbp(w):
    'Returns True if w is one of these known verbs.'
    return (w in ['go', 'have', 'be', 'try', 'eat', 'take', 'help',
                  'make', 'get', 'jump', 'write', 'type', 'fill',
                  'put', 'turn', 'compute', 'think', 'drink',
                  'blink', 'crash', 'crunch', 'add'])


#print(introduce())
#while True:
#    the_input = input()
#    print(respond(the_input))
#    if 'bye' in the_input:
#        break