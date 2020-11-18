# sockexpect

Provides expect/pexpect style functionality for sockets.

<span id="SockExpect">class **SockExpect**</span>([builtins.object](builtins.html#object))


`Provides expect/pexpect style functionality for sockets. `


Methods defined here:

<span id="SockExpect-__init__">**\_\_init\_\_**</span>(self, s:socket.socket, eol:bytes=b'\\r\\n')  

Required parameters:
   s: a socket object. A timeout must be set for the expect() function to work properly. If s.gettimeout() == None, it will be set to DEFAULT_TIMEOUT.
      
Optional parameter:
    eol: bytes to use for end of line in sendline().`

<!-- -->

<span id="SockExpect-expect">**expect**</span>(self, regexp:Union\[bytes, Pattern\[~AnyStr\]\])  

Receive and save data from socket until the given regexp is matched, a timeout occurs, or the socket is closed. Data is read in chunks of size up to self.maxchunksize before being checked for a regexp match, so the buffer may contain data send by the server after the regexp match. Raises an exception on timeout error or socket close. On success, self.before will be equal to data received up to the start of the matched expression, and self.after will be equal to the matched expression and any data received afterwards. The of self.after is retained between calls, and matching is applied to data previously received. On failure, self.after will be equal to all data received appended to the value of self.after on entry. Both self.after and self.before are bytearray objects.

<!-- -->

<span id="SockExpect-send">**send**</span>(self, msg:bytes)  
`Send raw bytes to socket.`

<!-- -->

<span id="SockExpect-sendline">**sendline**</span>(self, line:bytes)  
`Send raw bytes to socket terminated by self.eol.`

------------------------------------------------------------------------

 
**Data**
 

**DEFAULT\_CHUNKSIZE** = 4096

**DEFAULT\_MAXBUFFSIZE** = 16384

**DEFAULT\_TIMEOUT** = 1.0
