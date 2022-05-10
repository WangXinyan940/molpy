cmake_minimum_required(VERSION 3.20)

project(molpy_cpp_test)
set(CMAKE_CXX_STANDARD 11)

include(FetchContent)
FetchContent_Declare(
  googletest
  URL https://github.com/google/googletest/archive/609281088cfefc76f9d0ce82e1ff6c30cc3591e5.zip
)
# For Windows: Prevent overriding the parent project's compiler/linker settings
set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
FetchContent_MakeAvailable(googletest)
enable_testing()

set(SRC_DIR ../src)
set(INCLUDE_DIR ../include)
include_directories(molpy_cpp_test PRIVATE ../include)

# test pybind
find_package(pybind11)
pybind11_add_module(vec ../src/vec_bind.cpp)
pybind11_add_module(arrayTest ../src/array_bind.cpp)

# test cpp
set(SOURCES test_vec.cpp test_array.cpp test_main.cpp)

add_executable(
  molpy_cpp_test
  ${SOURCES}
)

target_link_libraries(
  molpy_cpp_test
  gtest_main
)

include(GoogleTest)
gtest_discover_tests(molpy_cpp_test)