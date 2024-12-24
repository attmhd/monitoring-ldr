from fastapi import FastAPI, Form, HTTPException
import mysql.connector
from pydantic import BaseModel


# Initialize the FastAPI app
app = FastAPI()


# Database connection helper function
def get_db_connection():
    """Establish a connection to the MySQL database."""
    return mysql.connector.connect(
        host="localhost",       # Replace with your MySQL host
        user="root",            # Replace with your MySQL username
        password="",            # Replace with your MySQL password
        database="sensor_ldr"   # Replace with the name of your MySQL database
    )


# Pydantic model for LDR data
class LDRData(BaseModel):
    ldr_value: float


# Function to insert LDR data into the database
def insert_ldr_data_to_db(ldr_value: float):
    """Insert the LDR data value into the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO ldr_data (ldr_value) VALUES (%s)", (ldr_value,))
    conn.commit()
    cursor.close()
    conn.close()


# Endpoint to insert LDR data
@app.post("/insert_data")
async def insert_data(ldr_value: float = Form(...)):
    """Insert LDR data into the database and return a success message."""
    try:
        insert_ldr_data_to_db(ldr_value)
        return {"message": "Data inserted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inserting data: {e}")


# Function to retrieve all LDR data from the database
def get_all_ldr_data():
    """Fetch all LDR data from the database."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM ldr_data")
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result


# Endpoint to get all LDR data
@app.get("/get_data")
async def get_data():
    """Retrieve LDR data from the database."""
    try:
        result = get_all_ldr_data()
        if not result:
            raise HTTPException(status_code=404, detail="No data found")
        return {"result": result}
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"MySQL error: {err}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Main execution
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)
