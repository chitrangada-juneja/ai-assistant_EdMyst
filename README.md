__Instructions to set up AI Assistant__


To run this AI Assistant, you need some things set up :

In the `backend` :
* create a virtual environment in Python
* download all the packages needed in the `requirements.txt` file.
* ensure you have the necessary keys and tokens listed in the `.env` file.
* Add your database as pdf files in the folder `data`. Everytime you add files, and rerun the chatbot, make sure you delete the word-embedding chunks and index files from `storage`. The AI Assistant only recreates these files when they don't exist.
* run `uvicorn main:app --reload --host 0.0.0.0 --port 8000` inside the virtual environment.
  
In the `frontend` :
* You need to have Create React App installed for the frontend to configure properly; refer to the `package.json` file.
* run `npm start`, and click on the link that appears for your local run of the AI Assistant.


