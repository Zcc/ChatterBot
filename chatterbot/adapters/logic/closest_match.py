# -*- coding: utf-8 -*-
from .base_match import BaseMatchAdapter
from fuzzywuzzy import fuzz
import copy
from chatterbot.conversation import Statement

class ClosestMatchAdapter(BaseMatchAdapter):
    """
    The ClosestMatchAdapter creates a response by
    using fuzzywuzzy's process class to extract the most similar
    response to the input. This adapter selects a response to an
    input statement by selecting the closest known matching
    statement based on the Levenshtein Distance between the text
    of each statement.
    """


    def get(self, input_statement):
        """
        Takes a statement string and a list of statement strings.
        Returns the closest matching statement from the list.
        """
        if len(self.statement_list) == 0:
            print("loading data.....")
            self.statement_list = self.context.storage.get_response_statements()
        if not self.statement_list:
            if self.has_storage_context:
                # Use a randomly picked statement
                return 0, self.context.storage.get_random()
            else:
                raise self.EmptyDatasetException()

        confidence = -1
        closest_match = input_statement

        # Find the closest matching known statement
        for statement in self.statement_list:
            ratio = fuzz.ratio(str(input_statement.text), str(statement['text']))

            if ratio > confidence:
                confidence = ratio
                closest_match = statement

        '''
        closest_match, confidence = process.extractOne(
            input_statement.text,
            text_of_all_statements
        )
        '''
        values = copy.deepcopy(closest_match)
        # print(values)
        statement_text = values['text']

        del (values['text'])
        # Convert the confidence integer to a percent
        confidence /= 100.0
        print(str(self.__class__).split('.')[-1][:-2], confidence, statement_text)
        return confidence, Statement(statement_text, **values)

