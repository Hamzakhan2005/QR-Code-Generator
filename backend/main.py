from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import qrcode
from io import BytesIO
import base64
from pydantic import BaseModel

app = FastAPI(title="QR Code Generator API")

# CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QRRequest(BaseModel):
    text: str
    format: str = "png"  # png, jpg, svg
    size: int = 10  # QR code size (1-40)

@app.get("/")
def root():
    return {"message": "QR Code Generator API", "version": "1.0"}

@app.get("/generate_qr")
def generate_qr_get(text: str, format: str = "png", size: int = 10):
    """Generate QR code via GET request"""
    if not text or len(text.strip()) == 0:
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    if size < 1 or size > 40:
        raise HTTPException(status_code=400, detail="Size must be between 1 and 40")
    
    try:
        # Create QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=size,
            border=4,
        )
        qr.add_data(text)
        qr.make(fit=True)
        
        # Generate image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to bytes
        buf = BytesIO()
        img.save(buf, format=format.upper())
        buf.seek(0)
        
        # Return as streaming response
        media_type = f"image/{format.lower()}"
        return StreamingResponse(buf, media_type=media_type)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating QR code: {str(e)}")

@app.post("/generate_qr")
def generate_qr_post(request: QRRequest):
    """Generate QR code via POST request and return base64"""
    if not request.text or len(request.text.strip()) == 0:
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    if request.size < 1 or request.size > 40:
        raise HTTPException(status_code=400, detail="Size must be between 1 and 40")
    
    try:
        # Create QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=request.size,
            border=4,
        )
        qr.add_data(request.text)
        qr.make(fit=True)
        
        # Generate image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to base64
        buf = BytesIO()
        img.save(buf, format=request.format.upper())
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode()
        
        return {
            "success": True,
            "image": f"data:image/{request.format.lower()};base64,{img_base64}",
            "format": request.format,
            "text": request.text
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating QR code: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)