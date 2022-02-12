import struct 

class Packet_Decoder:

    def __init__(self, packet, id):
        self.data = packet
        self.expected_id = struct.unpack(">H", id)[0]

    def decode_header(self):
        id, flags, qdcount, ancount, nscount, arcount = struct.unpack(">HHHHHH", self.data)
        # if self.expected_id != id:
        #     exit(99)
        if flags < 2048 or self.expected_id != id:
            exit(99)
        
        return True


    def decode_question(self):
        for part in self.data:
            print(part)

    def decode_packet(self):
        self.decode_header()
        self.decode_question()
        # decode_answer()
        # decode_additional()
        return True

    # def decode_question(data):

    # def decode_answer(data):

    # def decode_additional(data):



# if __name__ == "__main__":
#     data = b'\xbc\xf7\x81\x01\x00\x00\x00\x00\x00\x00\x00\x00'
#     decode_packet(data)
