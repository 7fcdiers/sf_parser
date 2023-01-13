def mk_bullet(list: list) -> str:
    start_bullet = "<li><p>"
    end_bullet = "</p></li>"

    return end_bullet.join(start_bullet + val for val in list) + end_bullet

