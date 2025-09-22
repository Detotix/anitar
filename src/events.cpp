#include <thread>
#include "shared.h"
#include <fstream>
#include <iostream>

void start() {
    std::ifstream settings("settings.json");
    Shared::settings = json::parse(settings);
    
    std::string selected=Shared::settings["select"];
    std::ifstream charbase("chars/"+selected+"/charbase.json");
    Shared::charbase = json::parse(charbase);
}

void eventhandler() {
    std::this_thread::sleep_for(std::chrono::milliseconds(timing::eventhandler));
}

json renderstring(std::string renderstring) {
    json renderinfo;
    return renderinfo;
}