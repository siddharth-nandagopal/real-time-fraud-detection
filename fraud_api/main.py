import uvicorn

from app import app

# Executable programs should define a main function that is called from within a conditional block
# It starts a server using uvicorn
if __name__ == '__main__':
    uvicorn.run(app)