
class Response:

    def __init__(self):
        self.id = None
        self.auth = None
        self.type = []
        self.name = None
        self.ttl = []
        self.answer = []
        self.additional = []
        self.num_answers = 0
        self.num_additional = 0
    
    def display_response(self):
        index = 0
        if self.num_answers != 0:
            print("\n***Answer Section (" +  str(self.num_answers) + " records)***\n")
        for answer in self.answer:
            response = ""
            if self.type[index] == 1:
                response += "IP\t"
            elif self.type[index] == 2:
                response += "NS\t"
            elif self.type[index] == 5:
                response += "CNAME\t"
            else:
                response += "MX\t"
            
            response += answer + "\t"
            response += str(self.ttl[index]) + "\t"

            if self.auth == '1':
                response += "auth"
            else:
                response += "nonauth"
            
            index += 1
            print(response)
        
        if self.num_additional != 0:
            print("\n***Additional Section (" +  str(self.num_additional) + " records)***\n")
        for additional in self.additional:
            response = ""
            if self.type[index] == 1:
                response += "IP\t"
            elif self.type[index] == 2:
                response += "NS\t"
            elif self.type[index] == 5:
                response += "CNAME\t"
            else:
                response += "MX\t"
            
            response += additional + "\t"
            response += str(self.ttl[index]) + "\t"

            if self.auth == '1':
                response += "auth"
            else:
                response += "nonauth"
            
            index += 1
            print(response)
        
        print("\n")
            


    