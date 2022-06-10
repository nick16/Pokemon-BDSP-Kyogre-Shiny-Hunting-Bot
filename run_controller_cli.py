#!/usr/bin/env python3

import argparse
import asyncio
import logging
import os, signal

from aioconsole import ainput

from joycontrol import logging_default as log, utils

from joycontrol.controller import Controller
from joycontrol.controller_state import button_push
from joycontrol.memory import FlashMemory
from joycontrol.protocol import controller_protocol_factory
from joycontrol.server import create_hid_server

from shiny_hunter import checkColor
import subprocess
logger = logging.getLogger(__name__)


async def kill_process_by_name(target_process):
    subprocesses = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
    output, error = subprocesses.communicate()
    
    for line in output.splitlines():
        if target_process in str(line):
            pid = int(line.split(None, 1)[0])
            os.kill(pid, signal.SIGKILL)

async def shiny_hunt(controller_state):
    if controller_state.get_controller() != Controller.PRO_CONTROLLER:
        raise ValueError('This script only works with the Pro Controller!')

    # Waits until controller is fully connected
    await controller_state.connect()

    await ainput(prompt='Make sure the Switch is in the Home menu and press <enter> to continue.')
    i = 0  # Used to keep track of resets but resets to zero every time script stops.
    while True:
        print('reset number', i)
        # Press A Button
        await button_push(controller_state, 'a')
        await button_push(controller_state, 'a')
        print('PRESSED a')
        await asyncio.sleep(.5)

        # Press Up Button to avoid downloading game update, if your game has a pending update.
        '''
        await button_push(controller_state, 'up')
        await button_push(controller_state, 'up')
        print('PRESSED up')
        await asyncio.sleep(.5)
        '''

        # Press A Button
        await button_push(controller_state, 'a')
        await button_push(controller_state, 'a')
        print('PRESSED a')
        await asyncio.sleep(2)

        # Press A Button to choose profile
        await button_push(controller_state, 'a')
        await button_push(controller_state, 'a')
        print('PRESSED a to start game')
        await asyncio.sleep(24)

        # Press A Button
        await button_push(controller_state, 'a')
        await button_push(controller_state, 'a')
        print('PRESSED a')
        await asyncio.sleep(4)

        # Press A Button on start screen
        await button_push(controller_state, 'a')
        await button_push(controller_state, 'a')
        print('PRESSED a on start screen')
        await asyncio.sleep(12)

        # Press A Button to encounter pokemon
        await button_push(controller_state, 'a')
        await button_push(controller_state, 'a')
        print('PRESSED a to encounter pokemon')
        await asyncio.sleep(1)

        # Press A
        await button_push(controller_state, 'a')
        await button_push(controller_state, 'a')
        print('PRESSED a')
        await asyncio.sleep(11)
        
        # Restart OBS to reduce the amount of OBS freezes
        await kill_process_by_name('obs')
        print('restarting obs')
        await asyncio.sleep(.5)
        os.system('gnome-terminal -- obs')
        await asyncio.sleep(7.1)  # Wait for shiny animation + pokemon to be still on screen

        check_pokemon = checkColor(724,279)  # Precise coordinates of screen where Kyogre is for the longest.
        if check_pokemon == 'not_shiny':
            # press Home Button
            await button_push(controller_state, 'home')
            await button_push(controller_state, 'home')
            print('PRESSED home')
            await asyncio.sleep(1)

            # Press X Button
            await button_push(controller_state, 'x')
            await button_push(controller_state, 'x')
            print('PRESSED x')
            await asyncio.sleep(.5)

            # Press A Button to close game
            await button_push(controller_state, 'a')
            await button_push(controller_state, 'a')
            print('PRESSED a')
            await asyncio.sleep(1.5)
            i += 1
        elif check_pokemon == 'shiny':
            break
        elif check_pokemon == 'stuck':
            # If we determine that we are in the Switch settings, we press Back until we are hovering over the game
            for _ in range(6):
                await button_push(controller_state, 'b')
                await asyncio.sleep(1)


async def _main(args):
    # parse the spi flash
    if args.spi_flash:
        with open(args.spi_flash, 'rb') as spi_flash_file:
            spi_flash = FlashMemory(spi_flash_file.read())
    else:
        # Create memory containing default controller stick calibration
        spi_flash = FlashMemory()

    # Get controller name to emulate from arguments
    controller = Controller.from_arg(args.controller)

    with utils.get_output(path=args.log, default=None) as capture_file:
        # prepare the the emulated controller
        factory = controller_protocol_factory(controller, spi_flash=spi_flash)
        ctl_psm, itr_psm = 17, 19
        transport, protocol = await create_hid_server(factory, reconnect_bt_addr=args.reconnect_bt_addr,
                                                      ctl_psm=ctl_psm,
                                                      itr_psm=itr_psm, capture_file=capture_file,
                                                      device_id=args.device_id)

        controller_state = protocol.get_controller_state()
        await shiny_hunt(controller_state)


if __name__ == '__main__':
    # check if root
    if not os.geteuid() == 0:
        raise PermissionError('Script must be run as root!')

    # setup logging
    #log.configure(console_level=logging.ERROR)
    log.configure()

    parser = argparse.ArgumentParser()
    parser.add_argument('controller', help='JOYCON_R, JOYCON_L or PRO_CONTROLLER')
    parser.add_argument('-l', '--log')
    parser.add_argument('-d', '--device_id')
    parser.add_argument('--spi_flash')
    parser.add_argument('-r', '--reconnect_bt_addr', type=str, default=None,
                        help='The Switch console Bluetooth address, for reconnecting as an already paired controller')
    parser.add_argument('--nfc', type=str, default=None)
    args = parser.parse_args()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        _main(args)
    )
    
