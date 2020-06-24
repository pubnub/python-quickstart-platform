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

print
print("*****************************************")
print("* Submit updates to The Guide for Earth *")
print("*     Enter 42 to exit this process     *")
print("*****************************************")

while the_update != "42":
    print
    the_update = raw_input("Enter an update for Earth: ")
    the_message = {"entry": ENTRY, "update": the_update}
    envelope = pubnub.publish().channel(CHANNEL).message(the_message).sync()

    if envelope.status.is_error():
        print("[PUBLISH: fail]")
        print("error: %s" % status.error)
        pass
    else:
        print("[PUBLISH: sent]")
        print("timetoken: %s" % envelope.result.timetoken)
        pass
