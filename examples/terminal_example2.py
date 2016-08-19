from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

# Create a new instance of a ChatBot
bot = ChatBot("Terminal",
              storage_adapter="chatterbot.adapters.storage.MongoDatabaseAdapter",
              logic_adapters=[
                  "chatterbot.adapters.logic.MathematicalEvaluation",
                  "chatterbot.adapters.logic.TimeLogicAdapter",
                  "chatterbot.adapters.logic.ClosestMatchAdapter"
              ],
              input_adapter="chatterbot.adapters.input.TerminalAdapter",
              output_adapter="chatterbot.adapters.output.TerminalAdapter",
              database="qatest",
              read_only=True
              )
#bot.set_trainer(ChatterBotCorpusTrainer)
# 使用中文语料库训练它
#bot.train("chatterbot.corpus.test")  # 语料库
print("Type something to begin...")

# The following loop will execute each time the user enters input
while True:
    try:
        # We pass None to this method because the parameter
        # is not used by the TerminalAdapter
        bot_input = bot.get_response(None)

    # Press ctrl-c or ctrl-d on the keyboard to exit
    except (KeyboardInterrupt, EOFError, SystemExit):
        break
