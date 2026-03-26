CREATE TABLE IF NOT EXISTS users (
    id       INT         NOT NULL AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    salt     VARCHAR(64) NOT NULL,
    password VARCHAR(64) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS profiles (
    id      INT                          NOT NULL AUTO_INCREMENT,
    user_id INT                          NOT NULL UNIQUE,
    name    VARCHAR(100)                 NOT NULL,
    age     TINYINT UNSIGNED             NOT NULL,
    gender  VARCHAR(30)                  NOT NULL,
    budget  ENUM('Low','Medium','High')  NOT NULL,
    city    VARCHAR(100)                 NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS user_actions (
    id          INT                                       NOT NULL AUTO_INCREMENT,
    user_id     INT                                       NOT NULL,
    action_type ENUM('Itinerary','Reservation','Ticket')  NOT NULL,
    event_name  VARCHAR(200)                              NOT NULL,
    timestamp   DATETIME                                  NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS venues (
    id          INT                                            NOT NULL AUTO_INCREMENT,
    name        VARCHAR(200)                                   NOT NULL UNIQUE,
    type        ENUM('Music','Games','Movies','Food & Drinks') NOT NULL,
    city        VARCHAR(100)                                   NOT NULL,
    budget      ENUM('Low','Medium','High')                    NOT NULL,
    noise       ENUM('Low','Medium','High')                    NOT NULL,
    min_age     TINYINT UNSIGNED                               NOT NULL DEFAULT 0,
    time_of_day ENUM('Morning','Afternoon','Evening')          NOT NULL,
    description TEXT,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS venue_ratings (
    id       INT     NOT NULL AUTO_INCREMENT,
    venue_id INT     NOT NULL,
    user_id  INT     NOT NULL,
    rating   TINYINT NOT NULL CHECK (rating BETWEEN 1 AND 10),
    PRIMARY KEY (id),
    UNIQUE KEY uq_venue_user (venue_id, user_id),
    FOREIGN KEY (venue_id) REFERENCES venues(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id)  REFERENCES users(id)  ON DELETE CASCADE
);
