import struct
from response import *

class Packet_Decoder:

    def __init__(self, packet, id):
        self.data = packet
        self.expected_id = struct.unpack(">H", id)[0]
        self.packet_size = 0

    def decode_header(self, response):
        id, flags, qdcount, ancount, nscount, arcount = struct.unpack(">HHHHHH", self.data[:12])
        bin_flags = bin(flags)[2:]
        qr = bin_flags[0]
        aa = bin_flags[5]
        rcode = int(bin_flags[12:16])
        if rcode != 0:
            return rcode

        if self.expected_id != id:
            return 8
        
        if ancount == 0 and arcount == 0:
            return 7 
        
        if qr != '1':
            return 9
        response.auth = aa
        response.id = id
        response.num_answers = ancount
        response.num_additional = arcount
        self.packet_size += 12
        
        return 0


    def decode_question(self, response):
        response.name = self.decode_name(12)
        self.packet_size += 4
        return 0

    def decode_answer(self, response):
        answer_data = self.data[self.packet_size+1:]
        original_total = self.packet_size+1
        index = 0
        for i in range(response.num_answers):
            name_pointer, type, ans_class, ttl, rdlength = struct.unpack(">HHHIH", answer_data[index: index + 12])
            if ans_class != 1:
                return 10
            response.type.append(type)
            response.ttl.append(ttl)
            index = index + 12
            index, rdata = self.decode_record(rdlength, type, answer_data, index)
            response.answer.append(rdata)
        self.packet_size = index + original_total
        return 0
    
    def decode_record(self, rdlength, type, data, index):
        rdata = ""
        if type == 1:
            for i in range(rdlength):
                rdata += str(struct.unpack(">B", data[index:index+1])[0])
                if i != rdlength-1:
                    rdata += "."
                index += 1
        
        else:
            if type == 15:
                index += 2
            count = 1
            while True:
                num_vals = data[index]
                if num_vals == 192:
                    index += 1
                    rdata += self.decode_name(data[index])
                    count += 2
                else:
                    for _ in range(num_vals):
                        index += 1
                        rdata += chr(data[index])
                        count += 1
                
                index += 1
                if count >= rdlength or data[index] == 0:
                    break
                else:
                    rdata += "."
        
        return [index, rdata]

    def decode_additional(self, response):
        additional_data = self.data[self.packet_size:]
        original_total = self.packet_size
        index = 0
        for i in range(response.num_additional):
            name_pointer, type, ans_class, ttl, rdlength = struct.unpack(">HHHIH", additional_data[index: index + 12])
            if ans_class != 1:
                return 10
            if type != 1 and type != 2 and type != 5 and type != 15:
                pass
            response.type.append(type)
            response.ttl.append(ttl)
            index = index + 12
            index, rdata = self.decode_record(rdlength, type, additional_data, index)
            response.additional.append(rdata)
        self.packet_size = index + original_total
            

    def decode_name(self, offset):
        name_data = self.data[offset:]
        num_vals = name_data[0]
        name = ""
        index = 0
        more_vals = True
        while more_vals:
            for _ in range(num_vals):
                index += 1
                self.packet_size += 1
                name += chr(name_data[index])
            index += 1
            self.packet_size += 1
            num_vals = name_data[index]
            if num_vals == 0:
                more_vals = False
            else:
                name += "."
        
        return name

    def decode_packet(self):
        response = Response()
        return_val = self.decode_header(response)
        if return_val == 0:
            return_val = self.decode_question(response)
            if return_val == 0 and response.num_answers != 0:
                self.decode_answer(response)
                if return_val == 0 and response.num_additional != 0:
                    self.decode_additional(response)
        return [return_val, response]

    # def decode_question(data):

    # def decode_answer(data):

    # def decode_additional(data):



# if __name__ == "__main__":
#     data = b'\xbc\xf7\x81\x01\x00\x00\x00\x00\x00\x00\x00\x00'
#     decode_packet(data)
