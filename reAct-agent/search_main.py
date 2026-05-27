from search_graph import BenimAI

if __name__ == "__main__":
    ai = BenimAI()
    graph = ai.AIBuilder()
    chat = True
    while chat:
        try:
            user_input = input("lütfen arayacağınız girdiyi giriniz: ")
            ai.chat_with_ai(prompt = user_input,graph = graph).pretty_print()
        except Exception as e:
            print(f"Main konuşma hatası: {e}")
            user_input = input("lütfen tekrar denecek mi yazınız(evet, hayır): ")
            if user_input == "hayır":
                chat = False