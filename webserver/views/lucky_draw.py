import pytz
from datetime import datetime
from flask import Blueprint, jsonify, current_app, request
from werkzeug.exceptions import BadRequest, Conflict, Unauthorized
import db.lucky_draw as db_lucky_draw

lucky_draw_bp = Blueprint("lucky_draw", __name__, "lucky_draw")


@lucky_draw_bp.route("/raffle/<int:raffle_id>,<int:user_id>", methods=["GET"])
def get_raffle(raffle_id, user_id):
    """ Get raffle with the given ``raffle_id``. Returns the raffle applicants too, in case the user is an admin.
    Returns:
        - raffle: the raffle record for the given ``raffle_id``.
    """
    user_email = db_lucky_draw.get_user(user_id)
    raffle = db_lucky_draw.get_raffle(raffle_id=raffle_id, show_email=user_email['email'])

    if raffle:
        raffle_entry = db_lucky_draw.get_raffle_applicants(raffle_id=raffle_id, user_id=user_id)
        raffle["entry"] = raffle_entry[0] if raffle_entry else None

    return jsonify({"raffle": raffle})


@lucky_draw_bp.route("/past-raffles/<int:user_id", methods=["GET"])
def get_past_raffles(user_id):
    """ Get a list of past raffles. Returns the winner email ID too, in case the user is an admin.
    Returns:
        - raffles: the list of raffles.
    """
    user = db_lucky_draw.get_user(user_id)

    show_email = False
    if user['email_id']:
        show_email = True

    raffles = db_lucky_draw.get_past_raffles(show_email=show_email)
    return jsonify({"raffles": raffles})


@lucky_draw_bp.route("/last-week-raffles/<int:user_id>", methods=["GET"])
def get_last_week_raffles(user_id):
    """ Get a list of last week raffles.
    Returns:
        - raffles: the list of raffles.
    """
    user = db_lucky_draw.get_user(user_id)

    show_email = False
    if user['email_id']:
        show_email = True

    raffles = db_lucky_draw.get_past_raffles(show_email=show_email, days=7)
    return jsonify({"raffles": raffles})


@lucky_draw_bp.route("/next-raffle", methods=["GET"])
def get_next_raffle():
    """ Get the next raffle.
    Returns:
        - raffle: the next raffle.
    """
    raffles = db_lucky_draw.get_upcoming_raffles(limit=1)
    return jsonify({"raffle": raffles})


@lucky_draw_bp.route("/upcoming-raffles", methods=["GET"])
def get_upcoming_raffles():
    """ Get a list of upcoming raffles.
    Returns:
        - raffles: the list of raffles.
    """
    raffles = db_lucky_draw.get_upcoming_raffles(limit=1)
    return jsonify({"raffles": raffles})


@lucky_draw_bp.route("/ongoing-raffles", methods=["GET"])
def get_ongoing_raffles():
    """ Get a list of ongoing raffles.
    Returns:
        - raffles: the list of raffles.
    """
    raffles = db_lucky_draw.get_ongoing_raffles()
    return jsonify({"raffles": raffles})


@lucky_draw_bp.route("/draw-ticket/<int:user_id>", methods=["POST"])
def draw_ticket(user_id):
    """ Draw a new ticket for the given user.
    Returns:
        - ticket: the newly drawn ticket.
    """
    ticket = db_lucky_draw.draw_ticket(user_id=user_id)
    return jsonify({"status": "ok", "ticket": ticket})


@lucky_draw_bp.route("/tickets/<int:user_id>", methods=["GET"])
def get_tickets_for_user(user_id):
    """ Get a given user"s tickets.
    Returns:
        - tickets: the tickets of the given user.
    """
    tickets = db_lucky_draw.get_tickets_for_user(user_id=user_id)
    return jsonify({"tickets": tickets})


@lucky_draw_bp.route("/raffle/<int:raffle_id>,<int:user_id>/enter", methods=["POST"])
def enter_raffle(raffle_id, user_id):
    """ Create an entry for the given user for the raffle ``raffle_id``.
    The earliest valid non-redeemed ticket is used to enter the raffle.
    Raises:
        - BadRequest(404): The user has no valid non-redeemed tickets
        - BadRequest(404): The raffle doesn't exist
        - BadRequest(404): The raffle entries are closed
        - Conflict(409): The user has already entered the raffle
    """
    user = db_lucky_draw.get_user(user_id)
    ticket_no = db_lucky_draw.get_next_vaild_ticket_for_user(user_id=user_id)
    if ticket_no is None:
        raise BadRequest("You don't have any tickets left.")

    raffle = db_lucky_draw.get_raffle(raffle_id=raffle_id, show_email=user['email'])

    if not raffle:
        raise BadRequest("The raffle with id %s doesn't exist." % raffle_id)

    # Submissions close 1 hour prior to scheduled result time
    if datetime.now(pytz.UTC) > raffle["closing_time"]:
        raise BadRequest("Entries for raffle with id %s are closed." % raffle_id)

    try:
        db_lucky_draw.enter_raflle(raffle_id=raffle_id, ticket_no=ticket_no, user_id=user.id)
    except IntegrityError:
        raise Conflict("You have already signed up for this raffle.")

    return jsonify({"status": "ok"})


@lucky_draw_bp.route("/create-raffle", methods=["POST"])
def create_raffle():
    """ Create a new raffle. This endpoint is admin only.
    Raises:
        - BadRequest(401): The user is not an authorized admin
        - BadRequest(404): Incomplete form POSTed
    Returns:
        - raffle_id: the id of the newly created raffle.
    """

    title = request.form.get("title")
    description = request.form.get("description")
    prize = request.form.get("prize")
    prize_picture_url = request.form.get("prize_picture_url")
    start_time = request.form.get("start_time")
    closing_time = request.form.get("closing_time")

    if not title or not prize or not start_time or not closing_time:
        raise BadRequest("Title, Prize, Start time and Closing time are required.")

    if start_time > closing_time:
        raise BadRequest("Raffle closing time must be greater than start time.")

    raffle_id = db_lucky_draw.create_raffle(title=title, description=description, prize=prize,
                                            prize_picture_url=prize_picture_url, start_time=start_time, closing_time=closing_time)

    return jsonify({"status": "ok", "raffle_id": raffle_id})
