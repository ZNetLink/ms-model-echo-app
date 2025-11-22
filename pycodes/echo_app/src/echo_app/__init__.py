import ipaddress
import logging
from typing import Optional

import miaosuan as ms
from miaosuan.engine.engine import INTRPT_TYPE_SELF, INTRPT_TYPE_STRM


logger = logging.getLogger(__name__)

ECHO_APP_PACKET_FORMAT = "echo_app"
ECHO_APP_DEFAULT_REMOTE_PORT = 8100
ECHO_APP_DEFAULT_LOCAL_PORT = 8900


@ms.process_model("echo_app")
class EchoAppProcess:
    def __init__(self) -> None:
        self.role: Optional[str] = None
        self.dest_addr: Optional[int] = None

    @ms.state_enter("wait", begin=True)
    def enter_wait(self) -> None:
        ms.intrpt_schedule_self(ms.sim_time() + 0.1, 0)

    @ms.state_enter("init")
    def enter_init(self) -> None:
        module = ms.self_obj()
        if module is None:
            raise RuntimeError("EchoApp: missing module context during init")

        role = module.get_attr_string("role")
        if role not in {"client", "server"}:
            raise ValueError("EchoApp: role attribute must be 'client' or 'server'")
        self.role = role

        dest_str = module.get_attr_string("dest")
        try:
            self.dest_addr = int(ipaddress.IPv4Address(dest_str))
        except ipaddress.AddressValueError as exc:
            raise ValueError(f"EchoApp: invalid dest IPv4 address: {dest_str!r}") from exc

        self.register_udp_app()
        ms.intrpt_schedule_self(ms.sim_time() + 5.0, 0)


    @ms.state_enter("idle")
    def enter_idle(self) -> None:
        if self.role == "client" and ms.intrpt_type() == INTRPT_TYPE_SELF:
            ms.intrpt_schedule_self(ms.sim_time() + 1.0, 0)

    @ms.state_exit("idle")
    def exit_idle(self) -> None:
        intr_type = ms.intrpt_type()

        if intr_type == INTRPT_TYPE_SELF:
            if self.role == "client" and self.dest_addr is not None:
                message = f"Hello from client: {ms.sim_time():.6f}"
                self.send_pkt(self.dest_addr, message)
        elif intr_type == INTRPT_TYPE_STRM:
            stream_index = ms.intrpt_strm()
            packet = ms.pk_get(stream_index)
            pkt_format = ms.pk_format(packet)
            if pkt_format != ECHO_APP_PACKET_FORMAT:
                logger.warning("EchoApp: received unexpected packet format %s", pkt_format)
                return

            ici = ms.intrpt_ici()
            src_addr: Optional[int] = None
            if ici is not None:
                try:
                    src_addr = ici.get_int("remote address")
                except Exception:
                    logger.warning("EchoApp: missing remote address in ICI")

            data = ms.pk_nfd_get_string(packet, "data")
            logger.debug("EchoApp: received data %s", data)
            if self.role == "server" and src_addr is not None:
                self.send_pkt(src_addr, f"Echo: {data}")
        else:
            logger.warning("EchoApp: received unexpected interrupt type %s", intr_type)
            
    @ms.transition("wait", "init")
    def transition_init_idle(self) -> bool:
        return True
    
    @ms.transition("init", "idle")
    def transition_idle_init(self) -> bool:
        return True
    
    @ms.transition("idle", "idle")
    def transition_idle_idle(self) -> bool:
        return True

    def send_pkt(self, dst_addr: int, data: str) -> None:
        packet = ms.pk_create_fmt(ECHO_APP_PACKET_FORMAT)
        ms.pk_nfd_set_string(packet, "data", data)
        ms.pk_stamp(packet)

        ici = ms.ici_create("udp_ind")
        ici.set_int("remote address", int(dst_addr))
        ici.set_int("remote port", ECHO_APP_DEFAULT_REMOTE_PORT)
        ici.set_int("local port", ECHO_APP_DEFAULT_LOCAL_PORT)

        ms.ici_install(ici)
        ms.pk_send(packet, 0)
        ms.ici_install(None)

    def register_udp_app(self) -> None:
        module = ms.self_obj()
        if module is None:
            raise RuntimeError("EchoApp: missing module context when registering UDP app")

        ici = ms.ici_create("udp_command")
        ici.set_string("command", "listen")
        ici.set_int("app module id", module.get_id())
        ici.set_int("local port", ECHO_APP_DEFAULT_REMOTE_PORT)

        out_streams = ms.get_out_streams()
        try:
            udp_stream = next(iter(out_streams.values()))
        except StopIteration as exc:
            raise RuntimeError("EchoApp: UDP output stream not configured") from exc

        ms.ici_install(ici)
        ms.intrpt_schedule_remote(ms.sim_time(), 0, udp_stream.dst)
        ms.ici_install(None)

