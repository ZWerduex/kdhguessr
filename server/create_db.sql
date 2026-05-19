
create table players (
    name text primary key,
    password text not null
) without rowid;

create table rounds (
    id integer primary key,
    timestamp integer not null
);

create table rooms (
    id integer primary key
);

create table room_rounds (
    room_id integer not null,
    round_id integer not null,
    foreign key (room_id) references rooms(id),
    foreign key (round_id) references rounds(id)
    primary key (room_id, round_id)
);

create table round_results (
    player_name text not null,
    round_id integer not null,
    guess integer not null,
    score integer not null,
    foreign key (player_name) references players(name),
    foreign key (round_id) references rounds(id),
    primary key (player_name, round_id)
);