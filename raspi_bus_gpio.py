"""
Author: Nate Levesque <public@thenaterhood.com>
Language: Python3
Filename: raspi_bus_gpio.py
Description:
    Manages working with the pi output pins as a bus.  Uses two pins,
    one to provide a clock and another to transfer data.  Reads pins
    in parallel.
"""
import RPi.GPIO as io
from time import sleep

class gpio():
    """
    Manages IO for the raspberry pi GPIO a register.
    """
    __slots__=('register', 'error', 'inpins', 'outpins', 'debug', 'clock', 'size')
    
    def __init__( self, outpin, clock=23, size=8 ):
        """
        Constructs the class with either the input
        """
        io.setmode(io.BOARD)
        # Whether to print variables as they're created, for debug
        # purposes
        self.debug = False
        
        # Defines the input and output pins to use
        self.inpins = [3, 5, 7, 11, 13, 15, 19, 21, 23]
        self.outpins = outpin
        self.clock = clock
        self.size = size
            
    def Rx( self ):
        """
        Checks the state of an array of gpio input pins defined in
        self.inpins and sets the class register slot to the contained
        data.
        
        Arguments:
            none
        """
        RxData = []
        # Setting up and retrieving the state of each pin
        for pin in self.inpins:
            io.setup(pin, io.IN)
            RxData.append( io.input(pin) )
            
        self.register = RxData
            
        if self.debug:
            print( self )
            
        
    def Tx( self, data ):
        """
        Sets the array of pins defined in self.outpins to the binary
        representation of an integer (data).  Sets the class error
        field to True if there was an error (the integer did not fit
        in the number of bits)
        
        Arguments: 8, 10
            data (int): an integer to send
        """
        # Converts the input to an array of True and False that
        # represents the binary 1 and 0 bits of the binary number
        self.register = self.createBinArray( self.DecToBinString( data ) )
        if self.debug:
            print( self )
            
        # Iterates backwards through the binary data
        # and outputs it over the designated output pin and cycles
        # the clock once for each time it outputs.
        i = 0
        while i < len( self.register ) and i < self.size:
            # Configures the pins
            io.setup( self.outpins, io.OUT )
            io.setup( self.clock, io.OUT )
            
            # Sends the data
            io.output( self.outpins, self.register[i] )
            
            # Cycles the clock
            io.output( self.clock, True )
            sleep(.00001)
            io.output( self.clock, False )
            sleep(.00001)
            
            i += 1
        
        # Checks to see if the number fit in the number of output
        # pins and sets the error field to True if it did not    
        if ( len( self.register ) > self.size ):
            self.error = True
        
        self.error = False
               
    def DecToBinString( self, integer ):
        """
        Returns a string of the binary representation
        of an integer.
        
        Arguments:
            integer (int): an integer
        Returns:
            (str): the string of the binary rep of the integer
        """
        return bin(integer)[2:]
        
    def createBinArray( self, binary ):
        """
        Creates a binary array from a string of 1's and 0's
        
        Arguments:
            binary (str): a string representation of a binary number
        Returns:
            binArray (list): a list of boolean values that represent
                the binary number
        """
        binArray = []
        
        for digit in binary:
            if ( digit == '0' ):
                binArray.append( False )
            if ( digit == '1' ):
                binArray.append( True )
                
        while len( binArray ) < self.size:
            binArray.insert(0, False)
                
        return binArray
        
    def __del__( self ):
        """
        Cleans up the gpio interface when the instance of the class
        is deleted
        """
        # Clear the output on the hardware
        self.Tx( 0 )
        
        # Clean up the GPIO interface
        io.cleanup()
        
    def __str__( self ):
        """
        Returns a graphical representation of the bits stored
        in the class's 'register' field.
        """
        r = ''
        for bit in self.register:
            if ( bit ):
                r = r + "@"
            else:
                r = r + "o"
        return r
        
if __name__ == "__main__":
    import sys
    if ( len( sys.argv ) < 2 ):
        instance = gpio( 5 )
        print( "Current state of parallel input pins is:" )
        instance.Rx()
        print( instance.register )
    else:
        try:
            int( sys.argv[1] )
            int( sys.argv[2] )
        except:
            raise RuntimeError
        instance = gpio( int( sys.argv[2] ) )

        instance.Tx( int( sys.argv[1] ) )
        print( "Sent data" )
