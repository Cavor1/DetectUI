from types import resolve_bases
from ollama import chat, ChatResponse

response : ChatResponse = chat(model = 'llava-phi3:3.8b', messages = [
    {
        'role':'user',
        'content':'whats on the image?',
        'images':['./test.png']
    }
])

print(response.message.content)
