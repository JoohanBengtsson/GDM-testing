import random
from transformers import pipeline, set_seed
import config


def generate_random_text():
    """ Sets up a text generator for initiating conversations randomly. Returns a randomized string starting with
    start_str """

    # Reads conversation starters from the conv-starters.txt-file and samples one from them randomly.
    with open('miscellaneous .txt-files/conv-starters.txt') as f:
        lines = f.readlines()

    start_str = random.sample(lines, 1)[0].split('\n')[0]
    generator = pipeline('text-generation', model='gpt2')
    generated_response = generator(start_str, max_length=30, num_return_sequences=1)[0]['generated_text']
    generated_response = generated_response.replace("\n", " ")
    return generated_response


def clean_from_excluded_tokens(sentence):
    """ Method for cleansing strings from tokens that are specified to be excluded in the miscellaneous .txt-files/
    excluded_tokens.txt. """
    excluded_tokens = set_of_excluded_tokens()
    for elem in excluded_tokens:
        sentence = sentence.replace(elem, "")
    return sentence


def set_of_excluded_tokens():
    """ Method for reading the excluded tokens that are tokens that should be disregarded. They are specified in
    miscellaneous .txt-files/excluded_tokens.txt. """
    with open('miscellaneous .txt-files/excluded_tokens.txt') as f:
        lines = f.readlines()
    lines = [elem.replace("\n", "") for elem in lines]
    return lines


def count_sentences_within_string(text):
    """ Method for counting how many sentences there are within a text. Based upon the logic that every sentence ends
    with either ".", "!" or "?". """
    amount_sentences = text.count(".") + text.count("!") + text.count("?")
    return amount_sentences


class Conversation:
    """Class for keeping track of a conversation, which includes several messages"""

    def __init__(self, testee, conv_partner, conv_starter=None):
        self.messages = []
        self.whose_turn = ""
        self.testee = testee
        self.conv_partner = conv_partner

        """ Only randomizes conversation start if config.RANDOM_CONV_START is True. """
        if config.RANDOM_CONV_START:
            self.messages.append(Message(generate_random_text(), 'generator', 'generator'))
            print("{}: {}".format('Generated starter', str(self.messages[0])))

        """ If conv_starter is specified from the CLI, conv_starter is not None and the starter is set according to the
            conv_starter. If it is none, it is randomized with 50/50 probability if testee or conv_partner starts. """
        if conv_starter.lower() == "testee":
            self.whose_turn = testee
        elif conv_starter.lower() == "conv_partner":
            self.whose_turn = conv_partner
        elif random.randint(0, 1) == 0:
            self.whose_turn = testee
        else:
            self.whose_turn = conv_partner

    def __getitem__(self, item):
        return self.messages[item]

    def __len__(self):
        return len(self.messages)

    def __iter__(self):
        return iter(self.messages)

    def initiate_conversation(self, conv_length):
        """ Function for running one conversation between testee and conv_partner. The function lets every GDM produce
            conv_length responses with regards to the conversation and last response produced. The messages produced are
            stored in self.messages which is then returned to TestWorld.

        Loops 2 * conv_length response requests, where each turn self.whos_turn produces the response and then
                self.whos_turn is switched to the other conversation partner. """
        for i in range(2 * conv_length):
            message = self.produce_message()
            self.messages.append(message)
            self.switch_turn()
        return self

    def produce_message(self, injected_sent=None):
        """ Function for producing one message from whos_turn. If injected_sent is not None, then that string may
        override the normal generate response procedure, and take its place."""

        if injected_sent is not None:
            message = Message(message=injected_sent, agent_id=self.whose_turn.get_id(), role=self.whose_turn.get_role())
        else:
            message = Message(self.whose_turn.act(self.str_conversation()), self.whose_turn.get_id(),
                              role=self.whose_turn.get_role())
        print("{}: {}".format(self.whose_turn.get_role(), str(message))) if config.VERBOSE else print()
        return message

    def switch_turn(self):
        """ Function for switching the turn to the agent that did not produce the last response. """
        self.whose_turn = self.testee if self.whose_turn.get_role() == self.conv_partner.get_role() \
            else self.conv_partner

    def str_conversation(self):
        """ Method for converting the list of Messages into a list of strings, so that it is printable. """
        stringified_messages = []
        for elem in self.messages:
            stringified_messages.append(str(elem))
        return stringified_messages

    def get_messages(self):
        """ Returns list of messages. """
        return self.messages

    def conv_from_file(self, lines):
        """ Work in progress. """
        for i in range(len(lines)):
            self.messages[i] = lines[i]

    def get_testee_id(self):
        """ Returns the ID of the testee for self (the Conversation-object self). """
        return self.testee.get_id()

    def filter_testee_mgs(self):
        """ Method for converting the list of Messages into a stringifed list of only the messages belonging to the
        Testee, as to evaluate only these messages, should it be necessary. """
        stringified_messages = []
        for message in self.messages:
            if message.get_role() == "Testee":
                stringified_messages.append(str(message))
        return stringified_messages


class Message:
    """ Class for controlling the properties of every Message"""

    def __init__(self, message, agent_id, role):
        self.message = message
        self.agent_id = agent_id
        self.role = role

    def belongs_to(self, agent_id):
        """ Function for checking if a message belongs to the specific agent_id brought as a parameter. """
        return agent_id == self.agent_id

    def __str__(self):
        """ Stringifies a message. That is, it turns a Message into a printable string. """
        return self.message

    def get_role(self):
        """ Function for returning the role of the GDM who produced self. Returns either 'Testee' or 'Other agent'. """
        return self.role
