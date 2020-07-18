


drop table if exists users;
create table users (
    profile_pic string default('default.png'),
    pics integer default(0),
    username string not null,
    firstname string not null,
    lastname string not null,
    email string not null,
    password string not null,
    likes integer default(0),
    matches integer default(0),
    bio text default('Tell everyone about yourself...'),
    gender string,
    age integer default(0),
    sex_orientation string,
    fame integer default(100),
    geo_location string,
    last_online string default('Offline'),
    complete string default('False'),
    verified string default(0)
);

drop table if exists interests;
create table interests(
    id integer primary key autoincrement,
    username string not null,
    travelling  integer default(0),
    exercise    integer default(0),
    movies      integer default(0),
    dancing     integer default(0),
    cooking     integer default(0),
    outdoors    integer default(0),
    politics    integer default(0),
    pets        integer default(0),
    photography integer default(0),
    sports      integer default(0)
);

drop table if exists likes ;
create table likes(
    id integer primary key autoincrement,
    user_liking string not null,
    user_liked string not null
);

drop table if exists matches;
create table matches(
    id integer primary key autoincrement,
    user_1 string not null,
    user_2 string not null
);

drop table if exists messages;
create table messages(
    id integer primary key autoincrement,
    sender string not null,
    recipient string not null,
    message text not null,
    timestamp string
    );

drop table if exists images;
create table images(
    username string not null,
    file_name string not null
);

drop table if exists history;
create table history(
  log_username string not null,
  notif_username string not null,
  message string not null,
  history_type integer default(0)
);
