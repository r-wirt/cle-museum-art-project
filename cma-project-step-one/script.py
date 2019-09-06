import sqlite3
import json

#Final JSON goes here
artwork_results = {'artworkdata': []}
connection = sqlite3.connect('cma-artworks.db')

cursor = connection.cursor()

#Query returns all 100 unique pieces of artwork
#with each row specifiying artwork id, accession number, tombstone, title, department id, & department name
cursor.execute("""

SELECT artwork.id,  artwork.accession_number, artwork.title, artwork.tombstone, artwork__department.department_id, department.name
FROM artwork
INNER JOIN artwork__department ON artwork.id = artwork__department.artwork_id
INNER JOIN department ON artwork__department.department_id = department.id

 """)

#Assign query results to variable
artwork_props = cursor.fetchall()
connection.commit()


#Loop converts each tuple from the artwork_props array to JSON format, then appends to artwork_results array
#Ex: ("artwork_id", "accession_number", ....) ---> { artworkid: "artwork_id", accession_number:"accession_number", ... }
for prop in artwork_props:
    artwork_results['artworkdata'].append(dict(

    artwork_id = prop[0],
    accession_number = prop[1],
    title = prop[2],
    tombstone =  prop[3],
    creators =  [],
    department = dict(
     id = prop[4],
     name = prop[5]
    )

    ))

#Query returns an artist's id, role, description, and artwork_id that they are associated with
cursor.execute("""


SELECT artwork__creator.artwork_id, Alias.id, Alias.role, Alias.description
FROM artwork__creator
INNER JOIN  ( SELECT * FROM creator  GROUP BY creator.description) Alias
ON artwork__creator.creator_id = Alias.id

 """)

#Assign query results to variable
artist_props = cursor.fetchall()
connection.commit()


#Matches up every piece of artwork in artwork_results with the appropriate creator(s) and their specific properties
for artwork in artwork_results['artworkdata']:
    for creator in artist_props:
        if artwork['artwork_id'] in creator:
            artwork['creators'].append({ 'id': creator[1], 'role': creator[2], 'description': creator[3] })

#Write artwork results to json file
with open('data.json', 'w', encoding='utf-8') as file:
    json.dump(artwork_results, file, ensure_ascii=False, indent = 4)


connection.close()
