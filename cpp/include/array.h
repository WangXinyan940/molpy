#ifndef ARRAY_H
#define ARRAY_H

#include <vector>
#include <ostream>
#include <functional>

template<typename T>
class Array {

    public:

        std::vector<T> data;
        std::vector<int> shape;
        std::vector<int> strides;

        void append(T value) {
            data.emplace_back(value);
        }

        void append(std::initializer_list<T> value) {
            for (auto i: value)
                append(i);
        }

        void clear() {
            data.clear();
        }

        const T* getPtr() const {
            return data.data();
        }

        T dtype() const {
            return data.value_type;
        }

        int getSize() const {
            return data.size();
        }

        int getNdim() const {
            return shape.size();
        }

};

#endif // ARRAY_H