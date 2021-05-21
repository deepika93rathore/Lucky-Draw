# Lucky-Draw


#### Install python dependencies

Install `virtualenv` using the command:

    pip install virtualenv

Move into the project directory and create a virtual environment, and install the python dependencies by running the following commands:

	virtualenv test
    source test/bin/activate
    pip install -r requirements.txt


# API Endpoints

### `/lucky-draw/raffle/<int:raffle_id>` [GET]

Get raffle with the given `raffle_id`. Returns the raffle applicants too, in case the user is an admin.

**Returns:**
- raffle: the raffle record for the given `raffle_id`.


### `/lucky-draw/past-raffles` [GET]

**Returns**:
- raffles: the list of raffles.

### `/lucky-draw/last-week-raffles` [GET]

Get a list of last week raffles.

**Returns**:
- raffles: the list of raffles.



### `/lucky-draw/next-raffle` [GET]

Get the next raffle.

**Returns:**
- raffle: the next raffle.


### `/lucky-draw/upcoming-raffles` [GET]
Get a list of upcoming raffles.

**Returns**:
- raffles: the list of raffles.

### `/lucky-draw/ongoing-raffles`[GET]

Get a list of ongoing raffles.

**Returns**:
- raffles: the list of raffles.



### `/lucky-draw/draw-ticket` [POST]
Draw a new ticket for the given user.

**Returns**:
- ticket: the newly drawn ticket.


### `/lucky-draw/tickets` [GET]
def get_tickets_for_user():
    """ Get a given user's tickets.

**Returns**:
- tickets: the tickets of the given user.


### `/lucky-draw/raffle/<int:raffle_id>/enter` [POST]

Create an entry for the given user for the raffle ``raffle_id``. The earliest valid non-redeemed ticket is used to enter the raffle.

**Raises**:
 - BadRequest(404): The user has no valid non-redeemed tickets
 - BadRequest(404): The raffle doesn't exist
 - BadRequest(404): The raffle entries are closed
 - Conflict(409): The user has already entered the raffle



### `/lucky-draw/create-raffle` [POST]

Create a new raffle. This endpoint is admin only.

**Raises**:
- BadRequest(401): The user is not an authorized admin
- BadRequest(404): Incomplete form POSTed

**Returns**:
- raffle_id: the id of the newly created raffle.
