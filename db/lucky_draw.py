from datetime import timedelta, datetime
from db.utils import executeQuery


def get_user(user_id):
    query = f"SSELECT * FROM users WHERE user_id == '{user_id}'"
    result = executeQuery(query, "one")
    return result[0]


def create_raffle(title, description, prize, prize_picture_url, start_time, closing_time):
    """Create a new lucky draw raffle.
    Args:
        title: the title of he raffle
        description (optional): the description of the raffle
        prize: the prize for the raffle winner
        prize_picture_url (optional): The URL for the cover picture of the prize
        start_time: The date and time when the raffle entries will start
        closing_time: The date and time when the raffle entries will close.
    Returns:
        ID of newly created raffle.
    """
    query = f" INSERT INTO raffle (title, description, prize, prize_picture_url, start_time, closing_time) \
             VALUES ('{title}', '{description}', '{prize}', '{prize_picture_url}', '{start_time}', '{closing_time}') RETURNING id; "
    raffle = executeQuery(query, "one")
    return raffle[0]


def enter_raflle(raffle_id, ticket_no, user_id):
    """Add an entry into the raffle for the given user with with the given user ticket.
    Args:
        raffle_id: The DB ID of the raffle
        ticket_no: The user ticket with which they enter the raffle
        user_id: The DB ID of the user.
    """
    query = f"INSERT INTO entry (raffle_id, ticket_no, user_id) VALUES ('{raffle_id}', '{ticket_no}', '{user_id}')"
    raffle = executeQuery(query, "one")
    return raffle[0]


def get_raffle(raffle_id, show_email):
    """Get the details for a given raffle.
    Args:
        raffle_id: The DB ID of the raffle
        show_email (optional): Show the email of the winner, in case the details are being accessed by an admin.
    Returns:
        Dictionary with the following structure:
        {
            "title": <raffle title>,
            "description": <raffle description>,
            "prize": <prize for the raffle winner>
            "prie_picture_url": <cover picture URL for the prize>
            "start_time": <date and time when the raffle entries will start>,
            "closing_time": <date and time when the raffle entries will close>,
            "winner_name": <name of the raffle winner> (if result is declared)
            "winner_ticket_no": <winning ticket no.> (if result is declared)
            "winner_email_id": <email ID of the raffle winner> (if result is declared, visible only to admins)
        }
    """
    cols = "title, description, prize, prize_picture_url, start_time, closing_time, name AS winner_name, ticket_no AS winner_ticket_no"
    if show_email:
        cols += ", email_id AS winner_email_id"

    query =  f"SELECT {cols} FROM raffle AS raffle LEFT JOIN result AS result \
             ON raffle.id = result.raffle_id\
             LEFT JOIN user\
                ON result.user_id = user.id\
             WHERE raffle.id = '{raffle_id}'"

    raffle = executeQuery(query, "one")
    return raffle if raffle[0] else None


def get_raffle_applicants(raffle_id, user_id):
    """Get a list of applicants for a given raffle.
    Args:
        raffle_id: The DB ID of the raffle
        user_id (Optional): If specified return entries of the user with the specified user_id.
    Returns:
        A list of dictionaries with the following structure:
        [
            {
                name" <name of the raffle applicant>
                "ticket_no": <ticket no. of the applicant>
                email_id": <email ID of the applicant>
            },
        ...
        ]
    """
    query = f" SELECT name, email_id, ticket_no, user_id \
              FROM entry AS entry \
         LEFT JOIN user \
                ON entry.user_id = user.id \
             WHERE entry.raffle_id = '{raffle_id}' AND user_id = '{user_id}' \
        "
    result = executeQuery(query, "all")
    return [row[0] for row in result]


def get_past_raffles(show_email, days):
    """Get the details for a given raffle.
    Args:
        show_email (optional): Show the email of the winner, in case the details are being accessed by an admin.
        days (optional): Limit the past raffles to past ``days`` days.
    Returns:
        A list of dictionaries with the following structure:
        [
            {
                "title": <raffle title>,
                "description": <raffle description>,
                "prize": <prize for the raffle winner>
                "prie_picture_url": <cover picture URL for the prize>
                "start_time": <date and time when the raffle entries will start>,
                "closing_time": <date and time when the raffle entries will close>,
                "winner_name": <name of the raffle winner> (if result is declared)
                "winner_ticket_no": <winning ticket no.> (if result is declared)
                "winner_email_id": <email ID of the raffle winner> (if result is declared, visible only to admins)
            },
            ...
        ]
    """
    cols = "title, description, prize, prize_picture_url, start_time, closing_time, name AS winner_name, result.ticket_no AS winner_ticket_no"
    if show_email:
        cols += ", email_id AS winner_email_id"

    query = """
            SELECT {cols}
              FROM raffle AS raffle
         LEFT JOIN result AS result
                ON raffle.id = result.raffle_id
         LEFT JOIN user
                ON result.user_id = user.id
             WHERE raffle.closing_time < NOW()
        """.format(cols=cols)

    if days:
        query += "AND raffle.closing_time > NOW()"
    result = executeQuery(query, "all")
    return [row[0] for row in result]


