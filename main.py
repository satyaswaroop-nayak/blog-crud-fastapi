from fastapi import FastAPI


app = FastAPI()

@app.get("/")
def getSomething():
    return {"data":"sometging"}