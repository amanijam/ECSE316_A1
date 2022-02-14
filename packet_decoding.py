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
        _, response.name = self.decode_name(12)
        self.packet_size += 4
        return 0

    def decode_answer(self, response):
        answer_data = self.data[self.packet_size+1:]
        original_total = self.packet_size+1
        index = 0
        for i in range(response.num_answers):
            if answer_data[index] == 192:
                _, type, ans_class, ttl, rdlength = struct.unpack(">HHHIH", answer_data[index: index + 12])
                index += 12
            else:
                index, _ = self.decode_name(index)
                index += 1
                type, ans_class, ttl, rdlength = struct.unpack(">HHIH", answer_data[index: index + 10])
                index += 10
            if ans_class != 1:
                return 10
            response.type.append(type)
            response.ttl.append(ttl)
            index, rdata = self.decode_record(rdlength, type, answer_data, index)
            response.answer.append(rdata)
        self.packet_size = index + original_total
        return 0
    
    def decode_record(self, rdlength, type, data, index):
        rdata = ""
        if type == 1:
            for i in range(rdlength):
                rdata += str(struct.unpack(">B", data[index:index+1])[0])
                rdata += "."
                index += 1
        
        else:
            if type == 15:
                index += 2
                rdlength = rdlength - 2
            count = 0
            pointer_found = False
            for _ in range(rdlength):
                if count == 0:
                    if index >= len(data):
                        break
                    elif data[index] == 192:
                        pointer_found = True
                    elif pointer_found:
                        rdata += self.decode_name(data[index])[1]
                        pointer_found = False
                    else:
                        count = data[index]
                else:
                    rdata += chr(data[index])
                    count -= 1
                    if count == 0:
                        rdata += "."
                index += 1
        
        if len(rdata) != 0 and rdata[len(rdata) - 1] == ".":
            rdata = rdata[0:len(rdata) - 1]
        return [index, rdata]

    def decode_additional(self, response):
        additional_data = self.data[self.packet_size:]
        original_total = self.packet_size
        index = 0
        for i in range(response.num_additional):
            if additional_data[index] == 192:
                _, type, ans_class, ttl, rdlength = struct.unpack(">HHHIH", additional_data[index: index + 12])
                index += 12
            else:
                index, _ = self.decode_name(index)
                index += 1
                type, ans_class, ttl, rdlength = struct.unpack(">HHIH", additional_data[index: index + 10])
                index += 10
            if ans_class != 1:
                return 10
            if type != 1 and type != 2 and type != 5 and type != 15:
                pass
            response.type.append(type)
            response.ttl.append(ttl)
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
            elif num_vals == 192:
                index += 1
                name += "." + self.decode_name(name_data[index])[1]
                more_vals = False
            else:
                name += "."
    
        return [index, name]

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
