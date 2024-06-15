#include <cstdint>

#include "pybind11/numpy.h"
#include "pybind11/pytypes.h"

namespace py = pybind11;

void grayConvert(py::array_t<uint8_t> img, double multiple = 1, py::object callback = py::none())
{
    for (int y = 0; y < img.shape()[0]; ++y) {
        for (int x = 0; x < img.shape()[1]; ++x) {
            auto pixel = img.at(y, x);

            if (pixel < 32) { // 255 / 8
                img.mutable_at(y, x) = 0;
            } else if (pixel < 96) { // 255 / 8 * 3
                img.mutable_at(y, x) = 1 * multiple;
            } else if (pixel < 160) {
                img.mutable_at(y, x) = 2 * multiple;
            } else if (pixel < 224) {
                img.mutable_at(y, x) = 3 * multiple;
            } else {
                img.mutable_at(y, x) = 4 * multiple;
            }

            if (callback.is_none() == false) {
                callback(x, y, img.at(y, x));
            }
        }
    }
}

PYBIND11_MODULE(chart_cpp, m) {
    m.def("grayConvert", grayConvert, py::arg("img"), py::arg("multiple") = 1, py::arg("callback") = py::none());
}