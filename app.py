from rag.retriever import get_retriever
from llm.gemini import ask_gemini
from voice.text_to_speech import speak
from voice.speech_to_text import listen

retriever = get_retriever()

print("=" * 60)
print("🏥 EMMA - AI Healthcare Voice Receptionist")
print("=" * 60)

while True:

    mode = input("\nChoose Mode:\n1. Voice\n2. Text\n3. Exit\n\nEnter choice: ")

    if mode == "3":
        break

    elif mode == "1":
        question = listen()

        if question is None:
            continue

    elif mode == "2":
        question = input("\nEnter your medical question: ")

    else:
        print("Invalid choice.")
        continue

    docs = retriever.invoke(question)

    context = "\n\n".join(doc.page_content for doc in docs)

    answer = ask_gemini(context, question)

    print("\n🤖 EMMA:\n")
    print(answer)

    speak(answer)