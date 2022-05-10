#ifndef ARRAY_H
#define ARRAY_H

#include <vector>
#include <stdexcept>

template<typename T>
class Array2 {

    public:

        Array2(int ncols) : m_ncols(ncols) { }
        Array2(int nrows, int ncols) : m_ncols(ncols) {
            m_data = std::vector<T>(nrows * ncols, 0);
            m_data.resize(nrows * ncols);
        }
        void append (const std::vector<T>& row) {
            if (row.size() != m_ncols) {
                throw std::runtime_error("Row size does not match ncols");
            }
            for (auto& elem : row) {
                m_data.push_back(elem);
            }            
        }
        int get_nrows() {
            return m_data.size() / m_ncols;
        }
        int get_ncols() {
            return m_ncols;
        }

        std::vector<T>* data(){
            return &m_data;
        }

    private:

        int m_ncols, m_nrows;
        std::vector<T> m_data;

};




#endif // ARRAY_H