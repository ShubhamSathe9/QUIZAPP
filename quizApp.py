import requests
import random
import html


# ------------------ COLORS ------------------ #
class Color:
    GREEN = "\033[92m"
    RED = "\033[91m"
    CYAN = "\033[96m"
    YELLOW = "\033[93m"
    BOLD = "\033[1m"
    END = "\033[0m"


# ------------------ QUIZ SETTINGS ------------------ #
class QuizSettings:

    @staticmethod
    def menu():
        while True:
            print("\n" + "-" * 60)
            print(Color.CYAN + Color.BOLD + "          *** WELCOME TO QUIZ APP ***" + Color.END)
            print("-" * 60)

            print("1) Start Quiz")
            print("2) How to Play")
            print("3) Quit\n")

            try:
                choice = int(input("Enter your choice (1–3): "))
                if choice in [1, 2, 3]:
                    return choice
                print(Color.RED + "❌ Please choose 1, 2, or 3." + Color.END)
            except ValueError:
                print(Color.RED + "❌ Invalid input! Only numbers allowed." + Color.END)

    @staticmethod
    def show_categories():
        print("\n📚 Categories:")
        print("----------------------------")
        print(" 9  : General Knowledge")
        print("10  : Books")
        print("11  : Film")
        print("12  : Music")
        print("13  : Musicals & Theatre")
        print("14  : Television")
        print("15  : Video Games")
        print("16  : Board Games")
        print("17  : Science & Nature")
        print("18  : Science: Computers")
        print("19  : Science: Mathematics")
        print("20  : Mythology")
        print("21  : Sports")
        print("22  : Geography")
        print("23  : History")
        print("24  : Politics")
        print("25  : Art")
        print("26  : Celebrities")
        print("27  : Animals")
        print("28  : Vehicles")
        print("29  : Comics")
        print("30  : Gadgets")
        print("31  : Anime & Manga")
        print("32  : Cartoons & Animation")

    @staticmethod
    def UserInput():

        # -------- AMOUNT -------- #
        while True:
            try:
                amount = int(input("\nHow many questions? : "))
                if amount > 0:
                    break
                print(Color.RED + "❌ Enter a positive number!" + Color.END)
            except ValueError:
                print(Color.RED + "❌ Only numbers allowed!" + Color.END)

        # -------- CATEGORY -------- #
        QuizSettings.show_categories()

        valid_categories = set(range(9, 33))

        while True:
            try:
                category = int(input("Enter Category ID: "))
                if category in valid_categories:
                    break
                print(Color.RED + "❌ Invalid category ID! Choose from list." + Color.END)
            except ValueError:
                print(Color.RED + "❌ Only numbers allowed!" + Color.END)

        # -------- DIFFICULTY -------- #
        while True:
            difficulty = input("Difficulty (easy/medium/hard): ").lower()
            if difficulty in ["easy", "medium", "hard"]:
                break
            print(Color.RED + "❌ Please choose: easy / medium / hard" + Color.END)

        return {
            "amount": amount,
            "category": category,
            "difficulty": difficulty,
            "type": "multiple"
        }


# ------------------ QUIZ ENGINE ------------------ #
class QuizEngine:

    def __init__(self, settings):
        self.amount = settings["amount"]
        self.category = settings["category"]
        self.difficulty = settings["difficulty"]
        self.qtype = settings["type"]
        self.questions = []

    def build_url(self):
        return (
            f"https://opentdb.com/api.php?amount={self.amount}"
            f"&category={self.category}"
            f"&difficulty={self.difficulty}"
            f"&type={self.qtype}"
        )

    def fetch_questions(self):
        try:
            response = requests.get(self.build_url(), timeout=5)
            data = response.json()

            if data["response_code"] != 0:
                print(Color.RED + "❌ API Error: No questions available!" + Color.END)
                return False

            self.questions = data["results"]
            return True

        except Exception as e:
            print(Color.RED + f"❌ Network error: {e}" + Color.END)
            return False

    def start_quiz(self):
        score = 0

        for idx, q in enumerate(self.questions, start=1):

            question = html.unescape(q["question"])
            correct = html.unescape(q["correct_answer"])
            incorrect = [html.unescape(i) for i in q["incorrect_answers"]]

            options = incorrect + [correct]
            random.shuffle(options)

            print(f"\n{Color.CYAN}Q{idx}: {question}{Color.END}")
            print("--------------------------------")

            for i, opt in enumerate(options, start=1):
                print(f"{i}) {opt}")

            # -------- SAFE ANSWER INPUT -------- #
            while True:
                try:
                    ans = int(input("\nYour answer (1–4): "))
                    if 1 <= ans <= 4:
                        selected = options[ans - 1]
                        break
                    print(Color.RED + "❌ Choose between 1 and 4 only!" + Color.END)
                except ValueError:
                    print(Color.RED + "❌ Only numbers allowed!" + Color.END)

            if selected == correct:
                print(Color.GREEN + "✔ Correct!" + Color.END)
                score += 1
            else:
                print(Color.RED + f"✘ Wrong! Correct was: {correct}" + Color.END)

        print("\n" + "-" * 40)
        print(Color.BOLD + f"🏁 FINAL SCORE: {score}/{len(self.questions)}" + Color.END)
        print("-" * 40)


# ------------------ MAIN LOOP ------------------ #
while True:
    choice = QuizSettings.menu()

    if choice == 1:
        settings = QuizSettings.UserInput()
        engine = QuizEngine(settings)

        if engine.fetch_questions():
            engine.start_quiz()

    elif choice == 2:
        print("\n📘 HOW TO PLAY:")
        print("- Choose number of questions")
        print("- Select category & difficulty")
        print("- Answer questions (1–4)")
        print("- Score shown at end\n")

    elif choice == 3:
        print("\n👋 Thank you for playing!\n")
        break