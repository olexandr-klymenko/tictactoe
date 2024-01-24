def err_resp(msg, reason, code):
    return {"error_reason": reason, "message": msg}, code
