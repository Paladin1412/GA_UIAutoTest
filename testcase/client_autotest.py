import time

import MyTestAPI as nss


def client_test():
    nss.login_qq()
    nss.select_section(2)
    # high_debug()
    new_player = nss.enter_gamecenter()

    if new_player == 0:
        nss.skip_newer_tech()
        nss.exit_server()
        nss.enter_gamecenter()
        nss.dress()

    nss.auto_tuoguan()
    nss.random_start(0)
    time.sleep(130)
    nss.wait_room()


def relax_profile():
    nss.login_qq()
    nss.select_section(2)
    # high_debug()
    new_player = nss.enter_gamecenter()

    if new_player == 0:
        nss.skip_newer_tech()
        nss.exit_server()
        nss.enter_gamecenter()
        nss.dress()

    # nss.auto_tuoguan()
    nss.relax_land_run(1000)


def delte_account():
    nss.login_qq()
    nss.select_section(4)
    # high_debug()

    new_player = nss.enter_gamecenter()

    time.sleep(10)
    gm_str = ['svr deleteaccount']
    nss.gm_input(gm_str)


if __name__ == '__main__':
    nss.auto_tuoguan()
