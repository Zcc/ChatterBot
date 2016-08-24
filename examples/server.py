from flask import Flask
from chatterbot import ChatBot
app = Flask(__name__)

@app.route('/getresponse/<string:query>', methods=['GET'])
def get_response(query):
    bot = ChatBot("Terminal",
                  storage_adapter="chatterbot.adapters.storage.MongoDatabaseAdapter",
                  logic_adapters=[
                      "chatterbot.adapters.logic.MathematicalEvaluation",
                      "chatterbot.adapters.logic.TimeLogicAdapter",
                      "chatterbot.adapters.logic.ClosestMatchAdapter"
                  ],
                  input_adapter="chatterbot.adapters.input.VariableInputTypeAdapter",
                  output_adapter="chatterbot.adapters.output.TerminalAdapter",
                  database="qatest",
                  read_only=True
                  )
    try:
        bot_response = bot.get_response(query)
        return bot_response
    except (KeyboardInterrupt, EOFError, SystemExit):
        return 'error!'
    return 'Hello, World!'

if __name__ == '__main__':
    app.run()