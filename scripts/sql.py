import os
import sqlite3

# Connect to SQLite database (or create a new one if it doesn't exist)
conn = sqlite3.connect("Starships/SQL/starbase.sqlite")
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS checksums (
        id INTEGER PRIMARY KEY,
        checksum TEXT,
        checksum_file_path TEXT,
        data_type TEXT,
        type TEXT,
        gene_type TEXT
    )
    """
)

# list of directories to search through
directories = (
    "./captain/tyr/fna/starfish",
    "./captain/tyr/fna/alignments",
    "./captain/tyr/fna/tree",
    "./captain/tyr/fna/blastdb",
    "./captain/tyr/hmm",
    "./captain/tyr/faa/starfish",
    "./captain/tyr/faa/alignments",
    "./captain/tyr/faa/tree",
    "./captain/tyr/faa/blastdb",
    "./captain/tyr/faa/manual",
    "./ships/fna/starfish",
    "./ships/fna/blastdb",
    "./ships/fna/manual",
    "./metadata/ships/starfish",
    "./metadata/ships/starfish/gff",
    "./metadata/ships/starfish/output",
    "./metadata/ships/manual",
    "./cargo/nlr/fna/blastdb",
    "./cargo/nlr/hmm",
    "./cargo/nlr/faa/starfish",
    "./cargo/nlr/faa/blastdb",
    "./cargo/fre/fna/blastdb",
    "./cargo/fre/hmm",
    "./cargo/fre/faa/starfish",
    "./cargo/fre/faa/blastdb",
    "./cargo/plp/fna/blastdb",
    "./cargo/plp/hmm",
    "./cargo/plp/faa/starfish",
    "./cargo/plp/faa/blastdb",
    "./cargo/duf3723/fna/blastdb",
    "./cargo/duf3723/hmm",
    "./cargo/duf3723/faa/starfish",
    "./cargo/duf3723/faa/blastdb",
)

# for directory in directories:
#     data_type = directory.split("/")[2]

#     if "manual" in directory:
#         db_source = "manual-annotations"
#     elif "mycodb" or "mtdb" in directory:
#         db_source = "mycodb"
#     else:
#         db_source = ""

#     if "cargo" in directory:
#         type = "cargo"
#     elif "captain" in directory:
#         type = "captain"
#     elif "ship" in directory:
#         type = "ship"
#     else:
#         type = ""

#     if (type == "captain" or "cargo") and len(directory.split("/")) > 4:
#         gene_type = directory.split("/")[4]

#     # Create table if it doesn't exist
#     cursor.execute(
#         f"""
#         CREATE TABLE IF NOT EXISTS {data_type} (
#             id INTEGER PRIMARY KEY,
#             name TEXT,
#             data_type TEXT,
#             db_source TEXT,
#             type TEXT,
#             gene_type TEXT,
#             file_path TEXT
#         )
#     """
#     )

#     # Iterate through files in the directory
#     for file_name in os.listdir(directory):
#         name = os.path.splitext(file_name)[0]
#         file_path = os.path.join(directory, file_name)
#         # Insert record into the fasta table
#         cursor.execute(
#             f"""
#             INSERT INTO {data_type} (name, data_type, db_source, type, gene_type, file_path)
#             VALUES (?, ?, ?, ?, ?, ?)
#             """,
#             (name, data_type, db_source, type, gene_type, file_path),
#         )

checksum_files = (
    "./cargo/nlr/faa/faa.checksums.txt",
    "./cargo/fre/faa/faa.checksums.txt",
    "./cargo/plp/faa/faa.checksums.txt",
    "./cargo/duf3723/faa/faa.checksums.txt",
    "./captain/tyr/faa/faa.checksums.txt",
)

for checksum_file in checksum_files:
    if checksum_file.endswith(".txt"):
        print(checksum_file)
        data_type = checksum_file.split("/")[2]
        type = checksum_file.split("/")[3]
        if type == "ships":
            gene_type = ""
        else:
            gene_type = checksum_file.split("/")[4]
        with open(checksum_file, "r") as file:
            lines = file.readlines()
        # Insert data into the table
        for line in lines:
            parts = line.strip().split("\t")
            checksum, checksum_file_path = parts[0], parts[1]

            insert_query = """
                INSERT INTO checksums (checksum, checksum_file_path, data_type, type, gene_type)
                VALUES (?, ?, ?, ?, ?);
            """
            cursor.execute(
                insert_query,
                (
                    checksum,
                    checksum_file_path,
                    data_type,
                    type,
                    gene_type,
                ),
            )


# Commit changes and close the connection
conn.commit()
conn.close()
