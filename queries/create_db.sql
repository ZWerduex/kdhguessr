
create table if not exists players (
    name text primary key,
    password blob not null
) without rowid;

create table if not exists rounds (
    id integer primary key,
    timestamp integer not null
);

create table if not exists rooms (
    id integer primary key
);

create table if not exists room_rounds (
    room_id integer not null,
    round_id integer not null,
    foreign key (room_id) references rooms(id),
    foreign key (round_id) references rounds(id)
    primary key (room_id, round_id)
);

create table if not exists round_results (
    player_name text not null,
    round_id integer not null,
    guess integer not null,
    score integer not null,
    foreign key (player_name) references players(name),
    foreign key (round_id) references rounds(id),
    primary key (player_name, round_id)
);