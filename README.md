# Nirvana Takehome

## Project Approach

I wanted to ensure that our objects (both success and errors) are handled gracefully between our services and routes.

In order to achieve this we use two basic classes: `success.py` and `errors.py`.

The thought behind wrapping every response inside of a `success.Success()` class when we get a 200 response, and wrapping every response inside of the correct `errors.Subclass` when we have an error is amazing for not only testing, but for handling responses from API's.

For example, in the `services/member_copay.py` class we use this exact pattern matching.

```
response = await CopayService.get_copay_data(id)
    match response:
        case success.Success():
            return {
                "status_code": 200,
                "response_type": "success",
                "description": "Successfully got member copay data and smoothed it for id: {}".format(id),
                "data": response.unpack()
            }
        case errors.NotEnoughDataError():
            return {
                "status_code": 500,
                "response_type": "error",
                "description": "Not enough data received",
                "data": response.toJson()
            }
        case _:
            return {
                "status_code": 500,
                "response_type": "UnexpectedError",
                "description": "Error retrieving data",
                "data": None
            }
```

This makes things extremely clear as to what went wrong (`NotEnoughDataError` versus a generic `UnexpectedError`) and when things are successful, we can simple `.unpack()` the object to return.

Additionally this is extensible, if we run into new errors we can add them into the pattern matcher, or maybe if we get tired of adding too many errors we can simple create a catchall error called `ApiUnreliableError` and handle it that way.

This also ensures, that our type safety handling works agnostic of what our service actually returns to the route. Since we're simply expecting a `success.Success()` object, instead of a `httpx.Response` object or a `dict` or `json`. Which makes coding to interfaces much more clean.

Additionally, this makes our tests incredibly robust, we can intentionally send bad data into our functions to test a negative case, and assert:

```
assert type(result) == error.NotEnoughDataError
```

## Decoupling Processes

I would have liked to add in actual Pub/Sub architecture, but I did end up running out of time. In my ideal vision of the API I would want any request to get member copay data to instead trigger an event that queues a job. That job should then do everything in our `services/copay_retrieval_service.py` and then return another event that then notifies the end-user that the data is ready to be recieved.

The reason for this decoupling, is that it would make this API endpoint even more resilient versus unreliable copay data API's. If we can't reach an endpoint, we can retry until we get a response, and if it takes too long we can then time out the request and decide to continue with the data we got, or return an error. 

## Run 

`docker-compose up --build` 

Is sufficient for running the project. This `compose` however also uses profiles, which means when you run the above command, the only services that will spin up are `MongoDB` and `Redis`.

In order to get the backend up and running you have to add to the command:

`docker-compose --profile backend up --build`

If you want to run both frontend, backend and all the requisite services you can specify it like so:

`docker-compose --profile dev up --build`

## Features

The project right now has basic JWT authentication and a VERY simplified admin panel (simple username password protection to get issued a JWT token).

The `membercopay/` endpoint is protected by this endpoint. In order to successfully get the JWT token you must create an admin by going to:

`admin/` 

With a request body that contains:

```
{
    "fullname": "Ragnaros Firelord",
    "email": "ragnaros@molten.core",
    "password": "majordomo"
}
```

Afterwards navigate to:

`admin/login`

With a request body that contains:

```
{
    "username": "ragnaros@molten.core",
    "password": "majordomo"
}
```

Which should return an access token that you can then attach to any subsequent API request that targets `membercopay/`.

Alternatively, you can navigate to the root and edit in `main.py` on line 10:

```
10| token_listener = JWTBearer() -> token_listener = lambda: {}
```

To gain full access to all the API endpoints.

## Testing

Navigate to the root folder for the `backend/` and create a Python virtual environment.

`python3 -m venv venv` to create a new virtual environment.

Activate it using `source venv/bin/activate` and install dependencies `pip3 install -r requirements.txt`.

Afterwards run `python3 -m pytest tests` to run all the tests.
