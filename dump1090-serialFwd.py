#   >>> Serial Forward for dump1090 TCP Streams <<<
#   Copyright (C) 2018 by Juan Benitez <juan.a.benitez(at)gmail.com>
#   All rights reserved.
#
# * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# * "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# * LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# * A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# * HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# * SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# * LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# * DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# * THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# * OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# 

import socket, sys, argparse
from time import sleep
try:
    import serial
except ImportError:
    sys.exit(">> Pyserial not installed, please install via >> apt install python-serial")

# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("--host",   type=str, help="dump1090 IP address default: localhost", default='localhost')
parser.add_argument("--tcp",    type=int, help="TCP port to connect to default: 30003 (SBS-1)", default=30003)
parser.add_argument("--port",   type=str, help="Serial Port to use default: /dev/serial0", default="/dev/serial0")
parser.add_argument("--baud",   type=int, help="Serial Baudrate default: 115200", default=115200)
parser.add_argument("--delayed",type=str, help="Delay start in seconds (Cron use) default: None (0)", default=0)
args = parser.parse_args()

# Wait for network services to start
sleep(args.delayed)

# Setup serial port and TCP connection
ser = serial.Serial(args.port, baudrate=args.baud)
dump1090 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dump1090.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
dump1090.connect( (args.host, args.tcp) )

while True:
    try:
        payload = dump1090.recv(1024*64).rstrip().splitlines() # dump1090 outputs 64kb at a time
        for line in payload:
            print line
            ser.write(line)

    except KeyboardInterrupt:
        ser.close()
        dump1090.close()
        sys.exit("> TERMINATED BY USER")

    # If connection fails close and try again in 10 seconds
    except socket.error, errMSG:
        dump1090.close()
        sleep(10)
        dump1090.connect( (args.host, args.tcp) )
        
    except:
        pass
        

    
