instructions= [
    
    "SET FOREIGN_KEY_CHECKS=0;",
    "DROP TABLE IF EXISTS todo;",
    "DROP TABLE IF EXISTS user;",
    "SET FOREIGN_KEY_CHECKS=1;",
    """
    CREATE TABLE user (
        userID INT PRIMARY KEY AUTO_INCREMENT,
        userName VARCHAR(50) UNIQUE NOT NULL, 
        password VARCHAR(120) NOT NULL
    );
    """,
    """
    CREATE TABLE todo (
        todoID INT PRIMARY KEY AUTO_INCREMENT,
        userID INT NOT NULL, 
        create_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        description VARCHAR(255) NOT NULL,
        completed BOOLEAN NOT NULL,
        FOREIGN KEY (userID) REFERENCES user (userID) 
    );
    """,
]