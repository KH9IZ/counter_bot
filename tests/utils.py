import time

from telebot.types import (
    CallbackQuery,
    Chat,
    Message,
    User,
    Update,
)


def build_message(**kwargs):
    options = {}
    detected_content_type = 'text'
    for option, content_type in (
        ('text', 'text'),
        ('dice', 'dice'),
        ('reply_to_message', None),
    ):
        if (value := kwargs.get(option)):
            options[option] = value
        if content_type:
            detected_content_type = detected_content_type
    options = dict(
        text=kwargs.get('text'),
        dice=kwargs.get('dice'),
        reply_to_message=kwargs.get('reply_to'),
    )
    return Message(
        message_id=kwargs['message_id'],
        from_user=kwargs.get('from_user', build_user()),
        date=kwargs.get('date', time.time()),
        chat=kwargs.get('chat', build_chat()),
        content_type=kwargs.get('content_type') or detected_content_type,
        options=options,
        json_string='{}',
    )


def build_callback_query(callback_id, **kwargs):
    return CallbackQuery(
        id=callback_id,
        from_user=kwargs.get('from_user', build_user()),
        data=kwargs.get('data'),
        chat_instance=kwargs.get('chat', build_chat()),
        message=kwargs.get('message', build_message(message_id=1)),
        json_string='{}',
    )


def build_user(**kwargs):
    return User(
        id=kwargs.pop('id', 1),
        is_bot=kwargs.pop('is_bot', False),
        first_name=kwargs.pop('first_name', 'Tester'),
        **kwargs
    )


def build_chat(**kwargs):
    return Chat(
        id=kwargs.get('id', 1),
        type=kwargs.get('type', 'private'),
        **kwargs
    )


def build_update(**kwargs):
    return Update(
        update_id=kwargs['update_id'],
        message=kwargs.get('message'),
        edited_message=kwargs.get('edited_message'),
        channel_post=kwargs.get('channel_post'),
        edited_channel_post=None,
        inline_query=None,
        chosen_inline_result=None,      
        callback_query=kwargs.get('callback_query'),
        shipping_query=None,
        pre_checkout_query=None,
        poll=None,
        poll_answer=None,
        my_chat_member=None,
        chat_member=None,
        chat_join_request=None,
    )
