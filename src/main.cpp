#include <iostream>
#include <thread>
#include "loudness.h"
#include "shared.h"
#include <SFML/Graphics.hpp>

int main() {
    std::thread loudnessthread(loudnessget);
    sf::RenderWindow window(sf::VideoMode(400, 400), "SFML Window");

    // Main loop: runs until the window is closed
    while (window.isOpen()) {
        std::this_thread::sleep_for(std::chrono::milliseconds(20));
        sf::Event event;
        while (window.pollEvent(event)) {
            // Close window if requested
            if (event.type == sf::Event::Closed)
                window.close();
        }

        // Clear the window with black color
        window.clear(sf::Color::Black);
        std::cout << Shared::loudness << "   \r" << std::flush;
        // Draw everything here...

        // Display the contents of the window
        window.display();
    }
    loudnessthread.join();
}