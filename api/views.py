from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from pypdf import PdfReader 
from openai import OpenAI
l =[]
client = OpenAI()
@api_view(['POST'])
def checksys(request):
    s = ""
    if request.data.get("clear"):
        l.clear()
        return Response({"message":"history cleared"}) 
    
    if not l and request.data.get("SysMsg"):
        l.append({"role": "system", "content": request.data.get("SysMsg")})
    
    if request.data.get('file'):
        datainfile = ""
        files = request.FILES['file']
        reader = PdfReader(files)
        print(len(reader.pages))
        print(files)
        for page in reader.pages:
            datainfile = datainfile+page.extract_text()
        if request.data.get("prompt"):
            s = request.data.get("prompt")+" "+datainfile
    elif request.data.get("prompt"):
            s = request.data.get("prompt")
    l.append({"role": "user", "content": s})
    print(l)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=l
    )
    l.append({"role": "assistant", "content": response.choices[0].message.content})
    print(l)
    return Response({"message":response.choices[0].message.content}) 


# Create your views here.
