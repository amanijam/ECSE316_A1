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
        tc = bin_flags[6]
        ra = bin_flags[8]
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
        question_data = self.data[12:]
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

        response.name = address
        self.packet_size += 4
        return 0

    def decode_answer(self, response):
        answer_data = self.data[self.packet_size+1:]
        print(self.data[self.packet_size+1:])
        type, ans_class, ttl, rdlength = struct.unpack(">HHIH", answer_data[2:12])
        if ans_class != 1:
            return 10
        response.type = type
        response.ttl = ttl
        index = 12
        if type == 1:
            rdata = ""
            for i in range(rdlength):
                rdata += str(struct.unpack(">B", answer_data[index:index+1])[0])
                if i != rdlength-1:
                    rdata += "."
                index += 1
            
            print(rdata)
        elif type == 2 or type == 5:
            rdata = ""
            for i in range(response.num_answers):
                rdata = ""
                num_vals = answer_data[index] 
                if num_vals == 192:
                    index += 1
                    index += answer_data[index] + 1
                    num_vals = answer_data[index]
                for _ in range(num_vals):
                    index += 1
                    rdata += chr(answer_data[index])
                    print(rdata)

                if i != (response.num_answers - 1):
                    index += 1
                
                response.answer.append(rdata)
        
        else:
            rdata = ""
            for i in range(response.num_answers):
                rdata = ""
                num_vals = answer_data[index] 
                if num_vals == 192:
                    index += 1
                    index += answer_data[index] + 1
                    num_vals = answer_data[index]
                while True:
                    for _ in range(num_vals):
                        index += 1
                        rdata += chr(answer_data[index])
                        print(rdata)
                    index += 1
                    num_vals = answer_data[index]
                    if num_vals == 0:
                        break
                    rdata += "."

                    # if i != (response.num_answers - 1):
                    #     index += 1
                    
                    # response.answer.append(rdata)

                

            # if type == 15:
            #     index += 2
            # response_data = answer_data[index:]
            # print(response_data)
            # num_vals = response_data[0]
            # rdata = ""
            # index = 0
            # more_vals = True
            # while more_vals:
            #     for _ in range(num_vals):
            #         index += 1
            #         self.packet_size += 1
            #         rdata += chr(response_data[index])
            #     index += 1
            #     self.packet_size += 1
            #     num_vals = response_data[index]
            #     if num_vals == 0:
            #         more_vals = False
            #     else:
            #         rdata += "."
        
        return 0

    def decode_packet(self):
        response = Response()
        self.decode_header(response)
        self.decode_question(response)
        self.decode_answer(response)
        # decode_additional()
        return True

    # def decode_question(data):

    # def decode_answer(data):

    # def decode_additional(data):



# if __name__ == "__main__":
#     data = b'\xbc\xf7\x81\x01\x00\x00\x00\x00\x00\x00\x00\x00'
#     decode_packet(data)