def get_upcoming_raffles(limit):
    """Get a list of upcoming raffles.
    Args:
        limit: Limit the results to get only the next raffle.
    Returns:
        A list of dictionaries with the following structure:
        [
            {
                "title": <raffle title>,
                "description": <raffle description>,
                "prize": <prize for the raffle winner>
                "prie_picture_url": <cover picture URL for the prize>
                "start_time": <date and time when the raffle entries will start>,
                 "closing_time": <date and time when the raffle entries will close>,
            },
            ...
        ]
    """
    query = f"""
            SELECT title, description, prize, prize_picture_url, start_time, closing_time
              FROM raffle AS raffle
             WHERE raffle.start_time > NOW()
          ORDER BY start_time
        """
    if limit:
        query += f"LIMIT = '{limit}'"


    result = executeQuery(query, "all")

    return [row[0] for row in result]


def get_ongoing_raffles():
    """Get a list of ongoing raffles.
    Returns:
        A list of dictionaries with the following structure:
        [
            {
                "title": <raffle title>,
                "description": <raffle description>,
                "prize": <prize for the raffle winner>
                "prie_picture_url": <cover picture URL for the prize>
                "start_time": <date and time when the raffle entries will start>,
                 "closing_time": <date and time when the raffle entries will close>,
            },
            ...
        ]
    """

    query = f"""
        SELECT title, description, prize, prize_picture_url, start_time, closing_time
          FROM raffle AS raffle
         WHERE raffle.start_time < NOW()
           AND raffle.closing_time > NOW()
    """
    result = executeQuery(query, "all")
    return [row[0] for row in result]


def draw_ticket(user_id):
    """Insert a new ticket for the given user.
    Args:
        user_id (int): the DB ID of the user.
    Returns:
        {
            "ticket_no": <ticket no.>,
            "valid_upto": <date and time till which the ticket is valid>,
        },
    """
    valid_upto = datetime.now() + timedelta(days=config.TICKET_VALIDITY)

    query = f"""
        INSERT INTO ticket (user_id, valid_upto)
             VALUES ('{user_id}', '{valid_upto}')
          RETURNING ticket_no, valid_upto
    """
    result = executeQuery(query, 'one')
    return result[0]


def get_tickets_for_user(user_id):
    """Get list of tickets drawn by a given user.
    Args:
        user_id (int): The DB ID of a user.
    Returns:
        A list of dictionaries with the following structure:
        [
            {
                "ticket_no": <ticket no.>,
                "valid_upto": <date and time till which the ticket is valid>,
                "redeemed": <True if the user has used the given ticket, else Flase>
            },
            ...
        ]
    """

    query = f"""
        SELECT ticket_no
              , valid_upto
              , ticket_no IN (SELECT ticket_no FROM entry where user_id = '{user_id}') AS redeemed
          FROM ticket
         WHERE user_id = '{user_id}'
    """
    result = executeQuery(query, "all")
    return [row[0] for row in result]


def get_next_vaild_ticket_for_user(user_id):
    """Get the earliest valid and non-redeemed ticket for the user.
    Args:
        id (int): The DB ID of a user.
    Returns:
        The ticket number of the earliest valid and non-redeemed ticket.
    """
    query = f" SELECT ticket_no\
         FROM ticket\
        WHERE user_id = '{user_id}'\
        AND  ticket_no NOT IN (SELECT ticket_no FROM entry where user_id = '{user_id}')\
        AND valid_upto > NOW()\
        ORDER BY created\
        LIMIT 1"

    result =  executeQuery(query, "one")
    return row["ticket_no"] if result else None


def get_raffles_to_compute_results():
    """Get a list of raffle IDs whose results are to be coomputed.
    Returns:
        A list of raffle IDs.
    """

    query=f"SELECT id \
        FROM raffle AS raffle \
        WHERE raffle.closing_time < NOW() \
        AND raffle.closing_time > NOW()"
    result = executeQuery(query, "one")
    return [row["id"] for row in result]


def save_raffle_results(raffle_id, ticket_no, user_id):
    """Save the results of a raffle.
    Args:
        raffle_id: The DB ID of the raffle
        ticket_no: The winning ticket no,
    """
    query = f"INSERT INTO result (raffle_id, ticket_no, user_id)\
                 VALUES ('{raffle_id}', '{ticket_no}', '{user_id}')"
    executeQuery(query, "one")
    return ""