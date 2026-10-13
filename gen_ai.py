from google import genai

client = genai.Client(api_key="AQ.Ab8RN6L6RAmvAf2LYSk01_JNA9IlA9kYl8L-3PhgElm-4a8UEQ")

interaction = client.interactions.create(
    model="gemini-3.8-flash",

    input="Explain how AI works in a few words"
)

print(interaction.output_text)
