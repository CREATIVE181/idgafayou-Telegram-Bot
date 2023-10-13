from CONFIG import easy_sql

async def find_id(message):
    try:
        if message.reply_to_message:
            return message.reply_to_message.from_user.id
        else:
            try:
                if len(message.entities) == 2:
                    return message.entities[1].user.id
                else:
                    return message.entities[0].user.id
            except Exception:
                for word in message.text.split():
                    if word[0] == '@':
                        try:
                            return easy_sql.select(f'SELECT id FROM users WHERE username = "{word[1:].lower()}"')[0]
                        except Exception:
                            return easy_sql.select(f'SELECT id FROM users WHERE id = {word[1:]}')[0]
                return False
    except Exception:
        return False
            
