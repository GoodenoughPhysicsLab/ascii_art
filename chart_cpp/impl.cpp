#include <cstdint>
#include <string>
#include <iostream>

#include "pybind11/pybind11.h"
#include "pybind11/numpy.h"
#include "pybind11/pytypes.h"

namespace py = pybind11;

void grayConvert(py::array_t<uint8_t> img, double multiple = 1)
{
    for (int y = 0; y < img.shape()[0]; ++y) {
        for (int x = 0; x < img.shape()[1]; ++x) {
            auto pixel = img.at(y, x);

            if (pixel < 32) { // 255 / 8
                img.mutable_at(y, x) = 0;
            } else if (pixel < 96) { // 255 / 8 * 3
                img.mutable_at(y, x) = static_cast<uint8_t>(1 * multiple);
            } else if (pixel < 160) {
                img.mutable_at(y, x) = static_cast<uint8_t>(2 * multiple);
            } else if (pixel < 224) {
                img.mutable_at(y, x) = static_cast<uint8_t>(3 * multiple);
            } else {
                img.mutable_at(y, x) = static_cast<uint8_t>(4 * multiple);
            }
        }
    }
}

void print_char_art(py::array_t<uint8_t> img, py::list CHAR_PIXEL)
{
    ::std::string cache;

    for (int y = 0; y < img.shape()[0]; ++y) {
        for (int x = 0; x < img.shape()[1]; ++x) {
            auto pixel = img.at(y, x);
            uint_least8_t i{};

            if (pixel < 32) { // 255 / 8
                i = 0;
            } else if (pixel < 96) { // 255 / 8 * 3
                i = 1;
            } else if (pixel < 160) {
                i = 2;
            } else if (pixel < 224) {
                i = 3;
            } else {
                i = 4;
            }

            cache += CHAR_PIXEL[i].cast<::std::string>();
        }
        cache += "\n";
    }

    ::std::cout << cache << '\n';
}

PYBIND11_MODULE(chart_cpp, m) {
    m.def("grayConvert", grayConvert, py::arg("img"), py::arg("multiple") = 1);
    m.def("print_char_art", print_char_art, py::arg("img"), py::arg("CHAR_PIXEL"));
}