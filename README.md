# hackathon t3chfest2017

## Bot devolped at t3chfest's hackathon.

Only need to register a bot, set the bridge IP and go!

*Usage*:

`python telegrambot.py`

*Funcionality*:

Telegram bot to control the lighting system.

* The bot interacts with the Twitter API to receive and send tweets.

  * Recognition of the language (API Twitter) -> flag of the country.

  * Analyze feelings -> lights in green (+) / red (-) / white

    * English
    * Spanish


* Send mails depending on the state in which the device is, if an unexpected change occurs an email will be received.

* Various additional features such as:
  * Turn on 1 / all lights.
  * Turn off 1 / all lights.
  * Turn on the lights as flags.
  * Turn the lights on randomly.

  # Schema of bot

  ![Schema](/images/scheme.png)


  # Architecture

  ![Architecture](/images/arch.png)
