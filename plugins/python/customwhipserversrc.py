from gi.repository import GObject, Gst


class CustomWhipServerSrc(Gst.Bin):
    __gstmetadata__ = (
        "CustomWhipServerSrc",
        "Source/Network/WebRTC",
        "Custom WHIP Server Source",
        "radio-aktywne",
    )

    __gsttemplates__ = Gst.PadTemplate.new(
        "audio_%u",
        Gst.PadDirection.SRC,
        Gst.PadPresence.SOMETIMES,
        Gst.Caps.from_string("audio/x-raw(ANY); application/x-rtp; audio/x-opus"),
    )

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._min = None
        self._max = None

        self._whip = Gst.ElementFactory.make("whipserversrc", "whip")
        self._signaller = self._whip.get_property("signaller")

        # Needed due to https://gitlab.gnome.org/GNOME/pygobject/-/issues/605
        self._agent = None

        self.add(self._whip)

        self._whip.connect("pad-added", self._on_pad_added)
        self._whip.connect("pad-removed", self._on_pad_removed)
        self._signaller.connect("webrtcbin-ready", self._on_webrtcbin_ready)

    @GObject.Property(
        type=str,
        nick="Address",
        blurb="Address to listen on",
    )
    def address(self) -> str | None:
        return self._signaller.get_property("host-addr")

    @address.setter
    def address(self, value: str) -> None:
        self._signaller.set_property("host-addr", value)

    @GObject.Property(
        type=str,
        nick="STUN server",
        blurb="STUN server to use",
    )
    def stun(self) -> str | None:
        return self._whip.get_property("stun-server")

    @stun.setter
    def stun(self, value: str) -> None:
        self._whip.set_property("stun-server", value)

    @GObject.Property(
        type=int,
        nick="Minimum RTP port",
        blurb="Minimum RTP port for the ICE agent",
        minimum=0,
        maximum=65535,
    )
    def min(self) -> int:
        if self._agent is not None:
            self._min = self._agent.get_property("min-rtp-port")

        return self._min

    @min.setter
    def min(self, value: int) -> None:
        if self._agent is not None:
            self._agent.set_property("min-rtp-port", value)
            self._min = self._agent.get_property("min-rtp-port")
        else:
            self._min = value

    @GObject.Property(
        type=int,
        nick="Maximum RTP port",
        blurb="Maximum RTP port for the ICE agent",
        minimum=0,
        maximum=65535,
    )
    def max(self) -> int:
        if self._agent is not None:
            self._max = self._agent.get_property("max-rtp-port")

        return self._max

    @max.setter
    def max(self, value: int) -> None:
        if self._agent is not None:
            self._agent.set_property("max-rtp-port", value)
            self._max = self._agent.get_property("max-rtp-port")
        else:
            self._max = value

    def _on_pad_added(
        self, element: Gst.Element, pad: Gst.Pad, *args, **kwargs
    ) -> None:
        """Handle the pad-added signal from the whipserversrc element."""

        ghost_pad = Gst.GhostPad.new(pad.get_name(), pad)
        self.add_pad(ghost_pad)

    def _on_pad_removed(
        self, element: Gst.Element, pad: Gst.Pad, *args, **kwargs
    ) -> None:
        """Handle the pad-removed signal from the whipserversrc element."""

        ghost_pad = self.get_static_pad(pad.get_name())
        self.remove_pad(ghost_pad)

    def _on_webrtcbin_ready(
        self,
        self_obj: Gst.Object,
        peer_id: str,
        webrtcbin: Gst.Element,
        *args,
        **kwargs
    ) -> None:
        """Handle the webrtcbin-ready signal from the signaller."""

        self._agent = webrtcbin.get_property("ice-agent")

        if self._min is not None:
            self._agent.set_property("min-rtp-port", self._min)

        if self._max is not None:
            self._agent.set_property("max-rtp-port", self._max)


__gstelementfactory__ = ("customwhipserversrc", Gst.Rank.NONE, CustomWhipServerSrc)
