from al_dialog_engine import AlDialogEngine

engine = AlDialogEngine(path="../testDialogFileForPractice.txt")

def main():
    question: str = "deep test"
    question2 : str = "go deeper"
    question3 : str = "go deeper"
    question4: str = "go deeper"

    question_words = question.lower().split()
    question_words2 = question2.lower().split()
    question_words3 = question3.lower().split()
    question_words4 = question4.lower().split()

    actions, response = engine.get_response(question_words)
    print(response)
    actions, response = engine.get_response(question_words2)
    print(response)
    actions, response = engine.get_response(question_words3)
    print(response)
    actions, response = engine.get_response(question_words4)
    print(response)
    actions, response = engine.get_response(question_words4)
    print(response)
    actions, response = engine.get_response(question_words4)
    print(response)

if __name__ == '__main__':
    main()