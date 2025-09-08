#ifndef INSTRUCTION_HPP
#define INSTRUCTION_HPP

#include <string>

class Instruction {
private:
    std::string opcode;
    std::string operand1;
    std::string operand2;

public:
    // Constructor that takes an instruction string
    Instruction(const std::string& instruction_str);
    
    // Destructor
    ~Instruction();
    
    // Getters for instruction components
    std::string get_opcode() const;
    std::string get_operand1() const;
    std::string get_operand2() const;
};

#endif // INSTRUCTION_HPP
