import traceback
import gradio as gr

from rag.retriever import get_retriever
from llm.gemini import ask_gemini
from voice.text_to_speech import speak
from voice.speech_to_text import transcribe

retriever = get_retriever()


def healthcare_chat(text_question, audio_file):

    print("=" * 60)
    print("Function Called")
    print("Text Question:", text_question)
    print("Audio File:", audio_file)
    print("=" * 60)

    try:

        # Decide whether to use typed text or microphone
        if audio_file is not None:
            print("🎤 Using microphone input...")
            question = transcribe(audio_file)
            print("Transcribed Question:", question)
        else:
            print("⌨️ Using text input...")
            question = text_question

        if not question:
            return "Please type a question or record your voice."

        print("Searching Vector Database...")

        docs = retriever.invoke(question)

        context = "\n\n".join(
            [doc.page_content for doc in docs]
        )

        print("Calling Gemini...")

        answer = ask_gemini(context, question)

        print("Gemini Response:")
        print(answer)

        print("Speaking...")

        speak(answer)

        print("Completed Successfully!")

        return f"""👤 You:
{question}

----------------------------

🤖 EMMA:

{answer}
"""

    except Exception as e:

        print("\n\nERROR OCCURRED\n")
        traceback.print_exc()

        return f"ERROR:\n\n{str(e)}"


demo = gr.Interface(
    fn=healthcare_chat,

    inputs=[
        gr.Textbox(
            label="Type your medical question"
        ),

        gr.Audio(
            sources=["microphone"],
            type="filepath",
            label="🎤 Or Speak"
        )
    ],

    outputs=gr.Textbox(
        label="AI Response",
        lines=15
    ),

    title="🏥 AI Healthcare Voice Receptionist",

    description="""
Type your symptoms OR click the microphone and speak.

The AI will:
1. Listen
2. Search the medical knowledge base
3. Generate an answer using Gemini
4. Speak the answer aloud
"""
)

demo.launch(debug=True)