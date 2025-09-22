// shared.h
#ifndef SHARED_H
#define SHARED_H

#include <vector>

#include "json.hpp"
using json = nlohmann::json;


class timing { // timing of threads
    public:
        inline static int window = 20; // all three in ms 
        inline static int loudness = 10; 
        inline static int eventhandler = 20; 
};

class Shared { // shared vars
    public:
        inline static int loudness = 0; 
        inline static bool open = true;
        
        inline static json charbase;
        inline static json eventdict;
        inline static json settings;
        
        inline static std::vector<std::string> eventlist;
};

#endif
