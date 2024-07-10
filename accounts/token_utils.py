# token_utils.py

def is_valid_token_format(token):
    # Add your validation logic here
    # For example, you might check if the token is a string and has a specific length
    if isinstance(token, str) and len(token) == 64:
        return True
    return False
