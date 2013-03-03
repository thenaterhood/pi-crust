Pi Crust
===============
A collection of wrappers to make working with the Raspberry Pi GPIO
interface more efficient.

Contents
---------------
	raspi_parallel_gpio			Works with parallel arrays of IO pins
	raspi_bus_gpio				Provides a bus interface via one pin
	
Raspi Binary GPIO
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
other than that.

Raspi Bus GPIO
---------------
This class provides a bus interface to output (for now, it still reads 
input in parallel).  The Rx function functions identical to the one 
in the Raspi Binary GPIO.  The Tx function is called the same way although 
it does operate differently.  Rather than iterating through an array 
of output and outputting on each pin, it iterates through the array of 
output and outputs it to one pin, cycles the clock on another pin so 
the value is read in (if using something like a shift register), then 
iterates to the next value.  Since there is no limit to the output as far 
as the software is concerned, the function will output until the transmit 
array is empty.

The class is initialized in a different way than the parallel one.  It
requires one argument, the pin to output data on.  For a clock, it defaults
to pin 23, although that can be set via an argument as well.  The clock
is somewhat makeshift and the implementation of that will likely change in 
the future.

This implementation uses fewer pins, so may be the better choice depending 
what you happen to be doing.  Be aware that it is also subject to heavier 
changes, since it was mainly hacked together.

LICENSE
------------

thenaterhood/basically-ti-basic repository (c) 2012-2013 Nate Levesque (TheNaterhood), [www.thenaterhood.com](www.thenaterhood.com)

[![Creative Commons License](http://i.creativecommons.org/l/by-sa/3.0/88x31.png)](http://creativecommons.org/licenses/by-sa/3.0/)

TL;DR: You can use, copy and modify this SO LONG AS you credit me and distribute your remixes with the same license.

This work is licensed under the [Creative Commons Attribution-ShareAlike 3.0 Unported License](http://creativecommons.org/licenses/by-sa/3.0/).

You should have received a copy of the license along with this
work. To view a copy of this license, visit http://creativecommons.org/licenses/by-sa/3.0/ or send
a letter to Creative Commons, 444 Castro Street, Suite 900, Mountain View, California, 94041, USA.
