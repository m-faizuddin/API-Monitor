
#main.py - This file is the entry point for the FastAPI application. It sets up the FastAPI instance, includes the API routes defined in the apis router, and defines a startup event to create the necessary database tables when the application starts. The root endpoint ("/") is also defined to return a simple message indicating that the API Monitor is running. This file serves as the main configuration and setup for the API monitoring application, allowing us to define routes and manage the application's behavior as we build it out further.

from fastapi import FastAPI
from database import create_tables
from routers import apis, logs
from apscheduler.schedulers.background import BackgroundScheduler
from worker import check_apis

from fastapi.middleware.cors import CORSMiddleware # this helps with cross-origin requests, allowing the frontend to communicate with the backend
# Imports FastAPI's CORS middleware. CORS is a browser security feature that
# controls whether a webpage is allowed to make requests to a different origin
# (different domain, protocol, or port). This middleware tells the browser
# which frontends are allowed to access our FastAPI backend.

app = FastAPI() #This line creates an instance of the FastAPI class and assigns it to the variable app. The FastAPI class is the main entry point for creating a FastAPI application. By creating an instance of FastAPI, we can define routes, handle requests, and manage the overall behavior of our API monitor application. The app variable will be used to register routes and define the behavior of our API monitor application as we build it out further.

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(apis.router) #This line includes the routes defined in the apis router into our main FastAPI application. The include_router() method is used to register the routes from the apis router with our main app instance. By including the apis router, we can organize our API endpoints related to API monitoring functionality in a modular way, keeping our code clean and maintainable. This allows us to define all the routes for managing monitored APIs in a separate file (routers/apis.py) and then include them in our main application using this line of code.
app.include_router(logs.router)

@app.on_event("startup") #this decorator registers the startup function to be called when the FastAPI application starts up. The startup function is responsible for creating the necessary database tables by calling the create_tables() function. By using the @app.on_event("startup") decorator, we ensure that the create_tables() function is executed automatically when the application starts, allowing us to set up the database tables before handling any incoming requests.
def startup():
    create_tables()
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_apis, "interval", minutes=5)
    scheduler.start()

@app.get("/")
def root():
    return {"message": "API Monitor is running!"}
