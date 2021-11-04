# other_files
Place for files that are important enough to show them (eg. related with interview process) but don't deserve its own repository.

Written with Pycharm and Python 3.9.2.

[web socket commit note: ](https://github.com/NieznanywInternetach/other_files/commit/7f9caddd01129bf79914735f2a7e698d7cba8830 "The commit")
* made for linux server as a try to bypass a particular restriction
* client.py is meant to send a [pickle](https://github.com/python/cpython/blob/main/Lib/pickle.py)d SQL request to the server using mixed-length header (fixed part determines lenght of the variable part which includes all information needed to decode the message)
* server.py recieves the request and checks if it's correct (and makes prompt about the status) and the database's response. If all's correct, sends back requested data

Notes for other scripts included at the beginning of the files
