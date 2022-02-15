import struct
from response import *

class Packet_Decoder:

    def __init__(self, packet, id):
        self.data = packet
        self.expected_id = struct.unpack(">H", id)[0]
        self.packet_size = 0

    # This function is responsible for decoding the header portion of the packet
    def decode_header(self, response):
        id, flags, qdcount, ancount, nscount, arcount = struct.unpack(">HHHHHH", self.data[:12])
        bin_flags = bin(flags)[2:] # Converts the flags to binary
        qr = bin_flags[0] # If the packet is a response
        aa = bin_flags[5] # If the packet is authorized
        rcode = int(bin_flags[12:16]) # Any returned errors encountered 
        if rcode != 0: # If there is an error
            return rcode

        if self.expected_id != id: #If the id does not match the request id
            return 8
        
        if ancount == 0 and arcount == 0: # If there are no records
            return 7 
        
        if qr != '1': #If it is not a response packet
            return 9
        
        # Sets the attributes of the response
        response.auth = aa
        response.id = id
        response.num_answers = ancount
        response.num_additional = arcount
        self.packet_size += 12
        
        return 0


    #This function is responsible for decoding the question
    def decode_question(self, response):
        _, response.name = self.decode_name(12) #Retrieves name
        self.packet_size += 4 #To account for the last two sections of this section
        return 0

    #This function is responsible for decoding the answer records
    def decode_answer(self, response):
        answer_data = self.data[self.packet_size+1:]
        original_total = self.packet_size+1
        index = 0
        for i in range(response.num_answers):
            if answer_data[index] == 192: #If a pointer is found 
                # The size of the next 5 sections is known
                _, type, ans_class, ttl, rdlength = struct.unpack(">HHHIH", answer_data[index: index + 12])
                index += 12 # index is moved forward
            else: 
                index, _ = self.decode_name(index) # Retreives name at index position
                index += 1 # Moves on to the next byte
                # The size of the next 4 sections is known
                type, ans_class, ttl, rdlength = struct.unpack(">HHIH", answer_data[index: index + 10])
                index += 10 #index is moved forward
            if ans_class != 1: # if there is an incorrect class value
                return 10
            # adds to the response data
            response.type.append(type)
            response.ttl.append(ttl)
            # helper function is called to retrieve the record data
            index, rdata = self.decode_record(rdlength, type, answer_data, index)
            response.answer.append(rdata) # Answer is added to response
        self.packet_size = index + original_total # Changes the packet size depending on the size of the answer section (index represents this)
        return 0
    
    # This function is used to decode a record
    def decode_record(self, rdlength, type, data, index):
        rdata = ""
        if type == 1: # If it is an A record
            for _ in range(rdlength): # We know that it is just the next 4 bytes
                rdata += str(struct.unpack(">B", data[index:index+1])[0]) # concatenates part of IP value
                rdata += "."
                index += 1
        
        else:
            if type == 15: # If it is a MX record
                index += 2 # Skip the preference section
                rdlength = rdlength - 2 
            count = 0
            pointer_found = False
            # Goes through expected length of answer
            for _ in range(rdlength):
                if count == 0:
                    if index >= len(data): # If the end of the packet is reached
                        break
                    elif data[index] == 192: # If a pointer is found
                        pointer_found = True # Let the next iteration know to use the offset value (packet compression)
                    elif pointer_found: 
                        rdata += self.decode_name(data[index])[1] # The name is retreived using the offset value
                        pointer_found = False 
                    else: 
                        count = data[index] # Reload count of the number of upcoming values
                else:
                    rdata += chr(data[index]) # Add character regularely
                    count -= 1 
                    if count == 0: # If the end of this portion of the sequence is reached
                        rdata += "." 
                index += 1 # Moves to the next byte
        
        # To remove the last . in the rdata
        if len(rdata) != 0 and rdata[len(rdata) - 1] == ".":
            rdata = rdata[0:len(rdata) - 1]
        return [index, rdata] 

    # This function is used to decode the additional section
    def decode_additional(self, response):
        additional_data = self.data[self.packet_size:]
        original_total = self.packet_size
        index = 0
        for i in range(response.num_additional):
            if additional_data[index] == 192: # If a pointer is found
                # The next 5 section sizes is known
                _, type, ans_class, ttl, rdlength = struct.unpack(">HHHIH", additional_data[index: index + 12])
                index += 12 # Moves the index forwards
            else:
                index, _ = self.decode_name(index) # Retrieves name
                index += 1 # Moves to the next byte
                # The size of the next 4 sections is known
                type, ans_class, ttl, rdlength = struct.unpack(">HHIH", additional_data[index: index + 10])
                index += 10 # Moves the index forwards
            if ans_class != 1: # If there is a wrong value in the answer class
                return 10
            
            # If it is not a compatible type
            if type != 1 and type != 2 and type != 5 and type != 15:
                pass
            
            # Set response attributes
            response.type.append(type)
            response.ttl.append(ttl)
            # Retreive record
            index, rdata = self.decode_record(rdlength, type, additional_data, index)
            response.additional.append(rdata) # Adds additional record to response
        self.packet_size = index + original_total # Changes the packet size depending on the size of the answer section (index represents this)
            
    # This function is used to get the name depending on the offset value
    def decode_name(self, offset):
        name_data = self.data[offset:]
        num_vals = name_data[0]
        name = ""
        index = 0
        more_vals = True
        # While the name is not finished
        while more_vals:
            # Goes through next sequence of characters
            for _ in range(num_vals):
                index += 1
                self.packet_size += 1
                name += chr(name_data[index])
            index += 1
            self.packet_size += 1
            num_vals = name_data[index] # Resets next sequence length
            if num_vals == 0:
                more_vals = False
            elif num_vals == 192: # If pointer is found
                index += 1
                name += "." + self.decode_name(name_data[index])[1] # Recursive call to the offset position
                more_vals = False
            else:
                name += "."
    
        return [index, name]

    # This function decodes the whole packet
    # It only moves on to the next packet section helper function
    # If there is not error encountered to that point
    def decode_packet(self):
        response = Response()
        return_val = self.decode_header(response) # decodes the header
        if return_val == 0:
            return_val = self.decode_question(response) # decodes the question
            if return_val == 0 and response.num_answers != 0:
                self.decode_answer(response) # decodes the answer
                if return_val == 0 and response.num_additional != 0:
                    self.decode_additional(response) # decodes the additional records
        return [return_val, response]
