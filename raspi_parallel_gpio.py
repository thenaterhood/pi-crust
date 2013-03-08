"""
Author: Nate Levesque <public@thenaterhood.com>
Language: Python3
Filename: raspi_parallel_gpio.py
Description:
    contains a class for reading/writing from the raspberry pi
    GPIO pins as two 8-bit arrays, like in assembly.  Note that
    this is designed (originally) for writing/reading 8-bit arrays
    of switches or LEDs "in one shot" but if the hardware is designed
    using shift registers, it could also be used to display data on an
    8xN LED display.
    
    The class requires integers which are then converted to binary
    in 8 bits.  If the output results in more than 8 bits, the program
    will display up to the first 8, and set its error field to True.
    If the output fits in the output array, then the error field is set
    to false.  Retrieving data does not set the error field.
    
    The class treats (as it was easier to wire it this way in my
    setup) the GPIO pins as one side of the connector is output and
    the other side is input.  In the setup section this is more clear
    as it includes pin numbers.  This can be changed by changing
    what pins are listed in the inpins and outpins (and if it's safe in
    your setup, they can be the same thing)
"""
import RPi.GPIO as io

class gpio():
    """
    Manages IO for the raspberry pi GPIO as two 8-bit registers.
    This may expand to 16 bit both ways, but for my purposes right now,
    8 bit is fine and with my setup it's safer to use it as two separate
    registers.
    
    """
    __slots__=('register', 'error', 'inpins', 'outpins', 'debug')
    
    def __init__( self ):
        """
        Constructs the class with either the input
        """
        io.setmode(io.BOARD)
        # Whether to print variables as they're created, for debug
        # purposes
        self.debug = False
        self.register = []
        
        # Defines the input and output pins to use
        self.inpins = [3, 5, 7, 11, 13, 15, 19, 21, 23]
        self.outpins = [8, 10, 12, 16, 18, 22, 24, 26]
            
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
        
        Arguments:
            data (int): an integer to send
        """
        # Converts the input to an array of True and False that
        # represents the binary 1 and 0 bits of the binary number
        self.register = self.createBinArray( self.DecToBinString( data ) )
        if self.debug:
            print( self )
            
        # Iterates backwards through the binary data (LSB -> MSB)
        # and outputs it over the designated output pins
        i = len( self.outpins ) - 1
        while i >= 0:
            io.setup( self.outpins[i], io.OUT )
            io.output( self.outpins[i], self.register[i] )
            i -= 1
        
        # Checks to see if the number fit in the number of output
        # pins and sets the error field to True if it did not    
        if ( len( self.outpins ) < len( self.register ) ):
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
                
        while len( binArray ) < 8:
            binArray.insert(0, False)
                
        return binArray
        
    def __del__( self ):
        """
        Cleans up the gpio interface when the instance of the class
        is deleted
        """
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
        instance = gpio()
        print( "Current state of parallel input pins is:" )
        instance.Rx()
        print( instance.register )
    else:
        instance = gpio()
        try:
            int( sys.argv[1] )
        except:
            raise RuntimeError
        instance.Tx( int( sys.argv[1] ) )
        print( "Sent data" )
    
