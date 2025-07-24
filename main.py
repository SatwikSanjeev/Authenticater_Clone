from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import pyotp, qrcode
import io, base64
import time

app = FastAPI()
templates = Jinja2Templates(directory="templates")

app = FastAPI()

# Serve static files from the "static" folder
app.mount("/static", StaticFiles(directory="static"), name="static")


secret = pyotp.random_base32()
totp = pyotp.TOTP(secret)
uri = totp.provisioning_uri(name="user@example.com", issuer_name="WebTOTPApp")

def generate_qr():
    img = qrcode.make(uri)
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    return base64.b64encode(buf.getvalue()).decode("utf-8")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    otp = totp.now()
    qr_code = generate_qr()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "otp": otp,
        "qr": qr_code,
        "remaining": 30 - int(time.time()) % 30
    })
