from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.provider import ProviderRequest
from astrbot.api.star import Context, Star
from astrbot.api import AstrBotConfig

class LLLMWhitelistPlugin(Star):
    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)
        self.config = config

        # 群聊设置
        self.group_mode = config.get("group_mode", "disabled")
        self.group_whitelist = config.get("group_whitelist", [])
        self.group_blacklist = config.get("group_blacklist", [])

        # 私聊设置
        self.private_mode = config.get("private_mode", "disabled")
        self.private_whitelist = config.get("private_whitelist", [])
        self.private_blacklist = config.get("private_blacklist", [])

    @filter.on_llm_request()
    async def on_llm_request(self, event: AstrMessageEvent, req: ProviderRequest):
        """在调用 LLM 前拦截，根据群聊/私聊模式进行检查"""
        group_id = event.get_group_id()
        sender_id = event.get_sender_id()

        if group_id:
            # ── 群聊消息 ──
            if self.group_mode == "whitelist":
                if str(group_id) not in [str(g) for g in self.group_whitelist]:
                    event.stop_event()
                    return
            elif self.group_mode == "blacklist":
                if str(group_id) in [str(g) for g in self.group_blacklist]:
                    event.stop_event()
                    return
            # disabled: 不拦截，放行
        else:
            # ── 私聊消息 ──
            if self.private_mode == "whitelist":
                if str(sender_id) not in [str(u) for u in self.private_whitelist]:
                    event.stop_event()
                    return
            elif self.private_mode == "blacklist":
                if str(sender_id) in [str(u) for u in self.private_blacklist]:
                    event.stop_event()
                    return
            # disabled: 不拦截，放行
