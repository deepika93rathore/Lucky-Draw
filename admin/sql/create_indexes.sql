BEGIN;

CREATE INDEX user_id_ticekts ON lucky_draw.ticket (user_id);
CREATE UNIQUE INDEX user_id_raffle_id_entry ON lucky_draw.entry (user_id, raffle_id);

COMMIT;
