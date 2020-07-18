--
--     id integer primary key autoincrement,
--     username string not null,
--     firstname string not null,
--     lastname string not null,
--     email string not null,
--     password string not null,
--     likes integer default(0),
--     matches integer default(0),
--     bio text default('Tell everyone about yourself...'),
--     gender string,
--     sex_orientation string,
--     fame integer default(0),
--     geo_location string,
--     last_online string,
--     complete string default(FALSE),
INSERT INTO users(email, username, profile_pic, firstname, lastname, password,  gender, last_online, verified) VALUES ('tspies@student.wethinkcode.co.za', 'Tristyn', 'Tristyn_HavanaCouplesShoot00342_edited.jpg', 'Tristyn', 'Spies', '$2b$12$T/ENjvPLY4p.beWVlWjGOe/6j0h2agDbFYA.Hub9DilAKzExtkJeq', 'Male', 'Never', 1);
INSERT INTO interests (username) VALUES ('Tristyn');
INSERT INTO images (username, file_name) VALUES ('Tristyn', 'Tristyn_HavanaCouplesShoot00342_edited.jpg');

INSERT INTO users(email, username, profile_pic, firstname, lastname, password,  gender, last_online, verified) VALUES ('ruth@matcha.com', 'Ruth', 'ruth_profile.jpg', 'Ruth', 'Shield', '$2b$12$T/ENjvPLY4p.beWVlWjGOe/6j0h2agDbFYA.Hub9DilAKzExtkJeq', 'Female', 'Never', 1);
INSERT INTO interests (username) VALUES ('Ruth');
INSERT INTO images (username, file_name) VALUES ('Ruth', 'ruth_profile.jpg');


INSERT INTO users(email, username, profile_pic, firstname, lastname, password,  gender, last_online, verified) VALUES ('mushu@matcha.com', 'Mushu', 'mushu_profile.jpg', 'Mushu', 'Spies', '$2b$12$T/ENjvPLY4p.beWVlWjGOe/6j0h2agDbFYA.Hub9DilAKzExtkJeq', 'Female', 'Never', 1);
INSERT INTO interests (username) VALUES ('Mushu');
INSERT INTO images (username, file_name) VALUES ('Mushu', 'mushu_profile.jpg'), ('Mushu', 'mushu1.jpg');

INSERT INTO users(email, username, firstname, lastname, password,  gender, last_online, verified) VALUES ('leyla@matcha.com', 'Leyla', 'Esterhuizen', 'Esterhuizen', '$2b$12$T/ENjvPLY4p.beWVlWjGOe/6j0h2agDbFYA.Hub9DilAKzExtkJeq', 'Female', 'Never', 1);
INSERT INTO interests (username) VALUES ('Leyla');

INSERT INTO users(email, username, profile_pic, firstname, lastname, password,  gender, last_online, verified) VALUES ('daniell@matcha.com', 'Daniell', 'daniell_profile.jpg', 'Daniell', 'Sutherland', '$2b$12$T/ENjvPLY4p.beWVlWjGOe/6j0h2agDbFYA.Hub9DilAKzExtkJeq', 'Male', 'Never', 1);
INSERT INTO interests (username) VALUES ('Daniell');
INSERT INTO images (username, file_name) VALUES ('Daniell', 'daniell_profile.jpg');

INSERT INTO users(email, username, firstname, lastname, password,  gender, last_online, verified) VALUES ('zaza@matcha.com', 'Zaza', 'Zaza', 'Browne', '$2b$12$T/ENjvPLY4p.beWVlWjGOe/6j0h2agDbFYA.Hub9DilAKzExtkJeq', 'Female', 'Never', 1);
INSERT INTO interests (username) VALUES ('Zaza');

INSERT INTO users(email, username, firstname, lastname, password,  gender, last_online, verified) VALUES ('rein@matcha.com', 'Rein', 'Reinhardt', 'Browne', '$2b$12$T/ENjvPLY4p.beWVlWjGOe/6j0h2agDbFYA.Hub9DilAKzExtkJeq', 'Male', 'Never', 1);
INSERT INTO interests (username) VALUES ('Rein');