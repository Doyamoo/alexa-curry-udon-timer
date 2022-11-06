import logging
from typing import Collection

from ask_sdk.standard import StandardSkillBuilder
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.utils import is_intent_name, is_request_type
from ask_sdk_model import Response
from ask_sdk_model.ui import SimpleCard

sb = StandardSkillBuilder()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@sb.request_handler(can_handle_func=is_request_type("LaunchRequest"))
def launch_request_handler(handler_input: HandlerInput) -> Response:
    """スキルを起動するハンドラー"""

    permissions = handler_input.request_envelope.context.system.user.permissions
    logger.info(permissions)

    if not (permissions and permissions.consent_token):
        # TODO パーミッションがない場合の処理
        logger.info("パーミッションなし")
    else:
        # タイマーをセットする
        logger.info("パーミッションあり")
        logger.info(permissions.consent_token)

        timer1 = {
            "duration": "PT3M",
            "timerLabel": "タイマー1",
            "creationBehavior": {"displayExperience": {"visibility": "VISIBLE"}},
            "triggeringBehavior": {
                "operation": {
                    "type": "ANNOUNCE",
                    "textToAnnounce": [
                        {"locale": "ja-JP", "text": "火を止めて、スープの素を入れてください。"}
                    ],
                },
                "notificationConfig": {"playAudible": True},
            },
        }

        timer2 = {
            "duration": "PT5M",
            "timerLabel": "タイマー2",
            "creationBehavior": {"displayExperience": {"visibility": "VISIBLE"}},
            "triggeringBehavior": {
                "operation": {
                    "type": "ANNOUNCE",
                    "textToAnnounce": [{"locale": "ja-JP", "text": "料理完了です。"}],
                },
                "notificationConfig": {"playAudible": True},
            },
        }

        try:
            logger.info("タイマー作成開始")

            timer_service_client = (
                handler_input.service_client_factory.get_timer_management_service()
            )
            timer_response = timer_service_client.create_timer(timer1)
            logger.info(timer_response)

            timer_response = timer_service_client.create_timer(timer2)
            logger.info(timer_response)

        except Exception as e:
            logger.error("タイマー作成エラー", e)

    speech_text = "カレーうどんのタイマーを開始します。"

    return (
        handler_input.response_builder.speak(speech_text)
        .set_card(SimpleCard("カレーうどんのタイマー", speech_text))
        .set_should_end_session(False)
        .response
    )


@sb.request_handler(can_handle_func=is_intent_name("HelloWorldIntent"))
def hello_world_intent_handler(handler_input: HandlerInput) -> Response:
    """ハローワールドインテント用ハンドラー。"""
    speech_text = "デコレーターを使ったPythonの世界へようこそ。"

    return (
        handler_input.response_builder.speak(speech_text)
        .set_card(SimpleCard("ハローワールド", speech_text))
        .set_should_end_session(True)
        .response
    )


@sb.request_handler(can_handle_func=is_intent_name("AMAZON.HelpIntent"))
def help_intent_handler(handler_input: HandlerInput) -> Response:
    """Helpインテントのハンドラー。"""
    speech_text = "こんにちは。と言ってみてください。"

    return (
        handler_input.response_builder.speak(speech_text)
        .ask(speech_text)
        .set_card(SimpleCard("ハローワールド", speech_text))
        .response
    )


@sb.request_handler(
    can_handle_func=lambda handler_input: is_intent_name("AMAZON.CancelIntent")(
        handler_input
    )
    or is_intent_name("AMAZON.StopIntent")(handler_input)
)
def cancel_and_stop_intent_handler(handler_input: HandlerInput) -> Response:
    """CancelおよびStopインテントの単一ハンドラー。"""
    speech_text = "さようなら"

    return (
        handler_input.response_builder.speak(speech_text)
        .set_card(SimpleCard("ハローワールド", speech_text))
        .response
    )


@sb.request_handler(can_handle_func=is_intent_name("AMAZON.FallbackIntent"))
def fallback_handler(handler_input: HandlerInput) -> Response:
    """
    このハンドラーは、サポートされていないロケールではトリガーされません。
    そのため、どのロケールでも安全にデプロイできます。
    """
    speech = "ハローワールドスキルは、お手伝いできません。" "こんにちは。と言ってみてください。"
    reprompt = "こんにちは。と言ってみてください。"
    handler_input.response_builder.speak(speech).ask(reprompt)
    return handler_input.response_builder.response


@sb.request_handler(can_handle_func=is_request_type("SessionEndedRequest"))
def session_ended_request_handler(handler_input: HandlerInput) -> Response:
    """セッション終了のハンドラー。"""
    return handler_input.response_builder.response


@sb.exception_handler(can_handle_func=lambda i, e: True)
def all_exception_handler(
    handler_input: HandlerInput, exception: Exception
) -> Response:
    """すべての例外ハンドラーを取得し、例外をログに記録して、
    カスタムメッセージで応答します。
    """
    logger.error(exception, exc_info=True)

    speech = "申し訳ありません。問題が発生しました。後でもう一度試してください。"
    handler_input.response_builder.speak(speech).ask(speech)

    return handler_input.response_builder.response


handler = sb.lambda_handler()
