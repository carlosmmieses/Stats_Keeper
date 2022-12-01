from os import stat
from stat_keeper.stat_keeper import StatKeeper
from sys import argv

if __name__ == "__main__":
    # We initiate a connection to setup the database
        # in case it does not exist
    init_stat_keeper = StatKeeper()
    init_stat_keeper.setup()
        # We start the workflow to read all PDFs in the PDF folder and 
        # add the info to the database in case the file was not scanned already
    stat_keeper = StatKeeper()
    stat_keeper.run()
    
    # We check for the arguments to see how to proceed
    # if any([(lambda x: x in argv)(x) for x in ["-a", "--all"]]):
    #     # We initiate a connection to setup the database
    #     # in case it does not exist
    #     init_stat_keeper = StatKeeper()
    #     init_stat_keeper.setup()
    #     # We start the workflow to read all PDFs in the PDF folder and 
    #     # add the info to the database in case the file was not scanned already
    #     stat_keeper = StatKeeper()
    #     stat_keeper.run()