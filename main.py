from google import genai

client = genai.Client()

chat = client.chats.create(
    model="gemini-3-flash-preview"
)

text = None

try:
    with open("story.txt" , "r") as file:
        text = file.read()
        
    chat.send_message(f"here is a document {text}")

    while True:
        user_que = input("Enter Question : ").lower()

        if user_que == "exit":
            break

        response = chat.send_message(f"Answer This {user_que}")

        print(response.text)
    
except FileNotFoundError:
    print("File not Found ! maybe check the filename")





