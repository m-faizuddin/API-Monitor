from fastapi import FastAPI
from database import create_tables


app = FastAPI() #This line creates an instance of the FastAPI class and assigns it to the variable app. The FastAPI class is the main entry point for creating a FastAPI application. By creating an instance of FastAPI, we can define routes, handle requests, and manage the overall behavior of our API monitor application. The app variable will be used to register routes and define the behavior of our API monitor application as we build it out further.

@app.on_event("startup") #this decorator registers the startup function to be called when the FastAPI application starts up. The startup function is responsible for creating the necessary database tables by calling the create_tables() function. By using the @app.on_event("startup") decorator, we ensure that the create_tables() function is executed automatically when the application starts, allowing us to set up the database tables before handling any incoming requests.
def startup():
    create_tables()


@app.get("/")
def root():
    return {"message": "API Monitor is running!"}
