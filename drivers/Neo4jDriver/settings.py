from neomodel import config

user = "neo4j"
password = "prime-paint-cafe-alfonso-joel-2355" #  by default its "neo4j"
host_name = "geometric_neo4j"

scheme = "neo4j"  # Connecting to Aura, use the "neo4j+s" URI scheme
port = 7687

bolt_url = "bolt://" + user+ ":" + password + "@" +host_name+ ":" + str(port)



config.DATABASE_URL = bolt_url