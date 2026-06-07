from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.provider import ProviderRequest
from astrbot.api.star import Context, Star
from astrbot.api import AstrBotConfig

class LLLMWhitelistPlugin(Star):
    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)
        self.config = config
        # 从配置中读取白名单群ID列表
        self.whitelist_groups = config.get("whitelist_groups", [])
        
    @filter.on_llm_request()
    async def on_llm_request(self, event: AstrMessageEvent, req: ProviderRequest):
        """在调用 LLM 前拦截，检查群是否在白名单中"""
        group_id = event.get_group_id()
        # 如果当前是群聊，且该群不在白名单中，阻止 LLM 调用
        if group_id and group_id not in self.whitelist_groups:
            event.stop_event()  # 停止事件传播，不会调用 LLM
