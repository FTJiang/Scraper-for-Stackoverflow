import random
 
SOURCE_FILE='UserAgents.txt'
 
def get():
    f = open(SOURCE_FILE)
    agents = f.readlines()
 
    return random.choice(agents).strip()
 
def getAll():
    f = open(SOURCE_FILE)
    agents = f.readlines()
    return [a.strip() for a in agents]

def Agent():
	agent = get()
	return agent