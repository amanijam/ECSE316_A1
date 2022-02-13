import struct 

class Packet_Decoder:

    def __init__(self, packet, id):
        self.data = packet
        self.expected_id = struct.unpack(">H", id)[0]
        self.packet_size = 0

    def decode_header(self):
        id, flags, qdcount, ancount, nscount, arcount = struct.unpack(">HHHHHH", self.data[:12])
        bin_flags = bin(flags)
        qr = bin_flags[0]
        aa = bin_flags[5]
        tc = bin_flags[6]
        ra = bin_flags[8]
        rcode = int(bin_flags[12:16])

        if rcode == 1:
            return 1
        elif rcode == 2:
            return 2
        elif rcode == 3:
            return 3
        elif rcode == 4:
            return 4
        elif rcode == 5:
            return 5

        if self.expected_id != id:
            return 8
        
        if ancount == 0 and arcount == 0:
            return 7 
        
        if qr != 1:
            return 9

        self.packet_size += 12
        
        return 0


    def decode_question(self):
        question_data = self.data[self.packet_size:]
        num_vals = question_data[0]
        address = ""
        index = 0
        more_vals = True
        while more_vals:
            for _ in range(num_vals):
                index += 1
                self.packet_size += 1
                address += chr(question_data[index])
            index += 1
            self.packet_size += 1
            num_vals = question_data[index]
            if num_vals == 0:
                more_vals = False
            else:
                address += "."

        qtype = struct.unpack(">H", question_data[index: index+2])
        self.packet_size += 4
        return address

    def decode_answer(self):
        answer_data = self.data[self.packet_size+1:]

        type, ans_class, ttl, rdlength = struct.unpack(">HHIH", answer_data[2:12])
        index = 12
        if type == 1:
            rdata = ""
            for i in range(rdlength):
                rdata += str(struct.unpack(">B", answer_data[index:index+1])[0])
                if i != rdlength-1:
                    rdata += "."
                index += 1
        else:
            if type == 15:
                index += 2
            response_data = self.data[index:]
            num_vals = response_data[0]
            rdata = ""
            index = 0
            more_vals = True
            while more_vals:
                for _ in range(num_vals):
                    index += 1
                    self.packet_size += 1
                    rdata += chr(response_data[index])
                index += 1
                self.packet_size += 1
                num_vals = response_data[index]
                if num_vals == 0:
                    more_vals = False
                else:
                    rdata += "."


    def decode_packet(self):
        self.decode_header()
        self.qname = self.decode_question()
        self.decode_answer()
        # decode_additional()
        return True

    # def decode_question(data):

    # def decode_answer(data):

    # def decode_additional(data):



# if __name__ == "__main__":
#     data = b'\xbc\xf7\x81\x01\x00\x00\x00\x00\x00\x00\x00\x00'
#     decode_packet(data)
