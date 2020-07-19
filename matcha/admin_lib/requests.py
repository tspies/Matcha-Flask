from matcha.common_lib.query import query_db


def admin_lib_get_block_requests():

    block_requests = query_db("SELECT * FROM blocked_accounts")

    return block_requests