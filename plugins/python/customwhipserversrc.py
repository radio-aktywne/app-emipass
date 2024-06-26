import gi

gi.require_version("GObject", "2.0")
gi.require_version("Gst", "1.0")
gi.require_version("GstWebRTC", "1.0")

from gi.repository import GObject, Gst, GstWebRTC  # noqa: E402


class CustomWhipServerSrc(Gst.Bin):
    __gstmetadata__ = (
        "CustomWhipServerSrc",
        "Source/Network/WebRTC",
        "Custom WHIP Server Source",
        "radio-aktywne",
    )

    _min: int | None
    _max: int | None
    _whip: Gst.Element
    _signaller: GObject.GInterface
    _webrtcbin: Gst.Element | None
    _agent: GstWebRTC.WebRTCICE | None

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._min = None
        self._max = None
        self._whip = self._setup_whip()
        self._signaller = self._setup_signaller()
        self._webrtcbin = None
        self._agent = None

    def _setup_whip(self) -> Gst.Element:
        whip = Gst.ElementFactory.make_with_properties(
            "whipserversrc",
            ["audio-codecs", "video-codecs"],
            [Gst.ValueArray(["OPUS"]), Gst.ValueArray([])],
        )

        self.add(whip)

        templates = whip.get_pad_template_list()
        for template in templates:
            self.add_pad_template(template)

        whip.connect("pad-added", self._on_pad_added)
        whip.connect("pad-removed", self._on_pad_removed)

        return whip

    def _setup_signaller(self) -> Gst.Element:
        signaller = self._whip.get_property("signaller")

        signaller.connect("webrtcbin-ready", self._on_webrtcbin_ready)

        return signaller

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

    @GObject.Property(
        type=str,
        nick="Codec",
        blurb="Codec to use",
    )
    def codec(self) -> str:
        codecs = self._whip.get_property("audio-codecs")
        return codecs[0]

    @codec.setter
    def codec(self, value: str) -> None:
        self._whip.set_property("audio-codecs", Gst.ValueArray([value]))

    def _on_pad_added(
        self, element: Gst.Element, pad: Gst.Pad, *args, **kwargs
    ) -> None:
        """Handle the pad-added signal from the whipserversrc element."""

        name = pad.get_name()
        ghost_pad = Gst.GhostPad.new(name, pad)
        self.add_pad(ghost_pad)

    def _on_pad_removed(
        self, element: Gst.Element, pad: Gst.Pad, *args, **kwargs
    ) -> None:
        """Handle the pad-removed signal from the whipserversrc element."""

        name = pad.get_name()
        ghost_pad = self.get_static_pad(name)
        self.remove_pad(ghost_pad)

    def _on_webrtcbin_ready(
        self,
        signaller: Gst.Object,
        peer_id: str,
        webrtcbin: Gst.Element,
        *args,
        **kwargs,
    ) -> None:
        """Handle the webrtcbin-ready signal from the signaller."""

        self._webrtcbin = webrtcbin
        self._agent = self._webrtcbin.get_property("ice-agent")

        if self._min is not None:
            self._agent.set_property("min-rtp-port", self._min)

        if self._max is not None:
            self._agent.set_property("max-rtp-port", self._max)


__gstelementfactory__ = ("customwhipserversrc", Gst.Rank.NONE, CustomWhipServerSrc)
