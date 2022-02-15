
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
        index = 0 # keep track of index in ttl and type
        if self.num_answers != 0:
            print("\n***Answer Section (" +  str(self.num_answers) + " records)***\n")
        # Goes through all answers, formats them appropriately and prints the lines
        for answer in self.answer:
            if self.type[index] == 1 or self.type[index] == 2 or self.type[index] == 5 or self.type[index] == 15:
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
                
                print(response)
            index += 1
        
        add_responses = []
        # Goes through all additional records and formats them appropriately
        # Filters out the non-compatible records
        for additional in self.additional:
            if self.type[index] == 1 or self.type[index] == 2 or self.type[index] == 5 or self.type[index] == 15:
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
                
                add_responses.append(response)
            else:
                self.num_additional -= 1
            index += 1
        
        if self.num_additional != 0:
            print("\n***Additional Section (" +  str(self.num_additional) + " records)***\n")
        
        # prints all the appropriate additional records
        for additional in add_responses:
            print(additional)
        
        print("\n")
            


    