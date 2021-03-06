BEGIN;

CREATE TABLE "user" (
  id                    SERIAL,
  email_id              TEXT NOT NULL,
  name                  TEXT NOT NULL,
  password              TEXT NOT NULL,
  auth_token            TEXT,
  created               TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
ALTER TABLE "user" ADD CONSTRAINT user_email_id_key UNIQUE (email_id);

CREATE TABLE lucky_draw.raffle (
  id                    SERIAL,
  title                 TEXT NOT NULL,
  description           TEXT,
  prize                 TEXT NOT NULL,
  prize_picture_url     TEXT,
  start_time            TIMESTAMP WITH TIME ZONE NOT NULL,
  closing_time          TIMESTAMP WITH TIME ZONE NOT NULL
);

CREATE TABLE lucky_draw.ticket (
  ticket_no             SERIAL,
  user_id               INT, -- FK to "user".id
  created               TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  valid_upto            TIMESTAMP WITH TIME ZONE NOT NULL
);

CREATE TABLE lucky_draw.entry (
  raffle_id             INT, -- FK to lucky_draw.raffle.id
  ticket_no             INT, -- FK to lucky_draw.ticket.ticket_no
  user_id               INT -- FK to "user".id
);

CREATE TABLE lucky_draw.result (
  raffle_id             INT, -- FK to lucky_draw.raffle.id
  ticket_no             INT, -- FK to lucky_draw.ticket.ticket_no
  user_id               INT -- FK to "user".id
);
ALTER TABLE lucky_draw.result ADD CONSTRAINT result_raffle_id_key UNIQUE (raffle_id);

COMMIT;
