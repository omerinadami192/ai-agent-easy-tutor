from konusmaai import talk_with_gpt

if __name__ == "__main__":
    model_name = input("konuşmak istediğiniz modeli giriniz: ")
    while True:
        user_prompt = input("Lütfen bir girdi giriniz: ")
        print(talk_with_gpt(prompt = user_prompt, model_name = model_name))
