drop table if exists consumer;
create table consumer (message_no int NOT NULL, transmission_time datetime(4) NOT NULL, arrival_time datetime(4) NOT NULL, primary key(message_no));

