# Mailgun Forwarder

This simple function adds another layer of forwarding in Mailgun. Currently, it's possible to have wildcards on the recipient filters, but it's only possible to forward to a single email. *Or to a URL*.

This guide was made focused on macOS, but should work just fine in most Linux flavors as well. For Windows, Google is your friend. In the end, it makes very little difference, as the final goal is to have it running in the cloud.

## Requirements

- Python 3 (I used 3.8.1)
- Mailgun account and API key
- Google Cloud Platform account
- (optional) [ngrok](https://ngrok.com) for local testing

## Google Cloud Platform

There are several sources on how to create and configure a GCP account, and even to use the free tier. I won't get into details because it's not the goal of this project. But create an account, a project and go to Cloud Functions to create the new function. Give it any name you want, allow unauthenticated requests (living on the edge) and set the language to Python 3.7 (or 3.8 Beta, I'm using it and works just fine).

At this point, even if you didn't actually create the function, you probably already have an URL that will trigger it. Copy this somewhere and leave this tab open.

## Mailgun

In a separate tab, [generate an API key in Mailgun](https://app.mailgun.com/app/account/security/api_keys) and save it somewhere.

Now, [create a Receiving route](https://app.mailgun.com/app/receiving/routes/new), set the expression type to Match Recipient and in the Recipient field enter `.*@<YOUR_DOMAIN_HERE>`. Obviously, replace the `<YOUR_DOMAIN_HERE>` part with your domain. In the Forward section, enter the URL that you saved from your Cloud Function. If you have other rules, set this one to be the highest priority value (so, last to be executed) and be sure to stop other rules before reaching this one. Look for the Stop checkmark in the other rules.

## Configuration

Clone the repo, create a virtualenv, activate it and install the required libraries:

```bash
$ git clone https://github.com/mauodias/mailgun-forwarder.git
$ cd mailgun-forwarder
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
```

After that is done, create two environment variables with the Mailgun API key and another one with a destination inbox.

NOTE: I'm using this single destination inbox because, in the end, I want to make some preprocessing in the email, but then send it to a single location. Feel free to adjust it the way you prefer.
```
$ export MAILGUN_TOKEN=<your_fancy_token_comes_here>
$ export DESTINATION_INBOX="<the_destination@email>"
```

This is enough to run the project locally.

## Running Locally

Open two terminal screens, one for the function and another one to ngrok, to create a public URL for your test server.

For ngrok:
```bash
$ ngrok http --bind-tls=true 8000
```
`--bind-tls=true` forces HTTPS only

For the function:
```bash
$ gunicorn app:app
```

Now, to test if the function works correctly, go to the [Receiving](https://app.mailgun.com/app/receiving/routes) section in Mailgun and try to send a sample post to the URL that ngrok is showing. If everything is working, you'll receive an email in the destination inbox you configured above.

## Moving to the Cloud

Go back to the tab where you were creating the Cloud Function. Scroll to the bottom and expand `Environment Variables, Networking, Timeouts and More`. In that section, create the same environment variables with the same values that you used above, for the local test.

Then, copy the contents of the `main.py` file from your local environment and paste it in the code editor in GCP. Click on `requirements.txt` and do the same.

To finish, click `Deploy` and wait until the grey circle becomes a green checkmark. After that, you can send emails to arbitrary users under your domain, and they'll be forwarded to your destination inbox.
