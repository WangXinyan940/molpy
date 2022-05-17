#ifndef ARRAY_H
#define ARRAY_H

#include <vector>
#include <ostream>

template<typename T>
class Array {

    public:

        std::vector<T> data;
        std::vector<int> shape;
        std::vector<int> strides;
        int ndim;

        void append(T value) {
            this->data.emplace_back(value);
        }

        void append(std::initializer_list<T> value) {
            for (auto i: value)
                this->data.emplace_back(i);
        }

        T* ptr() {
            return this->data.data();
        }

        void clear() {
            this->data.clear();
        }

        T dtype() {
            return data.value_type;
        }

};

#endif // ARRAY_H