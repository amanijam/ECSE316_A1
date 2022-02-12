import struct 

class Packet_Decoder:

    def __init__(self, packet, id):
        self.data = packet
        self.expected_id = struct.unpack(">H", id)[0]

    def decode_header(self):
        id, flags1, flags2, ancount, nscount, arcount = struct.unpack(">HBBHHHH", self.data)
        # if self.expected_id != id:
        #     exit(99)
        if flags1 < 2048 or self.expected_id != id:
            exit(99)
        
        if flags2 != 0: 
            exit(99)
        # Check the RCODE
        # Check the QDCount
        # Check the ANCount
        #
        
        return True


    def decode_question(self):
        question_data = self.data[96:]
        num_letters = question_data[0]
        address = ""
        for i in range(num_letters):
            address += chr(question_data[i+1])

        print(address)

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
