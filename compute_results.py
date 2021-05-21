from random import choice
from db import lucky_draw


class ResultComupter:

    def compute_result_for_given_raffle(self, raffle_id, user_id):
        applicants = lucky_draw.get_raffle_applicants(raffle_id, user_id)
        if applicants:
            winner = choice(applicants)
            lucky_draw.save_raffle_results(raffle_id=raffle_id, ticket_no=winner["ticket_no"], user_id=winner["user_id"])

    def compute_results(self):
        raffles = db_lucky_draw.get_raffles_to_compute_results()
        for raffle_id in raffles:
            self.compute_result_for_given_raffle(raffle_id, user_id)


if __name__ == "__main__":
    rc = ResultComupter()
    rc.compute_results()
