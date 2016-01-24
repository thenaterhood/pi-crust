import sys
from pi_crust import ParallelIO, BusIO

def do_parallel():
    if ( len( sys.argv ) < 2 ):
        instance = ParallelIO()
        print( "Current state of parallel input pins is:" )
        instance.Rx()
        print( instance.register )
    else:
        instance = ParallelIO()
        try:
            int( sys.argv[1] )
        except:
            raise RuntimeError
        instance.Tx( int( sys.argv[1] ) )
        print( "Sent data" )

def do_bus():
    if ( len( sys.argv ) < 2 ):
        instance = BusIO( 5 )
        print( "Current state of parallel input pins is:" )
        instance.Rx()
        print( instance.register )
    else:
        try:
            int( sys.argv[1] )
            int( sys.argv[2] )
        except:
            raise RuntimeError
        instance = BusIO( int( sys.argv[2] ) )

        instance.Tx( int( sys.argv[1] ) )
        print( "Sent data" )
