def pull(_git, branch, origin):
    out = f'{origin}/' if origin else ''
    return f'git pull {out}{branch}'

