# PubNub Python Sample App

This repository contains the files required to run the [PubNub Python Quickstart](https://www.pubnub.com/docs/platform/quickstarts/python).

PubNub takes care of the infrastructure and APIs needed for the realtime communication layer of your application. Work on your app's logic and let PubNub handle sending and receiving data across the world in less than 100ms.

## Get keys

You will need publish and subscribe keys to authenticate your app. Get your keys from the [Admin Portal](https://dashboard.pubnub.com/login).

## Set up the project

If you don't want to copy the code from this document, you can clone the repository and use the files in there.
   
1. Create a new folder for your Python scripts.

2. In that folder, create two files named `pub.py` and `sub.py`.

3. Install the PubNub Python SDK using `pip`:

    ```text
    pip install pubnub
    ```

## Add project files

If you don't want to copy the code from this document, you can clone the repository and use the files in there.

1. Open the `pub.py` file and add the following code. Remember to also replace the _myPublishKey_ and _mySubscribeKey_ placeholders with your keys.

    ```python
    from pubnub.callbacks import SubscribeCallback
    from pubnub.enums import PNStatusCategory
    from pubnub.pnconfiguration import PNConfiguration
    from pubnub.pubnub import PubNub

    ENTRY = "Earth"
    CHANNEL = "the_guide"
    the_update = None

    # replace the key placeholders with your own PubNub publish and subscribe keys
    pnconfig = PNConfiguration()
    pnconfig.publish_key = "myPublishKey"
    pnconfig.subscribe_key = "mySubscribeKey"
    pnconfig.uuid = "serverUUID-PUB"

    pubnub = PubNub(pnconfig)

    print("*****************************************")
    print("* Submit updates to The Guide for Earth *")
    print("*     Enter 42 to exit this process     *")
    print("*****************************************")

    while the_update != "42":
        the_update = input("Enter an update for Earth: ")
        the_message = {"entry": ENTRY, "update": the_update}
        envelope = pubnub.publish().channel(CHANNEL).message(the_message).sync()

        if envelope.status.is_error():
            print("[PUBLISH: fail]")
            print("error: %s" % envelope.status.error)
        else:
            print("[PUBLISH: sent]")
            print("timetoken: %s" % envelope.result.timetoken)
    ```

2. Open the `sub.py` file and add the following code. Remember to also replace the _myPublishKey_ and _mySubscribeKey_ placeholders with your keys.

    ```python
    import os

    from pubnub.callbacks import SubscribeCallback
    from pubnub.enums import PNStatusCategory
    from pubnub.pnconfiguration import PNConfiguration
    from pubnub.pubnub import PubNub

    ENTRY = "Earth"
    CHANNEL = "the_guide"

    # replace the key placeholders with your own PubNub publish and subscribe keys
    pnconfig = PNConfiguration()
    pnconfig.publish_key = "myPublishKey"
    pnconfig.subscribe_key = "mySubscribeKey"
    pnconfig.uuid = "serverUUID-SUB"

    pubnub = PubNub(pnconfig)

    class MySubscribeCallback(SubscribeCallback):
        def message(self, pubnub, event):
            print("[MESSAGE received]")

            if event.message["update"] == "42":
                print("The publisher has ended the session.")
                exit(0)
            else:
                print("{}: {}".format(event.message["entry"], event.message["update"]))

        def presence(self, pubnub, event):
            print("[PRESENCE: {}]".format(event.event))
            print("uuid: {}, channel: {}".format(event.uuid, event.channel))
            print()

        def status(self, pubnub, event):
            if event.category == PNStatusCategory.PNConnectedCategory:
                print("[STATUS: PNConnectedCategory]")
                print("connected to channels: {}".format(event.affected_channels))
                print()

    pubnub.add_listener(MySubscribeCallback())
    pubnub.subscribe().channels(CHANNEL).with_presence().execute()

    print()
    print("***************************************************")
    print("* Waiting for updates to The Guide about {}... *".format(ENTRY))
    print("***************************************************")
    print()
    ```

## Run the app

You first need to start the subcribe process to see the updates you want to publish.

1. Open the terminal and run the subscribe script by calling `python sub.py`.

    You should see a message that the script is waiting for updates. The subscriber process is implemented to receive updates from the publisher process, so you don't need any further input here.

2. In a new terminal window, run the publish script by calling `python pub.py`.

    You should see a message that informs you how to exit the process and a prompt that awaits your next update.

    When you're finished submitting entries, enter `42` to exit the publisher script. This operation also forces the subscriber script to exit.

## Documentation

* [Build your first realtime Python app with PubNub](https://www.pubnub.com/docs/platform/quickstarts/python)
* [API reference for Python](https://www.pubnub.com/docs/python/pubnub-python-sdk)

## Support

If you **need help** or have a **general question**, contact support@pubnub.com.
