# -*- coding: utf-8 -*-

# これは、スキルビルダーのハンドラークラスを使用した実装の
# アプローチにより作成された単純なHello WorldのAlexaスキルです。
import logging

from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.utils import is_intent_name, is_request_type
from ask_sdk_model import Response
from ask_sdk_model.ui import SimpleCard

sb = SkillBuilder()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@sb.request_handler(can_handle_func=is_request_type("LaunchRequest"))
def launch_request_handler(handler_input):
    """スキルを起動するハンドラーです。"""
    # type: (HandlerInput) -> Response
    speech_text = "ようこそ、アレクサスキルキットへ。こんにちは、と言ってみてください。"

    return handler_input.response_builder.speak(speech_text).set_card(
        SimpleCard("ハローワールド", speech_text)).set_should_end_session(
        False).response


@sb.request_handler(can_handle_func=is_intent_name("HelloWorldIntent"))
def hello_world_intent_handler(handler_input):
    """ハローワールドインテント用ハンドラー。"""
    # type: (HandlerInput) -> Response
    speech_text = "デコレーターを使ったPythonの世界へようこそ。"

    return handler_input.response_builder.speak(speech_text).set_card(
        SimpleCard("ハローワールド", speech_text)).set_should_end_session(
        True).response


@sb.request_handler(can_handle_func=is_intent_name("AMAZON.HelpIntent"))
def help_intent_handler(handler_input):
    """Helpインテントのハンドラー。"""
    # type: (HandlerInput) -> Response
    speech_text = "こんにちは。と言ってみてください。"

    return handler_input.response_builder.speak(speech_text).ask(
        speech_text).set_card(SimpleCard(
            "ハローワールド", speech_text)).response


@sb.request_handler(
    can_handle_func=lambda handler_input:
        is_intent_name("AMAZON.CancelIntent")(handler_input) or
        is_intent_name("AMAZON.StopIntent")(handler_input))
def cancel_and_stop_intent_handler(handler_input):
    """CancelおよびStopインテントの単一ハンドラー。"""
    # type: (HandlerInput) -> Response
    speech_text = "さようなら"

    return handler_input.response_builder.speak(speech_text).set_card(
        SimpleCard("ハローワールド", speech_text)).response


@sb.request_handler(can_handle_func=is_intent_name("AMAZON.FallbackIntent"))
def fallback_handler(handler_input):
    """
    このハンドラーは、サポートされていないロケールではトリガーされません。
    そのため、どのロケールでも安全にデプロイできます。
    """
    # type: (HandlerInput) -> Response
    speech = (
        "ハローワールドスキルは、お手伝いできません。"
        "こんにちは。と言ってみてください。")
    reprompt = "こんにちは。と言ってみてください。"
    handler_input.response_builder.speak(speech).ask(reprompt)
    return handler_input.response_builder.response


@sb.request_handler(can_handle_func=is_request_type("SessionEndedRequest"))
def session_ended_request_handler(handler_input):
    """セッション終了のハンドラー。"""
    # type: (HandlerInput) -> Response
    return handler_input.response_builder.response


@sb.exception_handler(can_handle_func=lambda i, e: True)
def all_exception_handler(handler_input, exception):
    """すべての例外ハンドラーを取得し、例外をログに記録して、
    カスタムメッセージで応答します。
    """
    # type: (HandlerInput, Exception) -> Response
    logger.error(exception, exc_info=True)

    speech = "申し訳ありません。問題が発生しました。後でもう一度試してください。"
    handler_input.response_builder.speak(speech).ask(speech)

    return handler_input.response_builder.response


handler = sb.lambda_handler()