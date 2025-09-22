#include <iostream>
#include <thread>
#include "loudness.h"
#include "shared.h"
#include <SFML/Graphics.hpp>
#include "events.h"

int main() {
    start();
    std::thread loudnessthread(loudnessget);
    std::thread eventhandlerthread(eventhandler);
    sf::RenderWindow window(sf::VideoMode(400, 400), "Anitar v5", sf::Style::Titlebar | sf::Style::Close);
    while (window.isOpen()) {
        std::this_thread::sleep_for(std::chrono::milliseconds(timing::window));
        sf::Event event;
        while (window.pollEvent(event)) {
            if (event.type == sf::Event::Closed) {
                Shared::open = false;
                window.close();
            }
        }

        window.clear(sf::Color::Black);
        std::cout << Shared::loudness << "   \r" << std::flush;

        window.display();
    }
    
    eventhandlerthread.join();
    loudnessthread.join();
}