from search_graph import BenimAI

if __name__ == "__main__":
    ai = BenimAI()
    graph = ai.AIBuilder()
    while True:
        user_input = input("lütfen arayacağınız girdiyi giriniz: ")
        ai.chat_with_ai(prompt = user_input,graph = graph).pretty_print()