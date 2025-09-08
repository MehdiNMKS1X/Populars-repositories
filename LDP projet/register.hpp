#ifndef registre_hpp
#define registre_hpp

#include <cstdint>

// Register class to encapsulate register operations
class Register {
private:
    uint16_t value;

public:
    // Constructor
    Register(uint16_t val = 0) : value(val) {}
    
    // Conversion operator
    operator uint16_t() const { return value; }
    
    // Assignment operator
    Register& operator=(uint16_t val) {
        value = val;
        return *this;
    }
    
    // Arithmetic operators
    Register& operator+=(uint16_t val) {
        value += val;
        return *this;
    }
    
    Register& operator-=(uint16_t val) {
        value -= val;
        return *this;
    }
};

#endif // register_hpp
