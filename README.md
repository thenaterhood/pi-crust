Pi Crust
===============
A collection of wrappers to make working with the Raspberry Pi GPIO
interface more efficient.

To install, clone or download the repository and run `python setup.py install`.

Raspi Parallel GPIO
---------------
This class provides a parallel output on an array of pins, as well as
an array of parallel input.  The pins for both sides are stored in
arrays and can be changed and even made the same, if your hardware
setup makes that a safe thing to do.  When the Rx function is called,
the class fills its data slot "register" with the boolean values of
the pins defined as input, which can then be read as an array.  The Rx
function does not take any arguments.  The Tx function transmits or sends
data over the pins defined as output in parallel.  No clock is used
as it isn't necessary in this case.

The Tx function takes an integer as an argument, which is then converted
into an array of boolean values (binary) and the pins of output are set
accordingly.  If the resulting binary number does not fit in the array
of pins, the number is output from least significant to most significant
bit until the output is full, and the error field of the class is set
to true.  No warnings or failures are produced by over-filling the output
other than that.  The class does not accept a size, as it relies on the
length of the array of pins it has at its disposal for output.

Usage:

The parallel class gives each input and output its own pin, so keep
that in mind while building hardware that you're using this with.

	from pi_crust import ParallelIO
	gpioInterface = ParallelIO( )

	Sending/Receiving:
	gpioInterface.Rx() # Retrieve the state of the array of input pins
	gpioInterface.Tx( integer ) # Send data over the array of output pins

Alternatively, a command line utility is provided for "on the fly" usage:

	$ picrust-parallel <integer to send>


Raspi Bus GPIO
---------------
This class provides a bus interface to output (for now, it still reads
input in parallel).  The Rx function functions identical to the one
in the Raspi Binary GPIO.  The Tx function is called the same way although
it does operate differently.  Rather than iterating through an array
of output and outputting on each pin, it iterates through the array of
output and outputs it to one pin, cycles the clock on another pin so
the value is read in (if using something like a shift register), then
iterates to the next value.  The class can be initialized with a size
as well, so that the class will be aware of when to stop sending data.  
The size defaults to 8 bits.

The class is initialized in a different way than the parallel one.  It
requires one argument, the pin to output data on.  For a clock, it defaults
to pin 23, although that can be set via an argument as well.  The clock
is somewhat makeshift and the implementation of that will likely change in
the future.

This implementation uses fewer pins, so may be the better choice depending
what you happen to be doing.  Be aware that it is also subject to heavier
changes, since it was mainly hacked together.

Usage:

The bus class uses two pins (per instance of the class) to provide a data
output and a clock signal.  For building hardware that requires a ton of
outputs, this is probably the best class to use.  If used with a mux,
controlling multiple groups of hardware individually would be possible
using only a few more pins to control mux output (probably best done
in parallel, using an instance of the parallel wrapper in addition to this
one.)

	from pi_crust import BusIO
	gpioInterface = BusIO( output pin, clock pin, output size )

	Defaults:
	gpioInterface = BusIO( output pin )

	Sending/Receiving:
	gpioInterface.Rx() # Retrieve data from the array of input pins
	gpioInterface.Tx( integer ) # Send data over the output pin

Alternatively, a command line utility is provided for "on the fly" usage:

	$ picrust-bus <integer to send> <pin to send over>

LICENSE
------------

Licensed under the BSD license. See LICENSE for full license text.

Though not required by the license terms, please consider contributing,
providing feedback, or simply dropping a line to say that this software
was useful to you.

thenaterhood/pi-crust (c) 2012-2013 Nate Levesque (TheNaterhood), [www.thenaterhood.com](http://www.thenaterhood.com)
