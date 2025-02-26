import zmq
from loguru import logger
import rovercom
from bootinfo import Service

CONTEXT = zmq.Context()



class ServiceStream:
    def __init__(self, address : str, sock_type : zmq.Socket):
        self.address = address # zmq address
        self.socket = None # initialized as None, before lazy loading
        self.sock_type = sock_type
        self.bytes = 0 # amount of bytes read/written so far




class WriteStream:
    def __init__(self, stream : ServiceStream):
        self.stream = stream
    
    # Initial setup of the stream (done lazily, on the first write)
    def _initialize(self):
        s = self.stream

        # already  initialized
        if s.socket is not None:
            return None
        
        try:
            #create a new socket
            socket = CONTEXT.socket(s.sock_type)
            socket.bind(s.address)
        except zmq.ZMQError as e:
            if socket:
                socket.close()
            return f"Failed to create/bind write socket at {s.address}: {str(e)}"
        
        s.socket = socket
        s.bytes = 0
        return None
    
    # Write byte data to the stream
    def WriteBytes(self, data : bytes):
        s = self.stream

        if s.socket is None:
            
            err = self._initialize()

            if err:
                return f"Error during initialization: {str(err)}"

        # Check if the socket writable
        if s.sock_type != zmq.PUB:
            return "Cannot write to a read-only stream"
        
        try:
            # Write the data
            s.socket.send(data)
        except zmq.ZMQError as e:
            return f"Failed to write to stream: {str(e)}"
        
        if isinstance(data, (bytes, str)):
            s.bytes += len(data)
        else:
            s.bytes += 1 


        return None
    
    # Write a rovercom sensor output message to the stream
    def Write(self, output : rovercom.SensorOutput):
        if output is None:
            return "Cannot write nil output"
        
        try:
            # Convert to over-the-wire format
            buf = output.SerializeToString()
        except Exception as e:
            return f"Failed to serialize sensor data: {str(e)}"    

        # Write the data
        return self.WriteBytes(buf)

class ReadStream:
    def __init__(self, stream : ServiceStream):
        self.stream = stream

    # initial setup of the stream (done lazily, on the first read) 
    def _initialize(self):
        s = self.stream

        # Already initialized
        if s.socket is not None:
            return None
        
        try:
            # Create a new socket
            socket = CONTEXT.socket(s.sockType)
            socket.connect(s.address)
            socket.setsockopt_string(zmq.SUBSCRIBE, "")
        except zmq.ZMQError as e:
            if socket:
                socket.close()
            return f"Failed to create/connect/subscribe read socket at {s.address}: {str(e)}"
        
        s.socket = socket
        s.bytes = 0
        return None
    
    # Read byte data from the stream
    def ReadBytes(self):
        s = self.stream

        if s.socket is None:

            err = self._initialize()
            if err:
                return None, f"Error during initialization: {str(err)}"
        
        # Check if the socket is readable
        if s.sock_type != zmq.SUB:
            return None, f"Cannot write to a read-only stream"
        
        try:
            # Read the data
            data = s.socket.recv()
        except zmq.ZMQError as e:
            return None, f"failed to read from stream: {str(e)}"

        s.bytes += len(data)
        return data, None
    
    # Read a rovercom sensor output message from the stream
    def Read(self):
        # Read the Data
        buf, err = self.ReadBytes()

        if err is not None:
            return None, err
        
        try:
            # Convert from over-the-wire format
            output = rovercom.SensorOutput().parse(buf)
        except Exception as e:
            return None, f"Failed to parse sensor data: {str(e)}"
        
        return output, None


# Map of all already handed out streams to the user program (to preserve singletons)
write_streams : dict[str, WriteStream] = {}
read_streams : dict[str, ReadStream] = {}



# Get a stream that you can write to (i.e. an output stream).
# This function returns None if the stream does not exist.
def GetWriteStream(self : Service, name : str):
    # Is this stream already handed out?
    if name in write_streams:
        return write_streams[name]
    
    # Does this stream exist?
    for output in self.outputs:
        if output.name == name:
            # ZMQ wants to bind write streams to tcp://*:port addresses, so if roverd gave us a localhost, we need to change it to *
            address = output.address.replace("localhost", "*", 1)
            
            # Create a new stream
            stream = ServiceStream(address, zmq.PUB)

            res = WriteStream(stream)
            write_streams[name] = res  
            return res
    
    logger.critical("Output stream %s does not exist. Update your program code or service.yaml" % name)
    return None


# Get a stream that you can read from (i.e. an input stream).
# This function returns None if the stream does not exist.
def GetReadStream(self : Service, service : str, name : str):
    stream_name = f"{service}-{name}"

    # Is this stream already handed out?
    if stream_name in read_streams:
        return read_streams[stream_name]
    
    # Does this stream exist
    for input in self.inputs:
        if input.service == service:
            for stream in input.streams:
                if stream.name == name:
                    
                    # Create a new stream
                    stream = ServiceStream(stream.address, zmq.SUB)

                    res = ReadStream(stream)
                    read_streams[stream_name] = res  
                    return res
    
    logger.critical("Input stream %s does not exist. Update your program code or service.yaml" % stream_name)
    return None


# Attach to Service object
Service.GetWriteStream = GetWriteStream
Service.GetReadStream = GetReadStream
        