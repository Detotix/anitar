#include <iostream>
#include <portaudio.h>
#include <thread>
#include "shared.h"

int loudnessget() {
    if (Pa_Initialize() != paNoError) return 1;

    PaStreamParameters inputParams;
    inputParams.device = Pa_GetDefaultInputDevice();
    inputParams.channelCount = 1;
    inputParams.sampleFormat = paInt16;
    inputParams.suggestedLatency = Pa_GetDeviceInfo(inputParams.device)->defaultLowInputLatency;
    inputParams.hostApiSpecificStreamInfo = nullptr;

    const int sampleRate = 22050;
    const int chunkSize = 128;    
    PaStream* stream;

    if (Pa_OpenStream(&stream, &inputParams, nullptr, sampleRate, chunkSize, paNoFlag, nullptr, nullptr) != paNoError) {
        Pa_Terminate();
        return 1;
    }

    if (Pa_StartStream(stream) != paNoError) {
        Pa_CloseStream(stream);
        Pa_Terminate();
        return 1;
    }

    int16_t buffer[chunkSize];

    while (Shared::open) {
        if (Pa_ReadStream(stream, buffer, chunkSize) && Pa_ReadStream(stream, buffer, chunkSize) != paInputOverflowed) break;

        int sum = 0;
        for (int i = 0; i < chunkSize; ++i) {
            sum += buffer[i] < 0 ? -buffer[i] : buffer[i];
        }

        Shared::loudness = sum >> 7; 

        std::this_thread::sleep_for(std::chrono::milliseconds(timing::loudness));
    }

    Pa_StopStream(stream);
    Pa_CloseStream(stream);
    Pa_Terminate();
    return 0;
}
