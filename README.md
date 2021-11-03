# Docker Jupyter Geometric

Hey all, Sam here, apologies for the following diatribe. I'm a full stack software engineer doing graduate work in mathematics. Specifically mathematical modeling. As a software engineer navigating the data science space, I have noticed that several of the approaches don't take advantage of current technologies and instead recreate the wheel. Namely the lack of database usage, structuring the project as a collection of scripts instead of as an application (api), not having a clear way to interact with the trained results, and not leveraging containerized environments.
 
This is just a containerized implementation of data science development in jupyter notebook leveraging neo4j as a database. The jupyter tutorial that we are focusing on is a list of tutorials on geometric learning using pytorch. Please refer to [Pytorch geometric](https://github.com/rusty1s/pytorch_geometric) for further information.

## Standing up the environment

1. Make sure that docker is installed on your local machine. 
2. Download this project 
3. Open a terminal and cd into this directory
3. Run `docker-compose up -d`
4. Open a browers and see your jupyter notebook at database interfaces

## Available Scripts

In the project directory, you can run:

### `docker-compose up`

Runs the app in the development mode with with logs output to the terminal

The neo4j interface can be viewed in a local browser
Open [http://localhost:7474/browser/](http://localhost:7474/browser/) to view it in the browser.


The jupyter notebook has all of the python packages as well as NVIDIA and CUDA drivers.
Open [http://localhost:8888/](http://localhost:8888/) to view the notebook in the browser.


To connect with the database use the container name instead of localhost.
To Shut this down either close the terminal or press ctrl c

### `docker-compose up -d`

This does the same as the previous command but it runs the app independant of your terminal being open. 

The services will run in the background until you cd into this directory and run **'docker-compose down'**


### `docker-compose build`
If you containered services are not behaving the way that you would expect run this command to rebuild all the containers. Then when you run docker-compose up it will use these fresh docker images.