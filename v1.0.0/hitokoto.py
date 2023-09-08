import json
import urllib.request as web

from mcdreforged.api.all import *

PLUGIN_METADATA = {
    "id": "mcdr_hitokoto",
    "version": "1.0.0",
    "name": "Hitokoto",
    "description": "Enjoy sentences from hitokoto in a server. ",
    "author": "dodo939",
    "link": "https://github.com/yfydodo939",
    "dependencies": {
       "mcdreforged": ">=2.0.0-alpha.1"
    }
}

types = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l']
types_text = {'a': "动画", 'b': "漫画", 'c': "游戏", 'd': "文学", 'e': "原创", 'f': "来自网络", 'g': "其他", 'h': "影视", 'i': "诗词", 'j': "网易云", 'k': "哲学", 'l': "抖机灵"}


def yy(context: PlayerCommandSource):
    server = context.get_server()
    info = context.get_info()
    datas = json.loads(web.urlopen("https://v1.hitokoto.cn/").read().decode("utf-8"))
    sentence = datas["hitokoto"]
    _type = types_text[datas["type"]]
    server.say(RText("§7[一言 " + _type + "]").set_click_event(RAction.open_url, "https://hitokoto.cn/").set_hover_text("https://hitokoto.cn/") + " " + RText("§3" + sentence).set_click_event(RAction.copy_to_clipboard, sentence).set_hover_text("点击复制到剪切板"))


def yy_type(context: PlayerCommandSource):
    server = context.get_server()
    info = context.get_info()
    _type = int(context.get_info().content.split()[1])
    if _type > 11 or _type < 0:
        server.say("§7[一言] §4没有对应类型! ")
        return
    sentence = web.urlopen("https://v1.hitokoto.cn/?encode=text&c=" + types[_type]).read().decode("utf-8")
    _type = types_text[types[_type]]
    server.say(RText("§7[一言 " + _type + "]").set_click_event(RAction.open_url, "https://hitokoto.cn/").set_hover_text("https://hitokoto.cn/") + " " + RText("§3" + sentence).set_click_event(RAction.copy_to_clipboard, sentence).set_hover_text("点击复制到剪切板"))


def yy_help(context: PlayerCommandSource):
    server = context.get_server()
    info = context.get_info()
    server.reply(info, "§2-------- hitokoto v1.0.0 --------")
    server.reply(info, RText("§7!!yy§r").set_click_event(RAction.suggest_command, "!!yy") + " 获取一句随机类型文案")
    server.reply(info, RText("§7!!yy §6<type: int>§r").set_click_event(RAction.suggest_command, "!!yy ") + " 获取一句指定类型文案")
    server.reply(info, RText("§7!!yy help§r").set_click_event(RAction.suggest_command, "!!yy help") + " 显示此帮助列表")
    server.reply(info, "§8类型对应整数: 0-动画 1-漫画 2-游戏 3-文学 4-原创 5-来自网络 6-其他 7-影视 8-诗词 9-网易云 10-哲学 11-抖机灵")


def on_load(server: ServerInterface, old):
    builder = SimpleCommandBuilder()
    builder.command("!!yy", yy)
    builder.command("!!yy help", yy_help)
    builder.command("!!yy <type>", yy_type)
    
    builder.arg("type", Integer)
    
    builder.register(server)
