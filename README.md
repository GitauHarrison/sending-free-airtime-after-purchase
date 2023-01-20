# Africa's Talking Airtime API

![Free Airtime Demo](/app/static/images/free-airtime.gif)

Demo app showing how a user gets free airtime after a successful purchase. The main point is to send voice airtime to a customer after a successfull purchase.


## Africa's Talking Airtime API

In your view function, add the following:

```python
def send_airtime():
    username = app.config['AT_USERNAME']
    api_key = app.config['AFRICASTALKING_API_KEY']

    africastalking.initialize(username, api_key)

    airtime = africastalking.Airtime

    phone_number = current_user.phone # use logged in user's phone number

    currency_code = "KES" #Change this to your country's code
    amount = 5

    try:
        response = airtime.send(
            phone_number=phone_number, amount=amount, currency_code=currency_code)
        print(response)
    except Exception as e:
        print(f"Encountered an error while sending airtime. More error details below\n {e}")
```

The API needs your application's username, gotten from creating an app on [AT dashboard](https://account.africastalking.com/). You will also need an API key, gotten from the dashboard.

The parameters needed to successfully invoke the Airtime API are:
- Application's `username`
- Airtime `api_key`
- User's `phone_number`
- `amount` to be topped up (you may also want to hide this data using an environment variable)
- `currency_code` (depending on your country)

Above, I am sourcing the `username` and `api_key` values from environment variables, to hide that data. The `airtime.send` function is used to send the actual airtime top up to the user.

## Note

- The [live app link](https://free-airtime.onrender.com/) may not work as I may disable the airtime topup feature since it consumes my AT wallet credit. 

## Technologies Used

- Flask
- Africa's Talking Airtime API
- Stripe API

## Testing The Application Locally

- Clone this repo:

    ```python
    $ git clone git@github.com:GitauHarrison/sending-free-airtime-after-purchase.git
    ```

- Change directory into the cloned folder:

    ```python
    $ cd sending-free-airtime-after-purchase
    ```

- Create and activate a virtual environment:

    ```python
    $ mkvirtualenv venv # using virtualenvwrapper
    ```

- Install project dependancies:

    ```python
    (venv)$ pip3 install -r requirements.txt
    ```

- Create and update a `.env` file to define environment variable values as seen in .`env-template`:

    ```python
    (venv)$ cp .env-template .env
    ```

- Run the application:

    ```python
    (venv)$ flask run
    ```

- Test the application in your favourite browser by pasting http://localhost:5000