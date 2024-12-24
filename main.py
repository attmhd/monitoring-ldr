from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse
import mysql.connector
from pydantic import BaseModel
from typing import Optional

# Inisialisasi aplikasi FastAPI
app = FastAPI()

# Koneksi ke database MySQL
def db_connection():
    return mysql.connector.connect(
        host="localhost",       # Ganti dengan host MySQL
        user="root",            # Ganti dengan username MySQL Anda
        password="",    # Ganti dengan password MySQL Anda
        database="sensor_ldr"  # Nama database yang akan digunakan
    )

# Model untuk menerima data LDR
class LDRData(BaseModel):
    ldr_value: float

# Endpoint untuk menerima data LDR dan menyimpannya ke MySQL
@app.post("/insert_data")
async def insert_data(ldr_value: float = Form(...)):
    # Menyimpan data LDR ke database
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO ldr_data (ldr_value) VALUES (%s)", (ldr_value,))
    conn.commit()
    cursor.close()
    conn.close()
    
    return {"message": "Data inserted successfully"}

# Endpoint untuk menampilkan data LDR
@app.get("/get_data")
async def get_data():
    # Mengambil data LDR dari database
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ldr_data")
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return JSONResponse(content=result)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
