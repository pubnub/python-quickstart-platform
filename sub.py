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
            os._exit(0)
        else:
            print("{}: {}".format(event.message["entry"], event.message["update"]))
        
        print
        pass

    def presence(self, pubnub, event):
        print("[PRESENCE: {}]".format(event.event))
        print("uuid: {}, channel: {}".format(event.uuid, event.channel))
        print
        pass

    def status(self, pubnub, event):
        if event.category == PNStatusCategory.PNConnectedCategory:
            print("[STATUS: PNConnectedCategory]")
            print("connected to channels: {}".format(event.affected_channels))
            print
        
        pass

pubnub.add_listener(MySubscribeCallback())
pubnub.subscribe().channels(CHANNEL).with_presence().execute()

print
print("***************************************************")
print("* Waiting for updates to The Guide about {}... *".format(ENTRY))
print("***************************************************")
print