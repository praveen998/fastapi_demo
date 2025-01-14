from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from fastapi.responses import HTMLResponse
from fastapi.responses import FileResponse
import os

app=FastAPI()


#return json response-------------------------
@app.get("/")
def home():
    return {"hello":"world"}

#return plaintext response--------------------
@app.get("/plaintext",response_class=PlainTextResponse)
def plaintext():
    return "Hello world"


#return html response-------------------------
@app.get("/htmltext",response_class=HTMLResponse)
def htmltext():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>FastAPI HTML Response</title>
    </head>
    <body>
        <h1>Hello, World!</h1>
        <p>This is an example of returning HTML from FastAPI.</p>
    </body>
    </html>
    """
    return html_content

@app.get("/media")
def getmedia():
    file_path="media/kali-linux-3840x2160-18058.jpg"
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return {"error":"file not found"}
