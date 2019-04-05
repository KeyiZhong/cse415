from re import *


def introduce():
    return("My name is Dale Vandermeer, and I am a college advisor. \n"
           "I was programmed Keyi Zhong. If you don't like the way I talk \n"
           "please contact him at kz25@uw.edu. \n"
           "How can I help you?\n")


def respond(the_input):
    wordlist = split(' ', the_input)
    wordlist[0] = wordlist[0].lower();

    if match('bye', the_input):
        return 'Goodbye'
    if wordlist[0:1] == ['can', 'you'] or wordlist[0:2]==['could','you']:
        return
    return uselessSentence();



def agentName():
    return 'Vandermeer'


def uselessSentence():
    sentence = ['']
