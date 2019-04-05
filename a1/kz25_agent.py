from re import *


def introduce():
    return("My name is Dale Vandermeer, and I am a college advisor. \n"
           "I was programmed Keyi Zhong. If you don't like the way I talk \n"
           "please contact him at kz25@uw.edu. \n"
           "How can I help you?\n")

college_name = null

def respond(the_input):
    wordlist = split(' ', the_input)
    wordlist[0] = wordlist[0].lower();

    if match('bye', the_input):
        return 'Goodbye'
    if wordlist[0:1] == ['can', 'you'] or wordlist[0:2]==['could','you']:
        return 'Yes I ' + wordlist[0] + ' '.join(wordlist[2:]) + '.'
    if 'college' in wordlist:

        return collegeSentence()

    return uselessSentence();


7
def agentName():
    return 'Vandermeer'


ueless_count = 0
def uselessSentence():
    sentence = ['Please be more specific',
                'Being in a college is not easy.',
                'Someimes you need to be patient.',
                'Always be hopeful to the future.',
                ]


college_count = 0
def collegeSentence():
    sentence = ['It is always hard to get to a college.']