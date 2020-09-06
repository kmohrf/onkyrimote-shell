from kien import CommandError, CommandResult, create_commander, var
from kien.transformation import to_enum

from onkyrimote.protocol import ChannelControl, PowerControl, VolumeControl
from onkyrimote.device.onkyo import TXSR304

command = create_commander("onkyo", "Controls an Onkyo Receiver")


@command("onkyo", is_abstract=True, inject=["onkyo"])
def onkyo():
    pass


@command(
    "volume", var("operation", choices=("up", "down", "mute", "unmute")), parent=onkyo
)
def volume(onkyo: VolumeControl, operation):
    {
        "up": onkyo.volume_up,
        "down": onkyo.volume_down,
        "mute": onkyo.mute,
        "unmute": onkyo.unmute,
    }[operation]()
    yield CommandResult("OK")


@command("power", var("state", choices=("on", "off")), parent=onkyo)
def power(onkyo: PowerControl, state):
    {"on": onkyo.power_on, "off": onkyo.power_off}[state]()
    yield CommandResult("OK")


@command("channel", var("channel", choices=TXSR304.Channel), parent=onkyo)
@command.transform(channel=to_enum(TXSR304.Channel))
def channel(onkyo: ChannelControl, channel):
    try:
        onkyo.set_channel(channel)
    except ValueError as exc:
        raise CommandError("Unsupported channel") from exc
    yield CommandResult("OK")
